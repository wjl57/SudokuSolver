from collections import Counter, defaultdict

__author__ = 'william'


class SudokuBoard:

    all_nums = set(i for i in range(1, 10))
    rows = [set() for _ in range(0, 9)]
    cols = [set() for _ in range(0, 9)]
    blocks = [set() for _ in range(0, 9)]
    remaining_rows = [set() for _ in range(0, 9)]
    remaining_cols = [set() for _ in range(0, 9)]
    remaining_blocks = [set() for _ in range(0, 9)]
    possibilities = [[set() for _ in range(0, 9)] for _ in range(0, 9)]
    board = None
    num_unknowns = 0

    def __init__(self, board):
        self.board = board
        self.calculate_possibilities()

    def calculate_possibilities(self):
        self.num_unknowns = 0
        for y in range(0, 9):
            for x in range(0, 9):
                val = self.board[y][x]
                if val is not None:
                    self.rows[y].add(val)
                    self.cols[x].add(val)
                    index = self.loc_to_block(y, x)
                    self.blocks[index].add(val)
                else:
                    self.num_unknowns += 1

        for y in range(0, 9):
            for x in range(0, 9):
                if self.board[y][x] is not None:
                    self.possibilities[y][x] = set()
                else:
                    self.possibilities[y][x] = self.all_nums - self.rows[y] - self.cols[x] \
                                               - self.blocks[self.loc_to_block(y, x)]
        for n in range(0, 9):
            self.remaining_rows[n] = self.all_nums.copy() - self.rows[n]
            self.remaining_cols[n] = self.all_nums.copy() - self.cols[n]
            self.remaining_blocks[n] = self.all_nums.copy() - self.blocks[n]

    def fill_sole_candidates(self):
        for y in range(0, 9):
            for x in range(0, 9):
                if len(self.possibilities[y][x]) == 1:
                    self.board[y][x] = self.possibilities[y][x].pop()

    def fill_unique_candidates(self):
        for y in range(0, 9):
            d = defaultdict(int)
            for x in range(0, 9):
                for val in self.possibilities[y][x]:
                    d[val] += 1
            for val in d:
                if d[val] == 1:
                    self.board[y][x] = val
        for x in range(0, 9):
            d = defaultdict(int)
            for y in range(0, 9):
                for val in self.possibilities[y][x]:
                    d[val] += 1
            for val in d:
                if d[val] == 1:
                    self.board[y][x] = val
                    # TODO: Add in 1 in a block

    def row_to_numbered_cells(self, y):
        numbered_cells = {}
        for x in range(0, 9):
            numbered_cells[x] = self.possibilities[y][x]
        return numbered_cells

    def col_to_numbered_cells(self, x):
        numbered_cells = {}
        for y in range(0, 9):
            numbered_cells[y] = self.possibilities[y][x]
        return numbered_cells

    def block_to_numbered_cells(self, block_num):
        numbered_cells = {}
        (y_block, x_block) = self.block_num_to_board_offsets(block_num)
        num = 0
        for y_offset in range(0, 3):
            for x_offset in range(0, 3):
                numbered_cells[num] = self.possibilities[y_block + y_offset][x_block + x_offset]
                num += 1
        return numbered_cells

    @staticmethod
    def find_val_with_count_in_numbered_cells(values, numbered_sets, count):
        d = {}
        for value in values:
            num_found = 0
            found_cell_nums = []
            for cell_num in numbered_sets.keys():
                if value in numbered_sets[cell_num]:
                    num_found += 1
                    if num_found > count:
                        num_found = 0
                        break
                    else:
                        found_cell_nums.append(cell_num)
            if num_found == count:
                d[value] = found_cell_nums
        return d

    def solve_next_step(self):
        self.fill_sole_candidates()
        self.calculate_possibilities()

    def set_board_with_block_dict(self, block_num, d):
        (y_block, x_block) = self.block_num_to_board_offsets(block_num)

        for val in d.keys():
            for cell_num in d[val]:
                (y_offset, x_offset) = self.cell_num_to_block_offsets(cell_num)
                self.board[y_block+y_offset][x_block+x_offset] = val

    @staticmethod
    def cell_num_to_block_offsets(num):
        return int(num / 3), num % 3

    @staticmethod
    def block_num_to_board_offsets(num):
        return int(num / 3) * 3, num % 3 * 3

    @staticmethod
    def loc_to_block(y, x):
        return int(x/3)+int(y/3)*3

    def verify_board_full(self):
        return self.num_unknowns == 0

    def print_board(self):
        row_count = 0
        col_count = 0
        for row in self.board:
            if row_count % 3 == 0:
                row_count = 0
                print('+-----------------------------+')
            row_count += 1
            for val in row:
                if col_count % 3 == 0:
                    col_count = 0
                    print('|', end='')
                col_count += 1
                if val is None:
                    print('   ', end='')
                else:
                    print(' ' + str(val) + ' ', end='')
            print('|\n')
        print('+-----------------------------+')

    def print_possibilities(self):
        row_count = 0
        col_count = 0
        for row in self.possibilities:
            if row_count % 3 == 0:
                row_count = 0
                print('+-------------------------------------------------------------------+')
            row_count += 1
            for val in row:
                if col_count % 3 == 0:
                    col_count = 0
                    print('|', end='')
                col_count += 1
                print(' ' + str(val) + ' ', end='')
            print('|\n')
        print('+-------------------------------------------------------------------+')

