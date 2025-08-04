#!/usr/bin/env python3
"""
Command-line interface for the Sudoku solver
"""

from sudoku_solver import SudokuSolver
import sys

def print_board(board):
    """Print the Sudoku board in a readable format"""
    print("   A B C | D E F | G H I")
    print("  -------+-------+-------")
    for i, row in enumerate(board):
        row_str = f"{i+1} "
        for j, cell in enumerate(row):
            if j % 3 == 0 and j != 0:
                row_str += "| "
            row_str += str(cell) if cell != 0 else "."
            row_str += " "
        print(row_str)
        if (i + 1) % 3 == 0 and i != 8:
            print("  -------+-------+-------")

def parse_input(input_str):
    """Parse input string into board format"""
    board = [[0] * 9 for _ in range(9)]
    lines = input_str.strip().split('\n')
    
    for i, line in enumerate(lines[:9]):
        if i >= 9:
            break
        for j, char in enumerate(line[:9]):
            if char.isdigit() and char != '0':
                board[i][j] = int(char)
    
    return board

def get_sample_puzzle():
    """Return a sample puzzle"""
    return [
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

def main():
    print("=== Sudoku Solver with Explanations ===")
    print()
    
    # Get puzzle input
    print("Enter your Sudoku puzzle (use 0 or . for empty cells):")
    print("You can enter 9 lines of 9 characters each, or type 'sample' for a demo puzzle")
    print("Example:")
    print("530070000")
    print("600195000")
    print("098000060")
    print("...")
    print()
    
    input_text = ""
    try:
        while True:
            line = input("Enter line (or 'sample' for demo): ").strip()
            if line.lower() == 'sample':
                board = get_sample_puzzle()
                break
            elif len(line) == 9 and all(c.isdigit() or c == '.' for c in line):
                input_text += line + '\n'
                if len(input_text.split('\n')) >= 10:  # 9 lines + empty line
                    board = parse_input(input_text)
                    break
            else:
                print("Invalid input. Please enter 9 digits (0-9) or dots (.) per line.")
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    
    print("\nOriginal Puzzle:")
    print_board(board)
    print()
    
    # Create solver and solve
    solver = SudokuSolver(board)
    
    if not solver.is_valid_board():
        print("Error: Invalid Sudoku puzzle!")
        return
    
    print("Solving puzzle...")
    steps = solver.solve_step_by_step()
    
    if not steps:
        print("No solving steps found. The puzzle might be unsolvable or require advanced techniques.")
        return
    
    print(f"\nFound {len(steps)} solving steps:")
    print("=" * 60)
    
    # Show all steps with explanations
    print(f"\nSolving Steps:")
    print("=" * 60)
    
    # Create a fresh solver to track board state
    step_solver = SudokuSolver(board)
    
    for i, step in enumerate(steps, 1):
        print(f"\nStep {i}: {step.technique.value}")
        print(f"Action: {step.description}")
        print(f"Cell: ({step.row+1}, {step.col+1})")
        print(f"Value: {step.value}")
        print(f"Explanation: {step.explanation}")
        
        # Apply the step to show current board state
        step_solver.board[step.row][step.col] = step.value
        step_solver._remove_candidate_from_peers(step.row, step.col, step.value)
        
        # Show current board state after this step
        print("\nBoard after this step:")
        print_board(step_solver.board)
        
        if step.candidates_removed:
            print(f"Candidates removed: {step.candidates_removed}")
        
        if step.cells_involved:
            print(f"Cells involved: {step.cells_involved}")
        
        print("-" * 60)
    
    print("\nPuzzle solved!")
    
    print(f"\nFinal Solution:")
    print_board(solver.board)
    print(f"Puzzle solved: {solver._is_solved()}")
    print(f"Board valid: {solver.is_valid_board()}")

if __name__ == "__main__":
    main() 