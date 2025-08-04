#!/usr/bin/env python3
"""
Simple CLI version that automatically solves the sample puzzle
"""

from sudoku_solver import SudokuSolver

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

def main():
    print("=== Sudoku Solver with Step-by-Step Explanations ===")
    print()
    
    # Sample puzzle
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
    step_solver = SudokuSolver(puzzle)
    
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
    print_board(step_solver.board)
    print(f"Puzzle solved: {step_solver._is_solved()}")
    print(f"Board valid: {step_solver.is_valid_board()}")

if __name__ == "__main__":
    main() 