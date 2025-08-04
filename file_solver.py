#!/usr/bin/env python3
"""
File-based Sudoku solver CLI
Reads Sudoku puzzles from files and outputs complete solutions with explanations
"""

from sudoku_solver import SudokuSolver
import sys
import argparse
import os

def print_board(board):
    """Print the Sudoku board in a readable format"""
    output = []
    output.append("   A B C | D E F | G H I")
    output.append("  -------+-------+-------")
    for i, row in enumerate(board):
        row_str = f"{i+1} "
        for j, cell in enumerate(row):
            if j % 3 == 0 and j != 0:
                row_str += "| "
            row_str += str(cell) if cell != 0 else "."
            row_str += " "
        output.append(row_str)
        if (i + 1) % 3 == 0 and i != 8:
            output.append("  -------+-------+-------")
    return output

def print_board_with_highlight(board, highlight_row, highlight_col, highlight_value):
    """Print the Sudoku board with color coding and highlighting"""
    output = []
    output.append("   A B C | D E F | G H I")
    output.append("  -------+-------+-------")
    
    for i, row in enumerate(board):
        row_str = f"{i+1} "
        for j, cell in enumerate(row):
            if j % 3 == 0 and j != 0:
                row_str += "| "
            
            # Color coding and highlighting
            if i == highlight_row and j == highlight_col:
                # Highlight the newly placed number
                row_str += f"[{highlight_value}]"  # Bracketed for emphasis
            elif cell != 0:
                # Original numbers
                row_str += str(cell)
            else:
                # Empty cells as dots
                row_str += "."
            
            row_str += " "
        output.append(row_str)
        if (i + 1) % 3 == 0 and i != 8:
            output.append("  -------+-------+-------")
    
    # Add legend
    output.append("")
    output.append("Legend:")
    output.append("  [X] = Just placed")
    output.append("  Numbers = Original numbers")
    output.append("  . = Empty cells")
    
    return output

def parse_sudoku_file(file_path):
    """Parse Sudoku puzzle from file"""
    board = [[0] * 9 for _ in range(9)]
    
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # Remove empty lines and strip whitespace
        lines = [line.strip() for line in lines if line.strip()]
        
        for i, line in enumerate(lines[:9]):
            if i >= 9:
                break
            
            # Handle different input formats
            if len(line) == 9:
                # Single line format: "530070000"
                for j, char in enumerate(line[:9]):
                    if char.isdigit():
                        board[i][j] = int(char)
            else:
                # Space-separated format: "5 3 0 0 7 0 0 0 0"
                numbers = line.split()
                for j, num in enumerate(numbers[:9]):
                    if num.isdigit():
                        board[i][j] = int(num)
        
        return board
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        sys.exit(1)

def solve_and_generate_output(board, output_file=None):
    """Solve the puzzle and generate output"""
    output_lines = []
    
    output_lines.append("=== Sudoku Solver with Step-by-Step Explanations ===")
    output_lines.append("")
    
    output_lines.append("Original Puzzle:")
    output_lines.extend(print_board(board))
    output_lines.append("")
    
    # Create solver and solve
    solver = SudokuSolver(board)
    
    if not solver.is_valid_board():
        output_lines.append("Error: Invalid Sudoku puzzle!")
        return output_lines
    
    output_lines.append("Solving puzzle...")
    steps = solver.solve_step_by_step()
    
    if not steps:
        output_lines.append("No solving steps found. The puzzle might be unsolvable or require advanced techniques.")
        return output_lines
    
    output_lines.append(f"\nFound {len(steps)} solving steps:")
    output_lines.append("=" * 60)
    
    # Show all steps with explanations
    current_board = [row[:] for row in board]  # Copy the original board
    
    for i in range(len(steps)):
        step = steps[i]
        output_lines.append(f"\nStep {i+1}: {step.technique.value}")
        output_lines.append(f"Action: {step.description}")
        output_lines.append(f"Cell: ({step.row+1}, {step.col+1})")
        output_lines.append(f"Value: {step.value}")
        output_lines.append(f"Explanation: {step.explanation}")
        
        # Apply the step to show current board state (only if a number is being placed)
        if step.value != 0:
            current_board[step.row][step.col] = step.value
        
        # Show current board state after this step
        output_lines.append("\nBoard after this step:")
        if step.value != 0:
            output_lines.extend(print_board_with_highlight(current_board, step.row, step.col, step.value))
        else:
            output_lines.extend(print_board(current_board))
        
        if step.candidates_removed:
            output_lines.append(f"Candidates removed:")
            for row, col, val in step.candidates_removed:
                output_lines.append(f"  - Removed {val} from cell ({row+1},{col+1})")
        
        if step.cells_involved:
            output_lines.append(f"Cells involved: {step.cells_involved}")
        
        # Add visual reasoning for Candidate Lines technique
        if step.technique.value == "Candidate Lines":
            output_lines.append("")
            output_lines.append("Visual Reasoning:")
            output_lines.append("  The number is constrained to a specific row/column within a box")
            output_lines.append("  This means it cannot appear elsewhere in that row/column")
        
        output_lines.append("-" * 60)
    
    output_lines.append("\nPuzzle solved!")
    output_lines.append(f"\nFinal Solution:")
    output_lines.extend(print_board(current_board))
    output_lines.append(f"Puzzle solved: {solver._is_solved()}")
    output_lines.append(f"Board valid: {solver.is_valid_board()}")
    
    return output_lines

def solve_step_by_step_with_output(board):
    """Solve the puzzle step by step and generate output"""
    output_lines = []
    
    output_lines.append("=== Sudoku Solver with Step-by-Step Explanations ===")
    output_lines.append("")
    
    output_lines.append("Original Puzzle:")
    output_lines.extend(print_board(board))
    output_lines.append("")
    
    # Create solver and solve step by step
    solver = SudokuSolver(board)
    
    if not solver.is_valid_board():
        output_lines.append("Error: Invalid Sudoku puzzle!")
        return output_lines
    
    output_lines.append("Solving puzzle...")
    
    current_board = [row[:] for row in board]  # Copy the original board
    step_count = 0
    
    while not solver._is_solved():
        step = solver._find_next_step()
        if step is None:
            output_lines.append("No more steps found. Puzzle might be unsolvable or need advanced techniques.")
            break
        
        step_count += 1
        output_lines.append(f"\nStep {step_count}: {step.technique.value}")
        output_lines.append(f"Action: {step.description}")
        output_lines.append(f"Cell: ({step.row+1}, {step.col+1})")
        output_lines.append(f"Value: {step.value}")
        output_lines.append(f"Explanation: {step.explanation}")
        
        # Apply the step to show current board state (only if a number is being placed)
        if step.value != 0:
            current_board[step.row][step.col] = step.value
        
        # Show current board state after this step
        output_lines.append("\nBoard after this step:")
        if step.value != 0:
            output_lines.extend(print_board_with_highlight(current_board, step.row, step.col, step.value))
        else:
            output_lines.extend(print_board(current_board))
        
        if step.candidates_removed:
            output_lines.append(f"Candidates removed:")
            for row, col, val in step.candidates_removed:
                output_lines.append(f"  - Removed {val} from cell ({row+1},{col+1})")
        
        if step.cells_involved:
            output_lines.append(f"Cells involved: {step.cells_involved}")
        
        # Add visual reasoning for Candidate Lines technique
        if step.technique.value == "Candidate Lines":
            output_lines.append("")
            output_lines.append("Visual Reasoning:")
            output_lines.append("  The number is constrained to a specific row/column within a box")
            output_lines.append("  This means it cannot appear elsewhere in that row/column")
        
        output_lines.append("-" * 60)
        
        # Apply the step to the solver
        solver.board[step.row][step.col] = step.value
        solver._remove_candidate_from_peers(step.row, step.col, step.value)
    
    output_lines.append(f"\nPuzzle solved!")
    output_lines.append(f"\nFinal Solution:")
    output_lines.extend(print_board(current_board))
    output_lines.append(f"Puzzle solved: {solver._is_solved()}")
    output_lines.append(f"Board valid: {solver.is_valid_board()}")
    
    return output_lines

def create_sample_file(filename):
    """Create a sample Sudoku file"""
    sample_content = """5 3 0 0 7 0 0 0 0
6 0 0 1 9 5 0 0 0
0 9 8 0 0 0 0 6 0
8 0 0 0 6 0 0 0 3
4 0 0 8 0 3 0 0 1
7 0 0 0 2 0 0 0 6
0 6 0 0 0 0 2 8 0
0 0 0 4 1 9 0 0 5
0 0 0 0 8 0 0 7 9"""
    
    with open(filename, 'w') as f:
        f.write(sample_content)
    
    print(f"Sample Sudoku file created: {filename}")

def main():
    parser = argparse.ArgumentParser(
        description="Solve Sudoku puzzles from files with step-by-step explanations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python file_solver.py puzzle.txt                    # Solve puzzle.txt and save to puzzle_solution.txt
  python file_solver.py puzzle.txt -o custom.txt      # Solve puzzle.txt and save to custom.txt
  python file_solver.py --create-sample sample.txt    # Create a sample puzzle file
  python file_solver.py puzzle.txt -v                 # Verbose output to console and auto-generated file

Input file format (9 lines, each with 9 numbers):
  5 3 0 0 7 0 0 0 0
  6 0 0 1 9 5 0 0 0
  0 9 8 0 0 0 0 6 0
  8 0 0 0 6 0 0 0 3
  4 0 0 8 0 3 0 0 1
  7 0 0 0 2 0 0 0 6
  0 6 0 0 0 0 2 8 0
  0 0 0 4 1 9 0 0 5
  0 0 0 0 8 0 0 7 9

Or single line format:
  530070000
  600195000
  098000060
  800060003
  400803001
  700020006
  060000280
  000419005
  000080079
        """
    )
    
    parser.add_argument('input_file', nargs='?', help='Input Sudoku file')
    parser.add_argument('-o', '--output', help='Output file for solution (default: inputfile_solution.txt)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Also print to console')
    parser.add_argument('--create-sample', help='Create a sample Sudoku file')
    
    args = parser.parse_args()
    
    # Handle create sample option
    if args.create_sample:
        create_sample_file(args.create_sample)
        return
    
    # Check if input file is provided
    if not args.input_file:
        parser.print_help()
        print("\nError: Input file is required.")
        print("Use --create-sample filename to create a sample puzzle file.")
        sys.exit(1)
    
    # Parse the Sudoku puzzle
    board = parse_sudoku_file(args.input_file)
    
    # Solve step by step and generate output
    output_lines = solve_step_by_step_with_output(board)
    
    # Generate output filename if not specified
    if not args.output:
        # Get the base name without extension
        base_name = os.path.splitext(args.input_file)[0]
        args.output = f"{base_name}_solution.txt"
    
    # Write to output file
    try:
        with open(args.output, 'w') as f:
            f.write('\n'.join(output_lines))
        print(f"Solution written to: {args.output}")
    except Exception as e:
        print(f"Error writing to output file: {e}")
        sys.exit(1)
    
    # Print to console if verbose
    if args.verbose:
        print('\n'.join(output_lines))

if __name__ == "__main__":
    main() 