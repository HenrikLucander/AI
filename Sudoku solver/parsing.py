def read_atoms(line):
    if len(line) < 2:
        return set()
    return set(line.replace(".","").split(" "))
    
def parse_file(filename):
    with open(filename) as f:
        return parse(f.read())
       
def parse_line(line):
    if line.startswith("UNSATISFIABLE"):
        print("No solution found!")
        return []
    elif line.startswith("SATISFIABLE"):
        return []
    return read_atoms(line)
    

def parse(text):
    lines = text.split("\n")
    if not lines or lines[-1] == "UNSATISFIABLE":
        return []
        
    sudokus = []
    for line in lines:
        if "(" not in line:
            continue
        sudokus.append(read_atoms(line))
    return sudokus
    
def num_ok(x,n):
    return x >= 1 and x <= n
    
def to_table(atoms,n,name="value"):
    sudoku = [[0 for i in range(n+1)] for i in range(n+2)]
    sudoku[n+1] = ""
    for atom in atoms:
        atom = atom.replace(".","").replace("\n","")
        if atom.startswith(name + "("):
            x,y,v = [int(i) for i in atom[len(name)+1:-1].split(",")]
            if sudoku[y][x]:
                sudoku[n+1] = "Multiple values at (%d,%d): at least %d and %d!" % (x,y,sudoku[y][x],v)
            sudoku[y][x] = v
                
    return sudoku
        
