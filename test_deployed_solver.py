#!/usr/bin/env python3
"""
Test script to debug the solver issue
"""

from sudoku_solver import SudokuSolver
import json

def test_puzzle_debug():
    """Test the puzzle and show detailed debugging info"""
    
    # The puzzle mentioned by the user
    puzzle = """207009000
500827340
400165702
000900800
600570000
000600003
000000004
008056020
150290600"""
    
    print("Testing puzzle:")
    print(puzzle)
    print("\n" + "="*50)
    
    # Parse the puzzle
    board = []
    for line in puzzle.strip().split('\n'):
        row = [int(c) if c != '0' else 0 for c in line.strip()]
        board.append(row)
    
    print("Parsed board:")
    for i, row in enumerate(board):
        print(f"Row {i+1}: {row}")
    
    print("\n" + "="*50)
    
    # Create solver
    solver = SudokuSolver(board)
    print(f"Board valid: {solver.is_valid_board()}")
    
    # Show initial candidates
    print("\nInitial candidates for empty cells:")
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                print(f"({i+1},{j+1}): {solver.candidates[i][j]}")
    
    print("\n" + "="*50)
    print("Solving step by step...")
    
    # Solve step by step
    steps = solver.solve_step_by_step()
    
    print(f"\nTotal steps found: {len(steps)}")
    print(f"Solved: {solver._is_solved()}")
    
    # Show final board
    print("\nFinal board:")
    for i, row in enumerate(solver.board):
        print(f"Row {i+1}: {row}")
    
    # Show remaining empty cells and their candidates
    empty_cells = []
    for i in range(9):
        for j in range(9):
            if solver.board[i][j] == 0:
                candidates = solver.candidates[i][j]
                if len(candidates) == 0:
                    empty_cells.append(f"({i+1},{j+1}) - NO CANDIDATES!")
                else:
                    empty_cells.append(f"({i+1},{j+1}) - candidates: {candidates}")
    
    if empty_cells:
        print(f"\n⚠️  Empty cells remaining: {len(empty_cells)}")
        for cell in empty_cells:
            print(f"  {cell}")
    else:
        print("\n✅ All cells filled successfully!")
    
    # Show first few steps in detail
    print(f"\nFirst 10 steps:")
    for i, step in enumerate(steps[:10]):
        print(f"Step {i+1}: {step.technique.value} - {step.description}")
        print(f"  Cell: ({step.row+1},{step.col+1}), Value: {step.value}")
        if step.candidates_removed:
            print(f"  Candidates removed: {step.candidates_removed}")
    
    if len(steps) > 10:
        print(f"... and {len(steps) - 10} more steps")
    
    return len(steps), solver._is_solved()

if __name__ == "__main__":
    steps, solved = test_puzzle_debug()
    print(f"\n{'='*50}")
    print(f"SUMMARY: {steps} steps, Solved: {solved}")
    print(f"{'='*50}")
