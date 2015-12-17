from transitions import Machine
from BadGuessError import BadGuessError
from SudokuLogger import SudokuLogger, SudokuStepLog
from SudokuPuzzle import SudokuPuzzle

__author__ = 'william'


class SudokuSolver(Machine):

    def __init__(self, sp):
        self.sudoku_puzzle = sp
        self.sudoku_logger = SudokuLogger()

        states = ['Ready', 'Sole_Candidate', 'Unique_Candidate', 'Naked_Pair', 'Block_RC_Interaction',
                  'Block_Block_Interaction', 'Make_Guess']

        Machine.__init__(self, states=states, initial='Ready')

        self.add_transition(trigger='perform_step', source='Ready', dest='Sole_Candidate',
                            before='log_initial_puzzle')

        self.add_transition(trigger='perform_step', source='Sole_Candidate', dest='Unique_Candidate',
                            conditions='fill_sole_candidate')

        # self.add_transition(trigger='perform_step', source='Unique_Candidate', dest='Make_Guess',
        #                     conditions='fill_unique_candidate')

        self.add_transition(trigger='perform_step', source='Unique_Candidate', dest='Naked_Pair',
                            conditions='fill_unique_candidate')

        self.add_transition(trigger='perform_step', source='Naked_Pair', dest='Block_RC_Interaction',
                            conditions='naked_pair')

        self.add_transition(trigger='perform_step', source='Block_RC_Interaction', dest='Block_Block_Interaction',
                            conditions='block_rc_interaction')

        self.add_transition(trigger='perform_step', source='Block_Block_Interaction', dest='Make_Guess',
                            conditions='block_block_interaction')

        self.add_transition(trigger='perform_step', source='Make_Guess', dest='Sole_Candidate',
                            before='make_guess')

        self.add_transition(trigger='perform_step', source='*', dest='Sole_Candidate')

    def validate_filled_cell(self, filled_cell, updated_cells):
        if filled_cell:
            (cell_name, val) = filled_cell
            if self.sudoku_puzzle.guess is not None:
                try:
                    self.sudoku_puzzle.validate_updated_cells_ignoring_newly_set_val(updated_cells, cell_name)
                except BadGuessError as bge:
                    self.revert_guess()
            return False
        else:
            return True

    def validate_updated_cells(self, updated_cells):
        if updated_cells:
            if self.sudoku_puzzle.guess is not None:
                try:
                    self.sudoku_puzzle.validate_updated_cells(updated_cells)
                except BadGuessError as bge:
                    self.revert_guess()
                    # TODO: Check probably isn't needed
                    self.assert_possibilities_are_non_empty()
            return False
        else:
            return True

    def fill_sole_candidate(self):
        ss = self.sudoku_puzzle.fill_sole_candidate()
        return self.validate_and_log_filled_cells_step(ss)

    def fill_unique_candidate(self):
        ss = self.sudoku_puzzle.fill_unique_candidate()
        return self.validate_and_log_filled_cells_step(ss)

    def naked_pair(self):
        ss = self.sudoku_puzzle.perform_naked_pair()
        return self.validate_and_log_updated_cells_step(ss)

    def block_rc_interaction(self):
        ss = self.sudoku_puzzle.perform_block_rc_interaction()
        return self.validate_and_log_updated_cells_step(ss)

    def block_block_interaction(self):
        ss = self.sudoku_puzzle.perform_block_block_interaction()
        return self.validate_and_log_updated_cells_step(ss)

    def make_guess(self):
        (cell_name, candidate) = self.sudoku_puzzle.determine_next_guess()
        if cell_name is None or candidate is None:
            self.revert_guess()
            return

        ss = self.sudoku_puzzle.make_guess(cell_name, candidate)
        additional = "All guesses so far: " + str(self.sudoku_puzzle.guess)
        self.sudoku_logger.log_step(ss.reason, ss.filled_cell, ss.updated_cells,
                                    self.sudoku_puzzle.get_board(), self.sudoku_puzzle.get_possibilities(), additional)

    def revert_guess(self):
        ss = self.sudoku_puzzle.revert_guess()
        additional = "Guesses now: " + str(self.sudoku_puzzle.guess)
        self.sudoku_logger.log_step(ss.reason, ss.filled_cell, ss.updated_cells, self.sudoku_puzzle.get_board(),
                                    self.sudoku_puzzle.get_possibilities(), additional)

    def validate_and_log_updated_cells_step(self, ss):
        if not ss:
            return True
        self.sudoku_logger.log_step(ss.reason, ss.filled_cell, ss.updated_cells,
                                    self.sudoku_puzzle.get_board(), self.sudoku_puzzle.get_possibilities())
        return self.validate_updated_cells(ss.updated_cells)

    def validate_and_log_filled_cells_step(self, ss):
        if not ss:
            return True
        self.sudoku_logger.log_step(ss.reason, ss.filled_cell, ss.updated_cells,
                                        self.sudoku_puzzle.get_board(), self.sudoku_puzzle.get_possibilities())
        return self.validate_filled_cell(ss.filled_cell, ss.updated_cells)

    def log_initial_puzzle(self):
        self.sudoku_logger.log_step("Starting Sudoku Solver", None, None, self.sudoku_puzzle.get_board(),
                                    self.sudoku_puzzle.get_possibilities(), "New puzzle...")

    def do_work(self):
        while not self.sudoku_puzzle.num_filled == 81:
            # print(self.current_state.name)
            self.perform_step()
            self.assert_possibilities_are_non_empty()
        print('#########################################################################################')
        self.sudoku_logger.print_log()

    def assert_possibilities_are_non_empty(self):
        for (cell_name, cell) in self.sudoku_puzzle.cells_dict.items():
            if len(cell.possibilities) < 1:
                print(cell_name, cell.possibilities)
                break
