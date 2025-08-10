from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from sudoku_solver import SudokuSolver
import json
import traceback
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/version')
def version():
    """Return version information for debugging"""
    return jsonify({
        'version': '1.2.1',
        'solver_updated': True,
        'cache_busting': True,
        'timestamp': '2025-08-10T19:00:00Z'
    })

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400
            
        board = data.get('board', [])
        
        # Validate board format
        if len(board) != 9 or any(len(row) != 9 for row in board):
            return jsonify({'error': 'Invalid board format'}), 400
        
        # Create solver and solve
        solver = SudokuSolver(board)
        
        if not solver.is_valid_board():
            return jsonify({'error': 'Invalid Sudoku puzzle'}), 400
        
        steps = solver.solve_step_by_step()
        
        # Convert steps to serializable format
        serialized_steps = []
        for step in steps:
            step_dict = {
                'technique': step.technique.value,
                'description': step.description,
                'row': step.row,
                'col': step.col,
                'value': step.value,
                'explanation': step.explanation,
                'candidates_removed': step.candidates_removed or [],
                'cells_involved': step.cells_involved or []
            }
            serialized_steps.append(step_dict)
        
        response = jsonify({
            'steps': serialized_steps,
            'final_board': solver.board,
            'is_solved': solver._is_solved()
        })
        
        # Add cache-busting headers to prevent CDN caching
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        response.headers['X-Solver-Version'] = '1.2.1'  # Version identifier
        
        return response
    except Exception as e:
        print(f"Error in solve endpoint: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/step', methods=['POST'])
def solve_step():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400
            
        board = data.get('board', [])
        step_index = data.get('step_index', 0)
        
        solver = SudokuSolver(board)
        
        if not solver.is_valid_board():
            return jsonify({'error': 'Invalid Sudoku puzzle'}), 400
        
        # Solve up to the requested step
        steps = []
        for i in range(step_index + 1):
            step = solver._find_next_step()
            if step is None:
                break
            
            # Apply the step
            solver.board[step.row][step.col] = step.value
            solver._remove_candidate_from_peers(step.row, step.col, step.value)
            steps.append(step)
        
        if step_index < len(steps):
            current_step = steps[step_index]
            step_dict = {
                'technique': current_step.technique.value,
                'description': current_step.description,
                'row': current_step.row,
                'col': current_step.col,
                'value': current_step.value,
                'explanation': current_step.explanation,
                'candidates_removed': current_step.candidates_removed or [],
                'cells_involved': current_step.cells_involved or []
            }
        else:
            step_dict = None
        
        return jsonify({
            'current_step': step_dict,
            'board': solver.board,
            'candidates': solver.candidates,
            'total_steps': len(steps)
        })
    except Exception as e:
        print(f"Error in step endpoint: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port) 