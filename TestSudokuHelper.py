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

    def test_cell_num_to_block_offsets(self):
        self.assertEqual(SudokuHelper.cell_num_to_block_offsets(0), (0, 0))
        self.assertEqual(SudokuHelper.cell_num_to_block_offsets(1), (0, 1))
        self.assertEqual(SudokuHelper.cell_num_to_block_offsets(2), (0, 2))
        self.assertEqual(SudokuHelper.cell_num_to_block_offsets(3), (1, 0))
        self.assertEqual(SudokuHelper.cell_num_to_block_offsets(4), (1, 1))
        self.assertEqual(SudokuHelper.cell_num_to_block_offsets(5), (1, 2))
        self.assertEqual(SudokuHelper.cell_num_to_block_offsets(6), (2, 0))
        self.assertEqual(SudokuHelper.cell_num_to_block_offsets(7), (2, 1))
        self.assertEqual(SudokuHelper.cell_num_to_block_offsets(8), (2, 2))

    def test_block_num_and_cell_num_to_offsets(self):
        self.assertEqual(SudokuHelper.block_num_and_cell_num_to_offsets(0, 0), (0, 0))
        self.assertEqual(SudokuHelper.block_num_and_cell_num_to_offsets(0, 2), (0, 2))
        self.assertEqual(SudokuHelper.block_num_and_cell_num_to_offsets(0, 3), (1, 0))
        self.assertEqual(SudokuHelper.block_num_and_cell_num_to_offsets(0, 7), (2, 1))
        self.assertEqual(SudokuHelper.block_num_and_cell_num_to_offsets(1, 0), (0, 3))
        self.assertEqual(SudokuHelper.block_num_and_cell_num_to_offsets(1, 2), (0, 5))
        self.assertEqual(SudokuHelper.block_num_and_cell_num_to_offsets(1, 3), (1, 3))
        self.assertEqual(SudokuHelper.block_num_and_cell_num_to_offsets(1, 7), (2, 4))
        self.assertEqual(SudokuHelper.block_num_and_cell_num_to_offsets(6, 0), (6, 0))
        self.assertEqual(SudokuHelper.block_num_and_cell_num_to_offsets(6, 2), (6, 2))
        self.assertEqual(SudokuHelper.block_num_and_cell_num_to_offsets(6, 3), (7, 0))
        self.assertEqual(SudokuHelper.block_num_and_cell_num_to_offsets(6, 7), (8, 1))
        self.assertEqual(SudokuHelper.block_num_and_cell_num_to_offsets(8, 8), (8, 8))

    def test_get_other_block_nums_horizontal(self):
        self.assertListEqual(SudokuHelper.get_other_block_nums_horizontal(0), [1, 2])
        self.assertListEqual(SudokuHelper.get_other_block_nums_horizontal(1), [0, 2])
        self.assertListEqual(SudokuHelper.get_other_block_nums_horizontal(2), [0, 1])
        self.assertListEqual(SudokuHelper.get_other_block_nums_horizontal(3), [4, 5])
        self.assertListEqual(SudokuHelper.get_other_block_nums_horizontal(4), [3, 5])
        self.assertListEqual(SudokuHelper.get_other_block_nums_horizontal(5), [3, 4])
        self.assertListEqual(SudokuHelper.get_other_block_nums_horizontal(6), [7, 8])
        self.assertListEqual(SudokuHelper.get_other_block_nums_horizontal(7), [6, 8])
        self.assertListEqual(SudokuHelper.get_other_block_nums_horizontal(8), [6, 7])

    def test_get_other_block_nums_vertical(self):
        self.assertListEqual(SudokuHelper.get_other_block_nums_vertical(0), [3, 6])
        self.assertListEqual(SudokuHelper.get_other_block_nums_vertical(1), [4, 7])
        self.assertListEqual(SudokuHelper.get_other_block_nums_vertical(2), [5, 8])
        self.assertListEqual(SudokuHelper.get_other_block_nums_vertical(3), [0, 6])
        self.assertListEqual(SudokuHelper.get_other_block_nums_vertical(4), [1, 7])
        self.assertListEqual(SudokuHelper.get_other_block_nums_vertical(5), [2, 8])
        self.assertListEqual(SudokuHelper.get_other_block_nums_vertical(6), [0, 3])
        self.assertListEqual(SudokuHelper.get_other_block_nums_vertical(7), [1, 4])
        self.assertListEqual(SudokuHelper.get_other_block_nums_vertical(8), [2, 5])

    def test_cell_name_to_loc(self):
        self.assertEqual(SudokuHelper.cell_name_to_loc('c000'), (0, 0))
        self.assertEqual(SudokuHelper.cell_name_to_loc('c100'), (1, 0))
        self.assertEqual(SudokuHelper.cell_name_to_loc('c220'), (2, 2))
        self.assertEqual(SudokuHelper.cell_name_to_loc('c241'), (2, 4))
        self.assertEqual(SudokuHelper.cell_name_to_loc('c313'), (3, 1))
        self.assertEqual(SudokuHelper.cell_name_to_loc('c455'), (4, 5))
        self.assertEqual(SudokuHelper.cell_name_to_loc('c688'), (6, 8))
        self.assertEqual(SudokuHelper.cell_name_to_loc('c757'), (7, 5))
