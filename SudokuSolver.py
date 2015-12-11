import logging
import sys
from transitions import Machine
from transitions import logger
# logger.setLevel(logging.INFO)
# logging.basicConfig(stream=sys.stdout, level=logging.INFO)

__author__ = 'william'


class SudokuSolver(object):
    states = ['Ready', 'Sole_Candidates', 'Unique_Candidates', 'Block_RC_Interaction', 'Done']

    def __init__(self, sp):
        self.sudoku_puzzle = sp
        machine = Machine(model=self, states=SudokuSolver.states, initial='Ready')

        machine.add_transition(trigger='perform_step', source='Ready', dest='Sole_Candidates')

        machine.add_transition(trigger='perform_step', source='Sole_Candidates', dest='Unique_Candidates',
                               conditions='fill_sole_candidates')

        machine.add_transition(trigger='perform_step', source='Unique_Candidates', dest='Block_RC_Interaction',
                               conditions='fill_unique_candidates')

        machine.add_transition(trigger='perform_step', source='Block_RC_Interaction', dest='Done',
                       conditions='block_rc_interactions')

        machine.add_transition(trigger='perform_step', source='*', dest='Sole_Candidates')

    def fill_sole_candidates(self):
        filled_cells = self.sudoku_puzzle.fill_sole_candidates()
        return self.print_state_and_board_then_return(filled_cells)

    def fill_unique_candidates(self):
        filled_cells = self.sudoku_puzzle.fill_unique_candidates()
        return self.print_state_and_board_then_return(filled_cells)

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
            return False
        else:
            print(self.state + ': None found')
            return True

    def block_rc_interactions(self):
        updated_cells = self.sudoku_puzzle.all_block_rc_interactions()
        return self.print_state_then_return(updated_cells)

    def do_work(self):
        print(self.state)
        self.sudoku_puzzle.print_board()
        while not self.is_Done():
            self.perform_step()

            # self.sudoku_puzzle.print_board()


