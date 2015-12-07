__author__ = 'william'

all_possibilities = {1, 2, 3, 4, 5, 6, 7, 8, 9}
all_locs = [i for i in range(0, 9)]
cell_locs = [i for i in range(0, 3)]


def loc_to_block_num(y, x):
    """
    :param y: The y location of the cell. Precondition: 0 <= y < 9
    :param x: The x location of the cell Precondition: 0 <= x < 9
    :return: The number of the block the cell is located in
    """
    return int(x/3)+int(y/3)*3


def block_num_to_block_offsets(block_num):
    """
    :param block_num: The block number. Precondition: 0 <= block_num < 9
    :return: The (y, x) position of the top-left cell in the block
    """
    return int(block_num / 3) * 3, block_num % 3 * 3


def offsets_to_cell_num(y_offset, x_offset):
    """
    :param y_offset: The y_offset inside a block. Precondition: 0 <= y_offset < 3
    :param x_offset: The x_offset inside a block. Precondition: 0 <= x_offset < 3
    :return: The cell number inside a block
    """
    return 3 * y_offset + x_offset


def loc_to_block_cell_num(y, x):
    """
    :param y: The y location of the cell on the board. Precondition: 0 <= y < 9
    :param x: The x location of the cell on the board. Precondition: 0 <= x < 9
    :return: The cell number offset inside a block
    """
    return (y % 3) * 3 + (x % 3)


def cell_num_to_block_offsets(cell_num):
    """
    :param cell_num: The cell number within the block. Precondition: 0 <= y < 9
    :return: (y_offset, x_offset) where y_offset is the number of cells from the top
    and x_offset is the number of cells from the bottom
    """
    return int(cell_num / 3), cell_num % 3


def block_num_and_cell_num_to_offsets(block_num, cell_num):
    """
    :param block_num: The block number. Precondition: 0 <= block_num < 9
    :param cell_num: The cell number in a block. Precondition: 0 <= block_num < 9
    :return: The (y,x) coordinates of the cell
    """
    (y_block, x_block) = block_num_to_block_offsets(block_num)
    (y_offset, x_offset) = cell_num_to_block_offsets(cell_num)
    return y_block + y_offset, x_block + x_offset


def get_other_block_nums_horizontal(excluded_block_num):
    """
    :param excluded_block_num: The excluded block number
    :return: The other two block numbers in the block row
    i.e. if excluded_block_num = 1, return [0, 2]
    """
    start = int(excluded_block_num / 3) * 3
    return [start+n for n in cell_locs if start+n != excluded_block_num]


def get_other_block_nums_vertical(excluded_block_num):
    """
    :param excluded_block_num: The excluded block number
    :return: The other two block numbers in the block col
    i.e. if excluded_block_num = 1, return [4, 7]
    """
    start = excluded_block_num % 3
    return [start+3*n for n in cell_locs if start+3*n != excluded_block_num]


def cell_name_to_loc(cell_name):
    """
    :param cell_name: A cell name in the form 'cYXB' where Y is y-coord, X is x-coord, B is block num
    :return: (y, x) location of the cell
    """
    return int(cell_name[1]), int(cell_name[2])