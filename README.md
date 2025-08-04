# Sudoku Solver with Step-by-Step Explanations

A comprehensive Sudoku solver that provides detailed explanations for each solving step, helping you understand the techniques used to solve Sudoku puzzles.

## 🎯 Main Solution: File-Based Solver

The primary way to use this solver is through the **file-based command-line interface**:

```bash
# Solve a puzzle from a file and output to a solution file
python file_solver.py puzzle.txt

# The output file will be automatically named: puzzle_solution.txt
```

### Features of the File Solver

- **📁 File Input/Output**: Read puzzles from text files, output detailed solutions
- **📝 Step-by-Step Explanations**: Each step includes detailed reasoning
- **🎨 Visual Board Display**: Shows incremental progress with highlighted new placements
- **🔍 Detailed Candidate Removal**: Lists exactly which candidates are removed from which cells
- **📊 Multiple Output Formats**: Verbose mode with extra details

### Example Usage

```bash
# Basic usage
python file_solver.py puzzle.txt

# Verbose mode with extra details
python file_solver.py puzzle.txt -v

# Specify custom output file
python file_solver.py puzzle.txt -o my_solution.txt
```

### Input File Format

Create a text file with your Sudoku puzzle (use 0 or . for empty cells):

```
5 3 0 0 7 0 0 0 0
6 0 0 1 9 5 0 0 0
0 9 8 0 0 0 0 6 0
8 0 0 0 6 0 0 0 3
4 0 0 8 0 3 0 0 1
7 0 0 0 2 0 0 0 6
0 6 0 0 0 0 2 8 0
0 0 0 4 1 9 0 0 5
0 0 0 0 8 0 0 7 9
```

## 🚀 Quick Start

1. **Clone the repository**:
```bash
git clone <repository-url>
cd sudoku-solver-with-explanations
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Create a puzzle file** and solve it:
```bash
python file_solver.py your_puzzle.txt
```

## 🛠️ Alternative Interfaces

### Interactive CLI
```bash
python cli_solver.py
```

### Simple Demo CLI
```bash
python simple_cli.py
```

### Web Interface
```bash
python app.py
# Then open http://localhost:5000
```

## 🧠 Solving Techniques

The solver implements these techniques with detailed explanations:

### 1. Single Candidate (Naked Single)
When a cell has only one possible candidate number.

### 2. Single Position (Hidden Single)  
When a number can only go in one position within a row, column, or 3x3 box.

### 3. Candidate Lines (Pointing Pairs/Triples)
When all candidates for a number in a box are aligned in the same row or column, that number can be eliminated from other cells in that row or column outside the box.

### 4. Double Pairs (Naked Pairs)
When two cells in the same row, column, or box contain the same two candidates, those candidates can be eliminated from other cells in that unit.

## 📁 Project Structure

```
sudoku-solver-with-explanations/
├── file_solver.py        # 🎯 Main file-based solver (RECOMMENDED)
├── sudoku_solver.py      # Core solving logic
├── cli_solver.py         # Interactive command-line interface
├── simple_cli.py         # Simple demo CLI
├── app.py               # Flask web application
├── templates/
│   └── index.html       # Web interface
├── requirements.txt      # Python dependencies
├── puzzle.txt           # Sample puzzle file
└── README.md           # This file
```

## 📊 Example Output

The file solver provides detailed output like this:

```
Step 5: Candidate Lines
Action: Remove 3 from row 1 outside box
Cell: (1, 4)
Value: 0
Explanation: Number 3 in box 2 can only be placed in row 1 (cells (1,4) and (1,5)). 
Since this number must go in row 1, it cannot appear anywhere else in that row outside the box. 
This eliminates 3 from other cells in row 1.

Board after this step:
   A B C | D E F | G H I
  -------+-------+-------
1 2 . 7 | . . 9 | . . . 
2 5 . . | 8 2 7 | 3 4 . 
3 4 . . | 1 6 5 | 7 . 2 
  -------+-------+-------
4 . . . | 9 . . | 8 . . 
5 6 . . | 5 7 8 | . . . 
6 8 . . | 6 . . | . . 3 
  -------+-------+-------
7 . . . | . 8 1 | . . 4 
8 . . 8 | . 5 6 | . 2 . 
9 1 5 . | 2 9 . | 6 . . 

Candidates removed:
  - Removed 3 from cell (1,7)
  - Removed 3 from cell (1,8)
  - Removed 3 from cell (1,9)
```

## 🔧 Programmatic Usage

```python
from sudoku_solver import SudokuSolver

# Create a puzzle (0 represents empty cells)
puzzle = [
    [5,3,0,0,7,0,0,0,0],
    [6,0,0,1,9,5,0,0,0],
    [0,9,8,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3],
    [4,0,0,8,0,3,0,0,1],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,4,1,9,0,0,5],
    [0,0,0,0,8,0,0,7,9]
]

# Create solver and solve
solver = SudokuSolver(puzzle)
steps = solver.solve_step_by_step()

# Print explanations
for i, step in enumerate(steps, 1):
    print(f"Step {i}: {step.technique.value}")
    print(f"Action: {step.description}")
    print(f"Explanation: {step.explanation}")
    print()
```

## 🤝 Contributing

Feel free to contribute by:
- Adding more advanced solving techniques
- Improving the explanations
- Adding unit tests
- Enhancing the file solver features

## 📄 License

This project is open source and available under the MIT License. 