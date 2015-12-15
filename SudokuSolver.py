from transitions import Machine
from BadGuessError import BadGuessError
from SudokuLogger import SudokuLogger, SudokuStepLog
from SudokuPuzzle import SudokuPuzzle

__author__ = 'william'


class SudokuSolver(Machine):

    def __init__(self, sp):
        self.sudoku_puzzle = sp
        self.sudoku_logger = SudokuLogger()

        states = ['Ready', 'Sole_Candidate', 'Unique_Candidate', 'Block_RC_Interactions', 'Block_Block_Interactions',
                  'Naked_Pairs', 'Make_Guess', 'Done']
        print(states)
        Machine.__init__(self, states=states, initial='Ready')

        self.add_transition(trigger='perform_step', source='Ready', dest='Sole_Candidate')

        self.add_transition(trigger='perform_step', source='Sole_Candidate', dest='Unique_Candidate',
                            conditions='fill_sole_candidate')

        self.add_transition(trigger='perform_step', source='Unique_Candidate', dest='Make_Guess',
                            conditions='fill_unique_candidate')

        self.add_transition(trigger='perform_step', source='Make_Guess', dest='Sole_Candidate',
                            before='make_guess')

        # self.add_transition(trigger='perform_step', source='Unique_Candidates', dest='Naked_Pairs',
        #                     conditions='fill_unique_candidates')

        # self.add_transition(trigger='perform_step', source='Naked_Pairs', dest='Block_RC_Interactions',
        #                     conditions='naked_pairs')
        #
        # self.add_transition(trigger='perform_step', source='Block_RC_Interactions', dest='Block_Block_Interactions',
        #                     conditions='block_rc_interactions')
        #
        # self.add_transition(trigger='perform_step', source='Block_Block_Interactions', dest='Done',
        #                     conditions='block_block_interactions')

        self.add_transition(trigger='perform_step', source='*', dest='Sole_Candidate')

    def print_state_and_board_then_return(self, filled_cell, updated_cells):
        if filled_cell:
            (cell_name, val) = filled_cell
            print(self.state + ": " + str(filled_cell))
            # TODO: Check if this actually works
            if self.sudoku_puzzle.guess is not None:
                try:
                    self.sudoku_puzzle.validate_updated_cells_ignoring_newly_set_val(updated_cells, cell_name)
                except BadGuessError as bge:
                    print(bge)
                    print("REVERTING GUESS!!!!!!!!!!!!!!!!!!!!!!!!! to " + str(self.sudoku_puzzle.guess.previous_guess))
                    self.sudoku_puzzle.revert_guess()
                    SudokuPuzzle.print_board(self.sudoku_puzzle.get_board())
                    self.sudoku_puzzle.print_possibilities()
                    self.assert_possibilities_are_non_empty()
                    print(self.sudoku_puzzle.num_filled)
            else:
                SudokuPuzzle.print_board(self.sudoku_puzzle.get_board())
                self.sudoku_puzzle.print_possibilities()
            return False
        else:
            print(self.state + ": None found")
            return True

    def print_state_then_return(self, updated_cells):
        if updated_cells:
            print(self.state + ": " + str(updated_cells))
            self.sudoku_puzzle.print_possibilities()
            # TODO: Check if this actually works
            if self.sudoku_puzzle.guess is not None:
                try:
                    self.sudoku_puzzle.validate_updated_cells(updated_cells)
                except BadGuessError as bge:
                    print(bge)
                    print("REVERTING GUESS!!!!!!!!!!!!!!!!!!!!!!!!!")
                    self.sudoku_puzzle.revert_guess()
                    SudokuPuzzle.print_board(self.sudoku_puzzle.get_board())
                    self.assert_possibilities_are_non_empty()
                    print(self.sudoku_puzzle.num_filled)
            return False
        else:
            print(self.state + ": None found")
            return True

    def fill_sole_candidate(self):
        (filled_cell, updated_cells) = self.sudoku_puzzle.fill_sole_candidate()
        self.sudoku_logger.log_step("Sole candidate", filled_cell, updated_cells,
                                    self.sudoku_puzzle.get_board(), self.sudoku_puzzle.get_possibilities())
        return self.print_state_and_board_then_return(filled_cell, updated_cells)

    def fill_unique_candidate(self):
        (filled_cell, updated_cells) = self.sudoku_puzzle.fill_unique_candidate()
        self.sudoku_logger.log_step("Unique candidate", filled_cell, updated_cells,
                                    self.sudoku_puzzle.get_board(), self.sudoku_puzzle.get_possibilities())
        return self.print_state_and_board_then_return(filled_cell, updated_cells)

    def naked_pairs(self):
        updated_cells = self.sudoku_puzzle.all_naked_pairs()
        return self.print_state_then_return(updated_cells)

    def block_rc_interactions(self):
        updated_cells = self.sudoku_puzzle.all_block_rc_interactions()
        return self.print_state_then_return(updated_cells)

    def block_block_interactions(self):
        updated_cells = self.sudoku_puzzle.all_block_block_interactions()
        return self.print_state_then_return(updated_cells)

    def make_guess(self):
        (candidate, cell_name) = self.sudoku_puzzle.determine_next_guess()
        if candidate is None or cell_name is None:
            self.sudoku_puzzle.revert_guess()
            return
        print(self.sudoku_puzzle.num_filled)
        (filled_cell, updated_cells) = self.sudoku_puzzle.make_guess(candidate, cell_name)
        additional = "All guesses so far: " + str(self.sudoku_puzzle.guess)
        self.sudoku_logger.log_step("Guessing: ", filled_cell, updated_cells,
                                    self.sudoku_puzzle.get_board(), self.sudoku_puzzle.get_possibilities(), additional)

    def do_work(self):
        print(self.state)
        SudokuPuzzle.print_board(self.sudoku_puzzle.get_board())
        while not self.sudoku_puzzle.num_filled == 81:
            self.perform_step()
            self.assert_possibilities_are_non_empty()
            print("num filled: " + str(self.sudoku_puzzle.num_filled))
        # SudokuPuzzle.print_board(self.sudoku_puzzle.get_board())
        print("num filled at end: " + str(self.sudoku_puzzle.num_filled))
        print('#########################################################################################')
        self.sudoku_logger.print_log()

    def assert_possibilities_are_non_empty(self):
        for (cell_name, cell) in self.sudoku_puzzle.cells_dict.items():
            if len(cell.possibilities) < 1:
                print(cell_name, cell.possibilities)
                break
