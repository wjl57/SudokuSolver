import logging
import sys
from transitions import Machine
from transitions import logger
# logger.setLevel(logging.INFO)
# logging.basicConfig(stream=sys.stdout, level=logging.INFO)

__author__ = 'william'


class SudokuSolver(Machine):

    def __init__(self, sp):
        self.sudoku_puzzle = sp

        states = ['Ready', 'Sole_Candidates', 'Unique_Candidates', 'Block_RC_Interactions', 'Block_Block_Interactions',
                  'Naked_Pairs', 'Done']
        print(states)
        Machine.__init__(self, states=states, initial='Ready')

        self.add_transition(trigger='perform_step', source='Ready', dest='Sole_Candidates')

        self.add_transition(trigger='perform_step', source='Sole_Candidates', dest='Unique_Candidates',
                            conditions='fill_sole_candidates')

        self.add_transition(trigger='perform_step', source='Unique_Candidates', dest='Naked_Pairs',
                            conditions='fill_unique_candidates')

        self.add_transition(trigger='perform_step', source='Naked_Pairs', dest='Block_RC_Interactions',
                            conditions='naked_pairs')

        self.add_transition(trigger='perform_step', source='Block_RC_Interactions', dest='Block_Block_Interactions',
                            conditions='block_rc_interactions')

        self.add_transition(trigger='perform_step', source='Block_Block_Interactions', dest='Done',
                            conditions='block_block_interactions')

        self.add_transition(trigger='perform_step', source='*', dest='Sole_Candidates')

    def print_state_and_board_then_return(self, filled_cells):
        if filled_cells:
            print(self.state + ': ' + str(filled_cells))
            self.sudoku_puzzle.print_board()
            return False
        else:
            print(self.state + ': None found')
            return True

    def print_state_then_return(self, updated_cells):
        if updated_cells:
            print(self.state + ': ' + str(updated_cells))
            # TODO: Check if this actually works
            if self.sudoku_puzzle.guess is not None:
                try:
                    self.sudoku_puzzle.validate_updated_cells(updated_cells)
                except BadGuessError as bge:
                    print(bge)
                    self.sudoku_puzzle.revert_guess()
            return False
        else:
            print(self.state + ': None found')
            return True

    def fill_sole_candidates(self):
        filled_cells = self.sudoku_puzzle.fill_sole_candidates()
        return self.print_state_and_board_then_return(filled_cells)

    def fill_unique_candidates(self):
        filled_cells = self.sudoku_puzzle.fill_unique_candidates()
        return self.print_state_and_board_then_return(filled_cells)

    def naked_pairs(self):
        updated_cells = self.sudoku_puzzle.all_naked_pairs()
        return self.print_state_then_return(updated_cells)

    def block_rc_interactions(self):
        updated_cells = self.sudoku_puzzle.all_block_rc_interactions()
        return self.print_state_then_return(updated_cells)

    def block_block_interactions(self):
        updated_cells = self.sudoku_puzzle.all_block_block_interactions()
        return self.print_state_then_return(updated_cells)

    def do_work(self):
        print(self.state)
        self.sudoku_puzzle.print_board()
        while not self.is_Done():
            self.perform_step()

            # self.sudoku_puzzle.print_board()
