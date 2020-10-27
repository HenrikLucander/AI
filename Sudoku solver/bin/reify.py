#!/usr/bin/python3

from logicparser import Parser, LexerError, ParsingError
import sys
    
def output_subtree(node, out, minimal=False, id_to_var=False):
    if node.done:
        return
    index = node.index
    if node.kind == "op":
        out.append("op(%d,%s)." % (node.index, node.name))
    elif node.kind == "atom":
        out.append("ident(%d,%s)." % (node.index, node.aspname()))
        if id_to_var:
            out.append("%s :- true(%d)." % (node.aspname(), node.index))
    elif node.kind == "const":
        out.append("const(%d,%s)." % (node.index, node.aspname()))
    else:
        out.append("variable(%d,%s)." % (node.index, node.aspname()))
        
    if not minimal:
        out.append("leaves(%d,%d)." % (node.index, node.leaves))
        
    args = node.kind in ("term", "atom")
    for nth, child in enumerate(node.children):
        if args:
            out.append("arg(%d,%d,%d)." % (index,nth+1,child.index))
        else:
            out.append("subf(%d,%d)." % (index,child.index))
            if node.ordered or not minimal:
                out.append("nth_child(%d,%d,%d)." % (index,nth+1,child.index))
        
        output_subtree(child, out, minimal, id_to_var)
            
    if not node.children:
        out.append("leaf(%d)." % node.index)
        
    node.done = True
        
        
def error(msg, retval):
    print(msg, file=sys.stderr)
    sys.exit(retval)

        
def to_lparse(clause, atoms):
    atoms.update(abs(a) for a in clause)
    clause.sort()
    lits = len(clause)
    negstart = lits
    
    for i, l in enumerate(clause):
        if l > 0:
            negstart = i
            break
    negs = lits - negstart
    neg = " ".join(str(i) for i in clause[negstart:])
    pos = " ".join(str(-i) for i in clause[:negstart])
    space = " " if len(neg) and len(pos) else ""
    return "1 1 %d %d %s%s%s" % (lits, negs, neg, space, pos)
    
def symbol_table(node, out, exprsymbols):
    if node.done:
        return
    node.done = True
    if node.is_ident():
        out.append("%d %s" % (node.index, node.aspname()))
    elif exprsymbols:
        out.append("%d %s" % (node.index, str(node).replace(" ","")))
    for c in node.children:
        symbol_table(c, out, exprsymbols)
    
def ground_root(root, out, atoms):
    clauses = []
    root.root_cnf(clauses)
    for e in root.exprs:
        e.to_cnf(clauses)
    for clause in clauses:
        out.append(to_lparse(clause, atoms))
        
def ground_epilogue(parser, out, shown, root_ids, atoms):
    end = parser.nextindex
    atomrule = "3 %d %s 0 0" % (len(atoms), " ".join(str(i) for i in atoms))
    out.append(atomrule)
    out.append("0")
    
    symbols = list(parser.symboltable.values())
    for atom in symbols:
        if atom.index != 0 and (not shown or atom.basename in shown):
            out.append("%d %s" % (atom.index, atom.aspname()))
    out.append("0")
    out.append("B+")
    #out.append(" ".join(str(r) for r in root_ids))
    #if exprsymbols:
    #    out.append(" ".join(str(r) for r in require))
    out.append("0")
    out.extend(["B-", "1", "0"])
    out.append("1")
    
def ground(roots, exprsymbols=False):

    maxindex = roots[-1].maxindex
    clauses = []
    for root in roots:
        root.root_cnf(clauses)
    atoms = set()
    for clause in clauses:
        for atom in clause:
            atoms.add(abs(atom))
        out.append(to_lparse(clause))
    require = []

    if exprsymbols:
        for root in roots:
            require.append(root.index)
            atoms.add(root.index)
    atoms = list(atoms)
    atomrule = "3 %d %s 0 0" % (len(atoms), " ".join(str(atom) for atom in atoms))
    out.append(atomrule)
    out.append("0")
    
    for root in roots:
        symbol_table(root, out, exprsymbols)
    out.append("0")
    out.append("B+")
    if exprsymbols:
        out.append(" ".join(str(r) for r in require))
    out.append("0")
    out.extend(["B-", "1", "0"])
    out.append("1")
    return "", "\n".join(out)
        
        
def reify(inputs, reorder=False, collapse=True, minimal=True, wrapper="%s", id_to_var=False, parseonly=False, format="asp", exprsymbols=False, shown=set()):
    if isinstance(inputs,str):
        inputs = [inputs]
    track_exprs = True
    startindex = 1
    ground = (format == "ground")
    if ground:
        minimal = True
        collapse = True
        startindex = 2
        track_exprs = False
        
    parser = Parser(wrapper=wrapper, collapse=collapse, reorder_subexprs=reorder, track_exprs=track_exprs, minimal=minimal, startindex=startindex)
    
    out = []
    roots = []
    root_ids = set()
    atoms = set()
    try:
        for input in inputs:
            for line in input.split("\n"):
                roots += parser.parse(line)
                if ground:
                    for root in roots:
                        ground_root(root, out, atoms)
                        root_ids.add(root.index)
                    roots = []
    except LexerError as e:
        error("LexerError: " + e.args[0], -1)
    except ParsingError as e:
        error(str(e), -2)
        
    if ground:
        ground_epilogue(parser, out, shown, root_ids, atoms)
        return parser.symboltable, "\n".join(out)
        
    if not len(roots) and not ground: 
        error("No expression found!", -3)
    if parseonly:
        return ""
    
    maxindex = roots[-1].maxindex
    
    out.append("node(1..%d)." % maxindex)
    for root in roots:
        if not minimal:
            out.append("% Expression: " + str(root))
            out.append("% Disambiguated: " + root.disambig_str(True))
            out.append("% Tex: " + root.tex_str(True))
        out.append("root(%d)." % root.index)
        out.append("lastsubexpr(%d,%d)." % (root.index, root.maxindex))
        exprs = root.exprs
        if not minimal:
            for e in root.exprs:
                if e.orig == e:
                    out.append("unique(%d)." % e.index)
                    out.append('tex(%d,"%s").' % (e.index,e.tex_str(True,True).replace('\\', '\\\\')))
                else:
                    out.append("duplicate(%d,%d)." % (e.index, e.orig.index))
            out.append("% Sorted subexpressions: " + ", ".join(str(e) for e in exprs if e.orig == e))
        output_subtree(root, out, minimal=minimal, id_to_var=id_to_var)
    return roots, "\n".join(out)
    
if __name__ == '__main__':
    reorder = False
    inputs = []
    args = sys.argv
    wrapper = "%s"
    
    formula = False
    wrap = False
    collapse = True
    minimal = False
    parseonly = False
    id_to_var = False
    exprsymbols = False
    show = False
    shown = set()
    for (i, arg) in enumerate(args):
        if show:
            shown = set(arg.split(","))
            show = False
        elif formula:
            inputs.append(arg)
            formula = False
        elif wrap:
            wrapper = arg
            wrap = False
        elif arg == "-f":
            formula = True
        elif arg == "-w":
            wrap = True
        elif arg == "--show":
            show = True
        elif arg == "--sort":
            reorder = True
        elif arg == "--nocollapse":
            collapse = False
        elif arg == "--minimal":
            minimal = True
        elif arg == "--parse":
            parseonly = True
        elif arg == "--idtovar":
            id_to_var = True
        elif arg == "--ground":
            format = "ground"
        elif arg == "--exprsymbols":
            exprsymbols = True
    if not inputs:
        inputs = [sys.stdin.read()]
    _, reified = reify(inputs, reorder=reorder, collapse=collapse, minimal=minimal, wrapper=wrapper, id_to_var=id_to_var, parseonly=parseonly, format=format, exprsymbols=exprsymbols, shown=shown)
    print(reified)