"""
Wrapper around the pyasp.ply submodule.

"""
import inspect

import pyasp.ply.lex as lex
import pyasp.ply.yacc as yacc
import re

class LexerError(Exception):
    pass
    
class ParsingError(Exception):
    pass


class Lexer:
    tokens = (
        'IDENT',
        'NUM',
        'LP',
        'RP',
        'COMMA',
        'AND',
        'OR',
        'NOT',
        'IMPLIES',
        'EQUIV'
    )

    # Tokens
    t_IDENT = r'(\\([^lr]|lambd|rh))?[a-zA-Z_][a-zA-Z0-9_]*'
    t_NUM = r'-?[0-9]+'
    t_LP = r'\('
    t_RP = r'\)'
    t_COMMA = r','
    t_AND = r'(&|∧|\\land)'
    t_OR = r'(\||∨|\\lor)'
    t_NOT = r'(-|¬|\\lnot)'
    t_IMPLIES = r'(-\>|→|\\rightarrow|\\limpl)'
    t_EQUIV = r'(\<-\>|↔|⟷|\\leftrightarrow|\\longleftrightarrow|\\lequiv)'
    t_ignore  = ' \t'
    t_ignore_COMMENT = r'%.*'
    

    def __init__(self):
        self.lexer = lex.lex(object=self)

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        wrong = str(t.value[0])
        msg = "Illegal character " + wrong + "."
        if wrong == "~":
            msg += " Note that negation is signified by -."
        raise LexerError(msg)
        
precedence = { 
    "neg": 1, 
    "and": 2,
    "or": 3,
    "implies": 4,
    "equiv": 5
}
          
opsymbols = { "and": "&", "or": "|", "implies": "->", "equiv": "<->", "neg": "-" }    
optex = { "and": r"\land", "or": r"\lor", "implies": r"\rightarrow", "equiv": r"\leftrightarrow", "neg": r"\neg " }
nodes = {}
class Node:

    def sat_id(self):
        return self.index
        
    def root_cnf(self, clauses):
        me = self.sat_id()
        clauses.append([me])
            
    def to_cnf(self, clauses):
        pass
        
    def is_ident(self):
        return not self.is_op()
        
    def aspname(self):
        addquotes = "\\" in self.name
        name = self.name.replace("\\","\\\\")
        if name.startswith("\\"):
            name = '$' + name + '$'
        if addquotes:
            name = '"' + name + '"'
        return name
        
    def countleaves(self):
        if self.children:
            self.leaves = 0
            for c in self.children:
                c.countleaves()
                self.leaves += c.leaves
        else:
            self.leaves = 1
            
    def __init__(self, kind, name, children, merge=False, ordered=False, collapse=False):
        self.kind = kind
        self.name = name
        self.basename = name
        self.orig = self
        self.index = 0
        self.sortkey = None
        
        self.children = children
        self.parenthesized = False
        self.ordered = ordered
        
        if not collapse or not children:
            self.name = name
        else:
            self.name = name + "(" + ",".join(c.name for c in children) + ")"
            self.children = []
        if merge:
            self.children = []
            for child in children:
                if not child.parenthesized and child.name == name:
                    self.children += child.children
                else:
                    self.children.append(child)
                    
    def calc_sortkey(self, reorder=False, isroot=False):
        if self.sortkey:
            return
        key = self._sortkey()
        if self.children:
            for child in self.children:
                child.calc_sortkey(reorder)
            if not self.ordered:
                _children = sorted(self.children, key=lambda n: n.sortkey)
            else:
                _children = self.children
            key += "(" + ",".join(c.sortkey for c in _children) + ")"
            if reorder:
                self.children = _children
        if isroot:
            self.sortkey = key + "A"
        else:
            self.sortkey = key + "B"
        
    def __str__(self, isroot=True):
        return self._str(Node.__str__, noparen=isroot)
        
    def disambig_str(self, isroot=True):
        if self.parenthesized or not isroot and self.is_op():
            begin = "("
            end = ")" 
        else:
            begin = end = ""
        return begin + self._str(Node.disambig_str, noparen=True) + end
        
    def tex_str(self, isroot=True, noparen=False):
        if isroot:
            begin = end = "$"
        else:
            begin = end = ""
        return begin + self._str(Node.tex_str, optex, noparen) + end
        
        
    def _str(self, tostr_func, opnames=opsymbols, noparen=False):
        if self.parenthesized and not noparen:
            return "(" + self._str(tostr_func, opnames, True) + ")"
        if not self.children:
            return self.name
        else:
            return self._str_inner(tostr_func, opnames, noparen)
            
    def flatten(self):
        flattened = [self]
        for c in self.children:
            flattened += c.flatten()
        return flattened

        
class Symbol(Node):
    def is_op(self):
        return False
    def _sortkey(self):
        return "0" + self.name
        
    def _str_inner(self, tostr_func, opnames=opsymbols, noparen=False):
        return self.name + "(" + ",".join(tostr_func(child, False) for child in self.children) + ")"
        
class Op(Node):

    def _str_inner(self, tostr_func, opnames=opsymbols, noparen=False):
        if len(self.children) == 1:
            return opnames[self.name] + tostr_func(self.children[0], False)
        else:
            return (" " + opnames[self.name] + " " ).join(tostr_func(child, False) for child in self.children)
            
    def is_op(self):
        return True
    def _sortkey(self):
        return str(precedence[self.name])
        
    def is_neg(self):
        return self.name == "neg"
        
    def sat_id(self):
        if self.is_neg():
            return -self.children[0].sat_id()
        return self.index
       
    def root_cnf(self, clauses):
        me = self.sat_id()
        #if me != self.index:
        #    clauses.append([self.index])
        op = self.name
        ids = [c.sat_id() for c in self.children]

        if op == "and":
            for c in self.children:
                c.root_cnf(clauses)
            return
            
        a, b = ids[0], ids[-1]
            
        if op == "or":
            clauses.append(ids)
        elif op == "implies":
            clauses.append([-a, b])
        elif op == "equiv":
            clauses.extend([[-a, b], [-b, a]])
        elif op == "neg":
            clauses.append([me])

    def to_cnf(self, clauses):
        op = self.name
        me = self.sat_id()
        ids = [c.sat_id() for c in self.children]
        a, b = ids[0], ids[-1]
        
        if op == "implies":
            # me -> (b | -a)
            # -me | b | -a
            clauses.append([-me, b, -a])
            
            # (b | -a) -> me
            # (-b & a) | me
            # (-b | me) & (a | me)
            clauses.append([me, -b])
            clauses.append([me, a])
        elif op == "equiv":
            a, b = ids
            # me -> (a <-> b)
            # -me | (a <-> b)
            # -me | a&b | -a&-b
            # (-me | a | -b) & (-me | b | -a)
            clauses.append([-me, a, -b])
            clauses.append([-me, b, -a])
            # (a <-> b) -> me
            # (a&-b) | (b&-a) | me
            # (me | a | b) & (me | -a | -b)
            clauses.append([me, a, b])
            clauses.append([me, -a, -b])
        elif op == "or":
            # me -> a|b|c|d...
            # -me|a|b|c|...
            clauses.append(ids + [-me])
            
            # a|b|... -> me
            # (-a&-b&...)|me
            # (-a|me)&(-b|me)&...
            clauses.extend([[-id,me] for id in ids])
            
        elif op == "and":
            # me -> a&b&...
            # -me | a&b&...
            # (-me|a)&(-me|b)&...
            clauses += [[id,-me] for id in ids] 
            
            # a&b&... -> me
            # -a|-b|...|me
            clauses.append([-id for id in ids] + [me])
        elif op == "neg": 
            pass      
            
class Parser:
    start = 'sentences'

    def __init__(self, merge=True, collapse=False, minimal=False, reorder_subexprs=False, track_exprs=True, startindex=1, wrapper="%s"):
        self.lexer = Lexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self, write_tables=0)
        self.roots = []
        self.merge = merge
        self.collapse = collapse
        self.wrapper = wrapper
        self.minimal = minimal
        self.symboltable = dict()
        self.track_exprs = track_exprs
        self.nextindex = startindex
        self.reorder_subexprs = reorder_subexprs
        
    def get_node(self, node):
        if not isinstance(node, Symbol) and not self.track_exprs:
            return node
            
        key = str(node)
        if key not in self.symboltable:
            self.symboltable[key] = node
        elif self.minimal:
            node = self.symboltable[key]
        else:
            node.orig = self.symboltable[key]
            
        return node
        
    def p_sentences(self, t):
        """sentences : sentence COMMA sentences
                     | sentence"""
        if len(t) == 4:
            t[0] = [t[1]] + t[3]
        else:
            t[0] = [t[1]]
        self.roots = t[0]
        

    def p_sentence(self, t):
        """sentence : atom 
                    | negation
                    | conjunction
                    | disjunction
                    | implication
                    | equivalence
                    | parenthesized
        """
        t[0] = t[1]
        
    def p_arglist(self, t):
        """arglist : LP args RP 
                   |
        """
        if len(t) == 4:
            t[0] = t[2]
        else:
            t[0] = []

    def p_args(self, t):
        """args : arg COMMA args
                | arg
        """
        if len(t) == 2:
            t[0] = [t[1]]
        else:
            t[0] = [t[1]] + t[3]
            
    def p_const(self, t):
        """ const : NUM """
        t[0] = self.get_node(Symbol("const", t[1], []))
            
    def p_arg(self, t):
        """ arg : term 
                | const """
        t[0] = t[1]

    def p_term(self, t):
        """term : IDENT arglist
        """
        t[0] = self.get_node(Symbol("term", self.wrapper % t[1], t[2], collapse=self.collapse))
    
    def p_atom(self, t):
        """atom : IDENT arglist
        """
        t[0] = self.get_node(Symbol("atom", self.wrapper % t[1], t[2], collapse=self.collapse))
        
    def p_negation(self, t):
        """negation : NOT negatable"""
        t[0] = self.get_node(Op("op", "neg", [t[2]]))
        
    def p_conjunction(self, t):
        """conjunction : conjunct AND conjunct"""
        t[0] = self.get_node(Op("op", "and", [t[1], t[3]], merge=self.merge))
        
    def p_disjunction(self, t):
        """disjunction : disjunct OR disjunct"""
        t[0] = self.get_node(Op("op", "or", [t[1], t[3]], merge=self.merge))
        
    def p_implication(self, t):
        """implication : condition IMPLIES condition"""
        t[0] = self.get_node(Op("op", "implies", [t[1], t[3]], ordered=True))
        
    def p_equivalence(self, t):
        """equivalence : condition EQUIV condition"""
        t[0] = self.get_node(Op("op", "equiv", [t[1], t[3]]))
        
    def p_parenthesized(self, t):
        """parenthesized : LP conjunction RP 
                         | LP disjunction RP 
                         | LP implication RP 
                         | LP equivalence RP
                         | LP negation RP
                         | LP atom RP
                         | LP parenthesized RP"""
        t[0] = t[2]
        t[0].parenthesized = True
        
    def p_negatable(self, t):
        """negatable : atom 
                     | negation
                     | parenthesized"""
        t[0] = t[1]
                     
    def p_conjunct(self, t):
        """conjunct : atom 
                    | negation
                    | conjunction
                    | parenthesized"""
        t[0] = t[1]
                    
    def p_disjunct(self, t):
        """disjunct : atom 
                    | negation
                    | conjunction
                    | disjunction
                    | parenthesized"""
        t[0] = t[1]
                     
    def p_condition(self, t):
        """condition : atom 
                     | negation
                     | conjunction
                     | disjunction
                     | parenthesized"""
        t[0] = t[1]
                     
        
        
    def p_error(self, t):
        if t is None:
            msg = "Syntax error: something is missing at the end of the expression (e.g. a closing brace or the right side of a binary operator)"
        elif isinstance(t, lex.LexToken):
            msg = "Syntax error at line %d, column %d: %s" % (t.lineno, t.lexpos+1, str(t.value))
        else:
            msg = "Syntax error at " + str(t)
        
        # Haven't seen a useful stack trace from this. 
        # msg += "\n" + ''.join(map(lambda x: "  %s:%s\n    %s" % (x[1], x[2], x[4][0]),
        #                   inspect.stack()))
        raise ParsingError(msg)

    def parse(self, line):
        line = line.strip()
        self.roots = []
        if len(line) > 0:
            self.parser.parse(line, lexer=self.lexer.lexer)
            
        index = self.nextindex
        for root in self.roots:
            root.calc_sortkey(self.reorder_subexprs, True)
            root.countleaves()
            exprs = root.flatten()
            exprs.sort(key=lambda x: x.sortkey)
            for e in exprs:
                if not e.index:
                    e.index = index
                    e.done = False
                    index += 1
            root.exprs = exprs
            root.maxindex = index - 1
        self.nextindex = index
        return self.roots


def filter_empty_str(l):
    return [x for x in l if x != '']

    