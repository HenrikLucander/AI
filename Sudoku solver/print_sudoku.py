#!/usr/bin/python3

from parsing import parse_line, parse_file, to_table
import sys
from sys import argv
from math import sqrt

def divider(n,k):
    base = "+" + "-"*k
    return base*k + "+"

def print_sudoku(sudoku,name,n,print_error=True):
    k = int(sqrt(n))
    ret = [divider(n,k)]
    if print_error and sudoku[n+1]:
        print(sudoku[n+1])
    for y in range(1,n+1):
        cur = ["|"]
        for x in range(1,n+1):
            v = sudoku[y][x]
            if not v:
                val = " "
            else:
                val = hex(sudoku[y][x])[2:]
            cur.append(val)
            if x % k == 0:
                cur.append("|")
        ret.append("".join(cur))
        if y % k == 0:
            ret.append(divider(n,k))
    print("\n".join(ret))
    
    
if __name__ == "__main__":

    name = "value"
    if len(argv) < 2:
        print("Usage: python3 print_sudoku.py <n> <instance>")
        print("You may also pass the instance via stdin instead")
        sys.exit()
    n = int(argv[1])
    if len(argv) > 2:
        name = argv[2]
    for line in sys.stdin:
        res = parse_line(line)
        if res:
            sudoku = to_table(res,n,name)
            #print(" ".join(sorted(line.split())))
            print_sudoku(sudoku,name,n)