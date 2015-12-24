__author__ = 'william'


class SudokuStep:

    def __init__(self, filled_cell, updated_cells, reason):
        # A (cell_name, val) tuple set by this method
        self.filled_cell = filled_cell
        # A set of (cell name, removed possibility) tuples for the cells with possibilities removed
        self.updated_cells = updated_cells
        # The reason the cell was filled/possibilities could be eliminated
        self.reason = reason

    def to_json(self):
        return {
            'filled_cell': self.filled_cell,
            'updated_cells': self.updated_cells,
            'reason': self.reason
        }
