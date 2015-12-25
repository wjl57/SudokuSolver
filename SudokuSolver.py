from transitions import Machine
from SudokuError import BadGuessError
from SudokuLogger import SudokuLogger

__author__ = 'william'


class SudokuSolver(Machine):

    def __init__(self, sp):
        self.sudoku_puzzle = sp
        self.sudoku_logger = SudokuLogger()
        self.just_solved_step = False

        states = ['Ready', 'Sole_Candidate', 'Unique_Candidate', 'Make_Guess', 'Done', 'Not_Complete']

        # ordered_optional_states = []

        ordered_optional_states = ['Naked_Pair', 'Hidden_Pair', 'Naked_Tuple_3', 'Naked_Tuple_4',
                                   'Block_RC_Interaction', 'Block_Block_Interaction',
                                   'Hidden_Subset_3', 'Hidden_Subset_4', 'Basic_Fish', 'Fish_3', 'Fish_4',
                                   'Skyscraper', 'Kite']

        optional_state_map = {
            'Naked_Pair': 'naked_pair',
            'Naked_Tuple_3': 'naked_tuple_3',
            'Naked_Tuple_4': 'naked_tuple_4',
            'Block_RC_Interaction': 'block_rc_interaction',
            'Block_Block_Interaction': 'block_block_interaction',
            'Hidden_Pair': 'hidden_subset_2',
            'Hidden_Subset_3': 'hidden_subset_3',
            'Hidden_Subset_4': 'hidden_subset_4',
            'Basic_Fish': 'basic_fish',
            'Fish_3': 'fish_3',
            'Fish_4': 'fish_4',
            'Skyscraper': 'skyscraper',
            'Kite': 'kite'
        }

        states += ordered_optional_states

        Machine.__init__(self, states=states, initial='Ready')

        self.add_transition(trigger='perform_step', source='Ready', dest='Sole_Candidate',
                            before='log_initial_puzzle')

        self.add_transition(trigger='perform_step', source='Sole_Candidate', dest='Unique_Candidate',
                            conditions='fill_sole_candidate')

        if not ordered_optional_states:
            self.add_transition(trigger='perform_step', source='Unique_Candidate', dest='Make_Guess',
                                before='fill_unique_candidate')
        else:
            # Add the transitions from super basic technique to first optional
            num_optional_states = len(ordered_optional_states)
            self.add_transition(trigger='perform_step', source='Unique_Candidate', dest=ordered_optional_states[0],
                                conditions='fill_unique_candidate')

            # Add transitions from one optional technique to another
            for n in range(0, num_optional_states - 1):
                self.add_transition(trigger='perform_step',
                                    source=ordered_optional_states[n],
                                    dest=ordered_optional_states[n+1],
                                    conditions=optional_state_map[ordered_optional_states[n]])

            # Add mandatory transition from optional to guessing for the last optional state
            self.add_transition(trigger='perform_step',
                                source=ordered_optional_states[-1],
                                dest='Make_Guess',
                                conditions=optional_state_map[ordered_optional_states[-1]])

        # Add the mandatory transitions
        self.add_transition(trigger='perform_step', source='Make_Guess', dest='Sole_Candidate',
                            before='make_guess')

        self.add_transition(trigger='perform_step', source='*', dest='Sole_Candidate')

        self.add_transition(trigger='done', source='*', dest='Done')
        self.add_transition(trigger='not_complete', source='*', dest='Not_Complete')

    def validate_filled_cell(self, filled_cell, updated_cells):
        if filled_cell:
            (cell_name, val) = filled_cell
            if self.sudoku_puzzle.guess is not None:
                try:
                    self.sudoku_puzzle.validate_updated_cells_ignoring_newly_set_val(updated_cells, cell_name)
                except BadGuessError as bge:
                    self.revert_guess()
            self.just_solved_step = True
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
            self.just_solved_step = True
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

    def naked_tuple_3(self):
        ss = self.sudoku_puzzle.perform_naked_tuple(3)
        return self.validate_and_log_updated_cells_step(ss)

    def naked_tuple_4(self):
        ss = self.sudoku_puzzle.perform_naked_tuple(4)
        return self.validate_and_log_updated_cells_step(ss)

    def hidden_subset_2(self):
        ss = self.sudoku_puzzle.perform_hidden_subset(2)
        return self.validate_and_log_updated_cells_step(ss)

    def hidden_subset_3(self):
        ss = self.sudoku_puzzle.perform_hidden_subset(3)
        return self.validate_and_log_updated_cells_step(ss)

    def hidden_subset_4(self):
        ss = self.sudoku_puzzle.perform_hidden_subset(4)
        return self.validate_and_log_updated_cells_step(ss)

    def basic_fish(self):
        ss = self.sudoku_puzzle.perform_basic_fish()
        return self.validate_and_log_updated_cells_step(ss)

    def fish_3(self):
        ss = self.sudoku_puzzle.perform_fish(3)
        return self.validate_and_log_updated_cells_step(ss)

    def fish_4(self):
        ss = self.sudoku_puzzle.perform_fish(4)
        return self.validate_and_log_updated_cells_step(ss)

    def skyscraper(self):
        ss = self.sudoku_puzzle.perform_skyscraper()
        return self.validate_and_log_updated_cells_step(ss)

    def kite(self):
        ss = self.sudoku_puzzle.perform_kite()
        self.assert_possibilities_are_non_empty()
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
            self.solve_next_step()
            self.assert_possibilities_are_non_empty()
        print('#########################################################################################')
        self.sudoku_logger.print_log()

    def solve_next_step(self):
        self.just_solved_step = False
        while not self.just_solved_step:
            self.perform_step()

    def assert_possibilities_are_non_empty(self):
        for (cell_name, cell) in self.sudoku_puzzle.cells_dict.items():
            if len(cell.possibilities) < 1:
                print(cell_name, str(self.current_state.name))
                break
