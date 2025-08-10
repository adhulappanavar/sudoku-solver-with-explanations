import copy
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum

class SolvingTechnique(Enum):
    SINGLE_CANDIDATE = "Single Candidate"
    SINGLE_POSITION = "Single Position"
    CANDIDATE_LINES = "Candidate Lines"
    DOUBLE_PAIRS = "Double Pairs"
    TRIPLE_PAIRS = "Triple Pairs"
    HIDDEN_PAIRS = "Hidden Pairs"
    HIDDEN_TRIPLES = "Hidden Triples"
    X_WING = "X-Wing"
    SWORDFISH = "Swordfish"
    XY_WING = "XY-Wing"
    XYZ_WING = "XYZ-Wing"

@dataclass
class SolvingStep:
    technique: SolvingTechnique
    description: str
    row: int
    col: int
    value: int
    explanation: str
    candidates_removed: List[Tuple[int, int, int]] = None  # (row, col, value)
    cells_involved: List[Tuple[int, int]] = None  # (row, col)

class SudokuSolver:
    def __init__(self, board: List[List[int]] = None):
        self.board = board if board else [[0] * 9 for _ in range(9)]
        self.solving_steps = []
        self.candidates = self._initialize_candidates()
        if board:
            self._update_candidates_from_board()
    
    def _initialize_candidates(self) -> List[List[List[int]]]:
        """Initialize candidate lists for each cell"""
        candidates = []
        for i in range(9):
            row = []
            for j in range(9):
                if self.board[i][j] == 0:
                    # Start with all numbers 1-9 as candidates
                    row.append(list(range(1, 10)))
                else:
                    row.append([])
            candidates.append(row)
        return candidates
    
    def load_board(self, board: List[List[int]]):
        """Load a new board and reset solver state"""
        self.board = copy.deepcopy(board)
        self.solving_steps = []
        self.candidates = self._initialize_candidates()
        self._update_candidates_from_board()
    
    def _update_candidates_from_board(self):
        """Update candidates based on current board state"""
        # First, reset all candidates
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    self.candidates[i][j] = list(range(1, 10))
                else:
                    self.candidates[i][j] = []
        
        # Then remove candidates based on filled cells
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    # Remove this value from candidates in same row, col, and box
                    value = self.board[i][j]
                    self._remove_candidate_from_peers(i, j, value)
    
    def _remove_candidate_from_peers(self, row: int, col: int, value: int):
        """Remove a candidate value from all peer cells"""
        # Remove from same row
        for c in range(9):
            if c != col and self.board[row][c] == 0 and value in self.candidates[row][c]:
                self.candidates[row][c].remove(value)
        
        # Remove from same column
        for r in range(9):
            if r != row and self.board[r][col] == 0 and value in self.candidates[r][col]:
                self.candidates[r][col].remove(value)
        
        # Remove from same 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if (r != row or c != col) and self.board[r][c] == 0 and value in self.candidates[r][c]:
                    self.candidates[r][c].remove(value)
    
    def _validate_candidates(self) -> bool:
        """Check if all empty cells have at least one candidate"""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0 and len(self.candidates[i][j]) == 0:
                    return False
        return True
    
    def solve_step_by_step(self) -> List[SolvingStep]:
        """Solve the puzzle step by step, returning explanations"""
        self.solving_steps = []
        max_iterations = 200  # Prevent infinite loops
        iteration = 0
        
        while not self._is_solved() and iteration < max_iterations:
            iteration += 1
            
            # Always try simple techniques first after each step
            step = self._find_single_candidate()
            if step:
                self._apply_step(step)
                continue
            
            step = self._find_single_position()
            if step:
                self._apply_step(step)
                continue
            
            # Try hidden singles (more advanced than single position)
            step = self._find_hidden_single()
            if step:
                self._apply_step(step)
                continue
            
            # Try advanced techniques only if they don't break the puzzle
            step = self._find_candidate_lines_safe()
            if step:
                self._apply_step(step)
                # After candidate removal, immediately check for new single candidates
                step = self._find_any_single_candidate()
                if step:
                    self._apply_step(step)
                continue
            
            step = self._find_double_pairs_safe()
            if step:
                self._apply_step(step)
                # After candidate removal, immediately check for new single candidates
                step = self._find_any_single_candidate()
                if step:
                    self._apply_step(step)
                continue
            
            # Try X-Wing technique for harder puzzles
            step = self._find_x_wing()
            if step:
                self._apply_step(step)
                # After candidate removal, immediately check for new single candidates
                step = self._find_any_single_candidate()
                if step:
                    self._apply_step(step)
                continue
            
            # If no step found, try to find any remaining single candidates
            # This catches cases where advanced techniques created new single candidates
            step = self._find_any_single_candidate()
            if step:
                self._apply_step(step)
                continue
            
            # No more steps found
            break
        
        if iteration >= max_iterations:
            print(f"Warning: Solver stopped after {max_iterations} iterations")
        
        return self.solving_steps
    
    def _apply_step(self, step: SolvingStep):
        """Apply a solving step and update the board state"""
        if step.value != 0:  # Place numbers
            self.board[step.row][step.col] = step.value
            self._remove_candidate_from_peers(step.row, step.col, step.value)
        # For candidate removal steps (step.value == 0), candidates are already removed
        # in the _find_candidate_lines_safe and _find_double_pairs_safe methods
        
        self.solving_steps.append(step)
    
    def _find_any_single_candidate(self) -> Optional[SolvingStep]:
        """Find any cell with only one candidate, even if it was missed before"""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0 and len(self.candidates[i][j]) == 1:
                    value = self.candidates[i][j][0]
                    explanation = f"Cell ({i+1},{j+1}) has only one possible candidate: {value}"
                    return SolvingStep(
                        technique=SolvingTechnique.SINGLE_CANDIDATE,
                        description=f"Place {value} in cell ({i+1},{j+1})",
                        row=i, col=j, value=value,
                        explanation=explanation
                    )
        return None
    
    def _is_solved(self) -> bool:
        """Check if the puzzle is solved"""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return False
        return True
    
    def _find_single_candidate(self) -> Optional[SolvingStep]:
        """Find cells with only one candidate (naked single)"""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0 and len(self.candidates[i][j]) == 1:
                    value = self.candidates[i][j][0]
                    explanation = f"Cell ({i+1},{j+1}) has only one possible candidate: {value}"
                    return SolvingStep(
                        technique=SolvingTechnique.SINGLE_CANDIDATE,
                        description=f"Place {value} in cell ({i+1},{j+1})",
                        row=i, col=j, value=value,
                        explanation=explanation
                    )
        return None
    
    def _find_single_position(self) -> Optional[SolvingStep]:
        """Find numbers that can only go in one position in a row/col/box (hidden single)"""
        # Check rows
        for i in range(9):
            for value in range(1, 10):
                positions = []
                for j in range(9):
                    if self.board[i][j] == 0 and value in self.candidates[i][j]:
                        positions.append(j)
                if len(positions) == 1:
                    j = positions[0]
                    explanation = f"Number {value} can only go in position ({i+1},{j+1}) in row {i+1}"
                    return SolvingStep(
                        technique=SolvingTechnique.SINGLE_POSITION,
                        description=f"Place {value} in cell ({i+1},{j+1})",
                        row=i, col=j, value=value,
                        explanation=explanation
                    )
        
        # Check columns
        for j in range(9):
            for value in range(1, 10):
                positions = []
                for i in range(9):
                    if self.board[i][j] == 0 and value in self.candidates[i][j]:
                        positions.append(i)
                if len(positions) == 1:
                    i = positions[0]
                    explanation = f"Number {value} can only go in position ({i+1},{j+1}) in column {j+1}"
                    return SolvingStep(
                        technique=SolvingTechnique.SINGLE_POSITION,
                        description=f"Place {value} in cell ({i+1},{j+1})",
                        row=i, col=j, value=value,
                        explanation=explanation
                    )
        
        # Check 3x3 boxes
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                for value in range(1, 10):
                    positions = []
                    for i in range(box_row, box_row + 3):
                        for j in range(box_col, box_col + 3):
                            if self.board[i][j] == 0 and value in self.candidates[i][j]:
                                positions.append((i, j))
                    if len(positions) == 1:
                        i, j = positions[0]
                        box_num = (box_row // 3) * 3 + (box_col // 3) + 1
                        explanation = f"Number {value} can only go in position ({i+1},{j+1}) in box {box_num}"
                        return SolvingStep(
                            technique=SolvingTechnique.SINGLE_POSITION,
                            description=f"Place {value} in cell ({i+1},{j+1})",
                            row=i, col=j, value=value,
                            explanation=explanation
                        )
        return None
    
    def _find_hidden_single(self) -> Optional[SolvingStep]:
        """Find hidden singles - numbers that can only go in one position in a row/col/box"""
        # Check rows for hidden singles
        for i in range(9):
            for value in range(1, 10):
                positions = []
                for j in range(9):
                    if self.board[i][j] == 0 and value in self.candidates[i][j]:
                        positions.append(j)
                
                if len(positions) == 1:
                    # Found a hidden single
                    col = positions[0]
                    explanation = f"Number {value} can only be placed in row {i+1} at position ({i+1},{col+1}) - it's the only cell in that row that can contain {value}"
                    return SolvingStep(
                        technique=SolvingTechnique.SINGLE_POSITION,
                        description=f"Place {value} in cell ({i+1},{col+1}) - hidden single in row",
                        row=i, col=col, value=value,
                        explanation=explanation
                    )
        
        # Check columns for hidden singles
        for j in range(9):
            for value in range(1, 10):
                positions = []
                for i in range(9):
                    if self.board[i][j] == 0 and value in self.candidates[i][j]:
                        positions.append(i)
                
                if len(positions) == 1:
                    # Found a hidden single
                    row = positions[0]
                    explanation = f"Number {value} can only be placed in column {j+1} at position ({row+1},{j+1}) - it's the only cell in that column that can contain {value}"
                    return SolvingStep(
                        technique=SolvingTechnique.SINGLE_POSITION,
                        description=f"Place {value} in cell ({row+1},{j+1}) - hidden single in column",
                        row=row, col=j, value=value,
                        explanation=explanation
                    )
        
        # Check 3x3 boxes for hidden singles
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                for value in range(1, 10):
                    positions = []
                    for i in range(box_row, box_row + 3):
                        for j in range(box_col, box_col + 3):
                            if self.board[i][j] == 0 and value in self.candidates[i][j]:
                                positions.append((i, j))
                    
                    if len(positions) == 1:
                        # Found a hidden single
                        row, col = positions[0]
                        box_num = (box_row // 3) * 3 + (box_col // 3) + 1
                        explanation = f"Number {value} can only be placed in box {box_num} at position ({row+1},{col+1}) - it's the only cell in that box that can contain {value}"
                        return SolvingStep(
                            technique=SolvingTechnique.SINGLE_POSITION,
                            description=f"Place {value} in cell ({row+1},{col+1}) - hidden single in box {box_num}",
                            row=row, col=col, value=value,
                            explanation=explanation
                        )
        
        return None
    
    def _find_candidate_lines_safe(self) -> Optional[SolvingStep]:
        """Find candidate lines (pointing pairs/triples) with safety checks"""
        # Check each box for candidate lines
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                for value in range(1, 10):
                    # Find all positions of this value in the box
                    positions = []
                    for i in range(box_row, box_row + 3):
                        for j in range(box_col, box_col + 3):
                            if self.board[i][j] == 0 and value in self.candidates[i][j]:
                                positions.append((i, j))
                    
                    if len(positions) >= 2:
                        # Check if all positions are in the same row or column
                        rows = set(pos[0] for pos in positions)
                        cols = set(pos[1] for pos in positions)
                        
                        if len(rows) == 1:
                            # All positions in same row - can remove value from rest of row
                            row = list(rows)[0]
                            removed = []
                            temp_candidates = copy.deepcopy(self.candidates)
                            
                            # Try the removal first
                            for j in range(9):
                                if j < box_col or j >= box_col + 3:  # Outside the box
                                    if self.board[row][j] == 0 and value in temp_candidates[row][j]:
                                        temp_candidates[row][j].remove(value)
                                        removed.append((row, j, value))
                            
                            # Check if this would make any cell have no candidates
                            if removed and self._validate_candidates_after_removal(temp_candidates, removed):
                                # Apply the removal
                                for row_idx, col_idx, val in removed:
                                    if val in self.candidates[row_idx][col_idx]:
                                        self.candidates[row_idx][col_idx].remove(val)
                                
                                box_num = (box_row // 3) * 3 + (box_col // 3) + 1
                                cell1 = f"({row+1},{box_col+1})"
                                cell2 = f"({row+1},{box_col+2})"
                                explanation = f"Number {value} in box {box_num} can only be placed in row {row+1} (cells {cell1} and {cell2}). Since this number must go in row {row+1}, it cannot appear anywhere else in that row outside the box. This eliminates {value} from other cells in row {row+1}."
                                return SolvingStep(
                                    technique=SolvingTechnique.CANDIDATE_LINES,
                                    description=f"Remove {value} from row {row+1} outside box",
                                    row=row, col=box_col, value=0,  # Don't place a number, just remove candidates
                                    explanation=explanation,
                                    candidates_removed=removed
                                )
                        
                        elif len(cols) == 1:
                            # All positions in same column - can remove value from rest of column
                            col = list(cols)[0]
                            removed = []
                            temp_candidates = copy.deepcopy(self.candidates)
                            
                            # Try the removal first
                            for i in range(9):
                                if i < box_row or i >= box_row + 3:  # Outside the box
                                    if self.board[i][col] == 0 and value in temp_candidates[i][col]:
                                        temp_candidates[i][col].remove(value)
                                        removed.append((i, col, value))
                            
                            # Check if this would make any cell have no candidates
                            if removed and self._validate_candidates_after_removal(temp_candidates, removed):
                                # Apply the removal
                                for row_idx, col_idx, val in removed:
                                    if val in self.candidates[row_idx][col_idx]:
                                        self.candidates[row_idx][col_idx].remove(val)
                                
                                box_num = (box_row // 3) * 3 + (box_col // 3) + 1
                                cell1 = f"({box_row+1},{col+1})"
                                cell2 = f"({box_row+2},{col+1})"
                                explanation = f"Number {value} in box {box_num} can only be placed in column {col+1} (cells {cell1} and {cell2}). Since this number must go in column {col+1}, it cannot appear anywhere else in that column outside the box. This eliminates {value} from other cells in column {col+1}."
                                return SolvingStep(
                                    technique=SolvingTechnique.CANDIDATE_LINES,
                                    description=f"Remove {value} from column {col+1} outside box",
                                    row=box_row, col=col, value=0,  # Don't place a number, just remove candidates
                                    explanation=explanation,
                                    candidates_removed=removed
                                )
        return None
    
    def _find_double_pairs_safe(self) -> Optional[SolvingStep]:
        """Find naked pairs (two cells with same two candidates) with safety checks"""
        # Check each row for naked pairs
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0 and len(self.candidates[i][j]) == 2:
                    pair = tuple(sorted(self.candidates[i][j]))
                    
                    # Check row for another cell with same pair
                    for k in range(9):
                        if k != j and self.board[i][k] == 0 and tuple(sorted(self.candidates[i][k])) == pair:
                            # Found a naked pair in row
                            removed = []
                            temp_candidates = copy.deepcopy(self.candidates)
                            
                            # Try the removal first
                            for l in range(9):
                                if l != j and l != k and self.board[i][l] == 0:
                                    for value in pair:
                                        if value in temp_candidates[i][l]:
                                            temp_candidates[i][l].remove(value)
                                            removed.append((i, l, value))
                            
                            # Check if this would make any cell have no candidates
                            if removed and self._validate_candidates_after_removal(temp_candidates, removed):
                                # Apply the removal
                                for row_idx, col_idx, val in removed:
                                    if val in self.candidates[row_idx][col_idx]:
                                        self.candidates[row_idx][col_idx].remove(val)
                                
                                explanation = f"Naked pair {pair} in row {i+1} - these numbers can't appear elsewhere in the row"
                                return SolvingStep(
                                    technique=SolvingTechnique.DOUBLE_PAIRS,
                                    description=f"Remove {pair} from other cells in row {i+1}",
                                    row=i, col=j, value=0,
                                    explanation=explanation,
                                    candidates_removed=removed,
                                    cells_involved=[(i, j), (i, k)]
                                )
        
        # Check columns for naked pairs
        for j in range(9):
            for i in range(9):
                if self.board[i][j] == 0 and len(self.candidates[i][j]) == 2:
                    pair = tuple(sorted(self.candidates[i][j]))
                    
                    # Check column for another cell with same pair
                    for k in range(9):
                        if k != i and self.board[k][j] == 0 and tuple(sorted(self.candidates[k][j])) == pair:
                            # Found a naked pair in column
                            removed = []
                            temp_candidates = copy.deepcopy(self.candidates)
                            
                            # Try the removal first
                            for l in range(9):
                                if l != i and l != k and self.board[l][j] == 0:
                                    for value in pair:
                                        if value in temp_candidates[l][j]:
                                            temp_candidates[l][j].remove(value)
                                            removed.append((l, j, value))
                            
                            # Check if this would make any cell have no candidates
                            if removed and self._validate_candidates_after_removal(temp_candidates, removed):
                                # Apply the removal
                                for row_idx, col_idx, val in removed:
                                    if val in self.candidates[row_idx][col_idx]:
                                        self.candidates[row_idx][col_idx].remove(val)
                                
                                explanation = f"Naked pair {pair} in column {j+1} - these numbers can't appear elsewhere in the column"
                                return SolvingStep(
                                    technique=SolvingTechnique.DOUBLE_PAIRS,
                                    description=f"Remove {pair} from other cells in column {j+1}",
                                    row=i, col=j, value=0,
                                    explanation=explanation,
                                    candidates_removed=removed,
                                    cells_involved=[(i, j), (k, j)]
                                )
        
        return None
    
    def _find_x_wing(self) -> Optional[SolvingStep]:
        """Find X-Wing patterns - when a number appears in exactly two positions in two rows/columns"""
        # Check for X-Wing in rows
        for value in range(1, 10):
            row_positions = {}
            for i in range(9):
                positions = []
                for j in range(9):
                    if self.board[i][j] == 0 and value in self.candidates[i][j]:
                        positions.append(j)
                if len(positions) == 2:
                    row_positions[i] = positions
            
            # Look for two rows with the same two column positions
            for row1 in row_positions:
                for row2 in row_positions:
                    if row1 < row2 and row_positions[row1] == row_positions[row2]:
                        # Found X-Wing pattern
                        cols = row_positions[row1]
                        removed = []
                        temp_candidates = copy.deepcopy(self.candidates)
                        
                        # Try removing the value from other cells in those columns
                        for col in cols:
                            for i in range(9):
                                if i != row1 and i != row2 and self.board[i][col] == 0:
                                    if value in temp_candidates[i][col]:
                                        temp_candidates[i][col].remove(value)
                                        removed.append((i, col, value))
                        
                        # Check if removal is safe
                        if removed and self._validate_candidates_after_removal(temp_candidates, removed):
                            # Apply the removal
                            for row_idx, col_idx, val in removed:
                                if val in self.candidates[row_idx][col_idx]:
                                    self.candidates[row_idx][col_idx].remove(val)
                            
                            explanation = f"X-Wing pattern found for number {value} in rows {row1+1} and {row2+1} at columns {[c+1 for c in cols]} - {value} can be removed from other cells in those columns"
                            return SolvingStep(
                                technique=SolvingTechnique.X_WING,
                                description=f"X-Wing: Remove {value} from columns {[c+1 for c in cols]} outside rows {row1+1},{row2+1}",
                                row=row1, col=cols[0], value=0,
                                explanation=explanation,
                                candidates_removed=removed,
                                cells_involved=[(row1, cols[0]), (row1, cols[1]), (row2, cols[0]), (row2, cols[1])]
                            )
        
        # Check for X-Wing in columns
        for value in range(1, 10):
            col_positions = {}
            for j in range(9):
                positions = []
                for i in range(9):
                    if self.board[i][j] == 0 and value in self.candidates[i][j]:
                        positions.append(i)
                if len(positions) == 2:
                    col_positions[j] = positions
            
            # Look for two columns with the same two row positions
            for col1 in col_positions:
                for col2 in col_positions:
                    if col1 < col2 and col_positions[col1] == col_positions[col2]:
                        # Found X-Wing pattern
                        rows = col_positions[col1]
                        removed = []
                        temp_candidates = copy.deepcopy(self.candidates)
                        
                        # Try removing the value from other cells in those rows
                        for row in rows:
                            for j in range(9):
                                if j != col1 and j != col2 and self.board[row][j] == 0:
                                    if value in temp_candidates[row][j]:
                                        temp_candidates[row][j].remove(value)
                                        removed.append((row, j, value))
                        
                        # Check if removal is safe
                        if removed and self._validate_candidates_after_removal(temp_candidates, removed):
                            # Apply the removal
                            for row_idx, col_idx, val in removed:
                                if val in self.candidates[row_idx][col_idx]:
                                    self.candidates[row_idx][col_idx].remove(val)
                            
                            explanation = f"X-Wing pattern found for number {value} in columns {col1+1} and {col2+1} at rows {[r+1 for r in rows]} - {value} can be removed from other cells in those rows"
                            return SolvingStep(
                                technique=SolvingTechnique.X_WING,
                                description=f"X-Wing: Remove {value} from rows {[r+1 for r in rows]} outside columns {col1+1},{col2+1}",
                                row=rows[0], col=col1, value=0,
                                explanation=explanation,
                                candidates_removed=removed,
                                cells_involved=[(rows[0], col1), (rows[0], col2), (rows[1], col1), (rows[1], col2)]
                            )
        
        return None
    
    def _validate_candidates_after_removal(self, temp_candidates: List[List[List[int]]], removed: List[Tuple[int, int, int]]) -> bool:
        """Check if removing candidates would leave any cell with no candidates"""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0 and len(temp_candidates[i][j]) == 0:
                    return False
        return True
    
    def get_board_state(self) -> Dict[str, Any]:
        """Get current board state for display"""
        return {
            'board': self.board,
            'candidates': self.candidates,
            'steps': [step.__dict__ for step in self.solving_steps]
        }
    
    def is_valid_board(self) -> bool:
        """Check if the current board is valid (no conflicts)"""
        # Check rows
        for i in range(9):
            row = [x for x in self.board[i] if x != 0]
            if len(row) != len(set(row)):
                return False
        
        # Check columns
        for j in range(9):
            col = [self.board[i][j] for i in range(9) if self.board[i][j] != 0]
            if len(col) != len(set(col)):
                return False
        
        # Check 3x3 boxes
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = []
                for i in range(box_row, box_row + 3):
                    for j in range(box_col, box_col + 3):
                        if self.board[i][j] != 0:
                            box.append(self.board[i][j])
                if len(box) != len(set(box)):
                    return False
        
        return True 