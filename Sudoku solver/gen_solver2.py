#!/usr/bin/python3

from submission import alternative_solution_finder
    
if __name__ == '__main__':
    import sys
    n = 9
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    rules = alternative_solution_finder(n)
    print("\n".join(str(r) for r in rules))