

# From Z3 https://github.com/Z3Prover/z3/blob/master/src/api/python/z3/z3.py
# Hack for having nary functions that can receive one argument that is the
# list of arguments.
def _get_args(args):
    try:
        if len(args) == 1 and (isinstance(args[0], tuple) or isinstance(args[0], list)):
            return args[0]
        elif len(args) == 1 and isinstance(args[0], set):
            return [arg for arg in args[0]]
        else:
            return args
    except:  # len is not necessarily defined when args is not a sequence (use reflection?)
        return args
        

class Expr:
    def __init__(self, name, children=[], is_operator=True):
        self.name = str(name)
        self.children = [to_expr(child) for child in children]
        self.is_operator = is_operator
        
    def precedence(self):
        if not self.is_operator:
            return 0
        precedence = { 
            "-": 1, 
            "&": 2,
            "|": 3,
            "->": 4,
            "<->": 5
        }
        return precedence[self.name]
        
    def child_str(self, parent):
        s = str(self)
        if self.precedence() >= min(parent.precedence(),2):
            return "(" + s + ")"
        else:
            return s
            
    def __str__(self):
        if not self.is_operator:
            if self.children:
                return "%s(%s)" % (self.name, ",".join(str(c) for c in self.children))
            else:
                return self.name
        elif not self.children:
            # Empty conjunction is true
            if self.name == "&":
                return "a|-a"
            # Empty disjunction is false
            elif self.name == "|":
                return "a&-a"
        elif len(self.children) == 1:
            s = self.children[0].child_str(self)
            if self.name == "-":
                return "-" + s
            else:
                return s
        else:
            return (" " + self.name + " ").join(c.child_str(self) for c in self.children)
        
def And(*args):
    return Expr("&", _get_args(args))

def Not(a):
    return Expr("-", [a])
    
def Or(*args):
    return Expr("|", _get_args(args))

def Implies(a, b):
    return Expr("->", [a,b])
    
def Equivalent(a, b):
    return Expr("<->", [a,b])
    
def Var(name, params=[]):
    return Expr(name, params, is_operator=False)
    
def orig_value(x,y,v):
    return Var("orig_value", [x,y,v])
    
def _not(x,y,v):
    return Not(value(x,y,v))
    
def to_expr(e):
    if isinstance(e, Expr):
        return e
    return Var(e)
    