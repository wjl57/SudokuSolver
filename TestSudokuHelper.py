import unittest
import SudokuHelper

__author__ = 'william'


class TestSudokuHelper(unittest.TestCase):

    def test_loc_to_block_num(self):
        self.assertEqual(SudokuHelper.loc_to_block_num(0, 0), 0)
        self.assertEqual(SudokuHelper.loc_to_block_num(2, 2), 0)
        self.assertEqual(SudokuHelper.loc_to_block_num(3, 2), 3)
        self.assertEqual(SudokuHelper.loc_to_block_num(4, 7), 5)
        self.assertEqual(SudokuHelper.loc_to_block_num(6, 6), 8)
        self.assertEqual(SudokuHelper.loc_to_block_num(8, 8), 8)

    def test_block_num_to_block_offsets(self):
        self.assertEqual(SudokuHelper.block_num_to_block_offsets(0), (0, 0))
        self.assertEqual(SudokuHelper.block_num_to_block_offsets(1), (0, 3))
        self.assertEqual(SudokuHelper.block_num_to_block_offsets(2), (0, 6))
        self.assertEqual(SudokuHelper.block_num_to_block_offsets(3), (3, 0))
        self.assertEqual(SudokuHelper.block_num_to_block_offsets(4), (3, 3))
        self.assertEqual(SudokuHelper.block_num_to_block_offsets(5), (3, 6))
        self.assertEqual(SudokuHelper.block_num_to_block_offsets(6), (6, 0))
        self.assertEqual(SudokuHelper.block_num_to_block_offsets(7), (6, 3))
        self.assertEqual(SudokuHelper.block_num_to_block_offsets(8), (6, 6))

    def test_offsets_to_cell_num(self):
        self.assertEqual(SudokuHelper.offsets_to_cell_num(0, 0), 0)
        self.assertEqual(SudokuHelper.offsets_to_cell_num(0, 1), 1)
        self.assertEqual(SudokuHelper.offsets_to_cell_num(0, 2), 2)
        self.assertEqual(SudokuHelper.offsets_to_cell_num(1, 0), 3)
        self.assertEqual(SudokuHelper.offsets_to_cell_num(1, 1), 4)
        self.assertEqual(SudokuHelper.offsets_to_cell_num(1, 2), 5)
        self.assertEqual(SudokuHelper.offsets_to_cell_num(2, 0), 6)
        self.assertEqual(SudokuHelper.offsets_to_cell_num(2, 1), 7)
        self.assertEqual(SudokuHelper.offsets_to_cell_num(2, 2), 8)

    def test_loc_to_block_cell_num(self):
        self.assertEqual(SudokuHelper.loc_to_block_cell_num(0, 0), 0)
        self.assertEqual(SudokuHelper.loc_to_block_cell_num(1, 2), 5)
        self.assertEqual(SudokuHelper.loc_to_block_cell_num(2, 1), 7)
        self.assertEqual(SudokuHelper.loc_to_block_cell_num(2, 2), 8)
        self.assertEqual(SudokuHelper.loc_to_block_cell_num(3, 0), 0)
        self.assertEqual(SudokuHelper.loc_to_block_cell_num(4, 5), 5)
        self.assertEqual(SudokuHelper.loc_to_block_cell_num(5, 5), 8)
        self.assertEqual(SudokuHelper.loc_to_block_cell_num(6, 6), 0)
        self.assertEqual(SudokuHelper.loc_to_block_cell_num(7, 7), 4)
        self.assertEqual(SudokuHelper.loc_to_block_cell_num(7, 8), 5)
        self.assertEqual(SudokuHelper.loc_to_block_cell_num(8, 8), 8)
