#!/usr/bin/python3

import sys

def name(sym):
    return sym[:sym.find("(")] 

if __name__ == '__main__':
    trueatoms = set()
    falseatoms = set()
    names = set()
    symbols = {}
    for i in range(1,len(sys.argv)-1,2):
        op = sys.argv[i]
        if "t" in op:
            atoms = trueatoms
        elif "f" in op:
            atoms = falseatoms
        with open(sys.argv[i+1]) as f:
            curr = f.read().split()
            atoms.update(curr)
            if "o" in op:
                names.update(name(c) for c in curr)
    phase = 0
    forbid = []
    require = []
    for line in open(sys.argv[-1]):
        if line[-1] == "\n":
            line = line[:-1]
        print(line)
        if line == "0":
            phase += 1
        elif phase == 1:
            id, sym = line.split()
            if sym in trueatoms:
                require.append(id)
            if sym in falseatoms:
                forbid.append(id)
            if name(sym) in names and sym not in trueatoms:
                forbid.append(id)
        elif line == "B+":
            if require:
                print(" ".join(require))
        elif line == "B-":
            if forbid:
                print(" ".join(forbid))