#!/usr/bin/env python3
"""
Test script for the Sudoku solver
"""

from sudoku_solver import SudokuSolver

def test_solver():
    # Test puzzle (0 represents empty cells)
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
    
    print("Original Puzzle:")
    print_board(puzzle)
    print()
    
    # Create solver and solve
    solver = SudokuSolver(puzzle)
    steps = solver.solve_step_by_step()
    
    print(f"Found {len(steps)} solving steps:")
    print("=" * 50)
    
    for i, step in enumerate(steps, 1):
        print(f"Step {i}: {step.technique.value}")
        print(f"Action: {step.description}")
        print(f"Cell: ({step.row+1}, {step.col+1})")
        print(f"Value: {step.value}")
        print(f"Explanation: {step.explanation}")
        
        if step.candidates_removed:
            print(f"Candidates removed: {step.candidates_removed}")
        
        if step.cells_involved:
            print(f"Cells involved: {step.cells_involved}")
        
        print("-" * 30)
    
    print("\nFinal Solution:")
    print_board(solver.board)
    print(f"Puzzle solved: {solver._is_solved()}")
    print(f"Board valid: {solver.is_valid_board()}")

def print_board(board):
    """Print the Sudoku board in a readable format"""
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        
        row_str = ""
        for j, cell in enumerate(row):
            if j % 3 == 0 and j != 0:
                row_str += "| "
            row_str += str(cell) if cell != 0 else "."
            row_str += " "
        
        print(row_str)

if __name__ == "__main__":
    test_solver() 