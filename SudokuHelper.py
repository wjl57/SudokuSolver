__author__ = 'william'

all_possibilities = {1, 2, 3, 4, 5, 6, 7, 8, 9}
all_locs = [i for i in range(0, 9)]
cell_locs = [i for i in range(0, 3)]


def loc_to_block_num(y, x):
    """
    :param y: The y location of the cell
    :param x: The x location of the cell
    :return: The number of the block the cell is located in
    """
    return int(x/3)+int(y/3)*3


def block_num_to_block_offsets(block_num):
    """
    :param block_num: the block number
    :return: The (y, x) position of the top-left cell in the block
    """
    return int(block_num / 3) * 3, block_num % 3 * 3


def offsets_to_cell_num(y_offset, x_offset):
    """
    :param y_offset: The y_offset inside a block
    :param x_offset: The x_offset inside a block
    :return: The cell number inside a block
    """
    return 3 * y_offset + x_offset


def loc_to_block_cell_num(y, x):
    """
    :param y: The y location of the cell
    :param x: The x location of the cell
    :return: The cell number inside a block
    """
    return (y % 3) * 3 + (x % 3)
