import copy

__author__ = 'william'


class SudokuBoard:

    all_nums = set(i for i in range(1, 10))
    rows = [set() for _ in range(0, 9)]
    cols = [set() for _ in range(0, 9)]
    blocks = [set() for _ in range(0, 9)]
    remaining_in_rows = [set() for _ in range(0, 9)]
    remaining_in_cols = [set() for _ in range(0, 9)]
    remaining_in_blocks = [set() for _ in range(0, 9)]
    possibilities = [[set() for _ in range(0, 9)] for _ in range(0, 9)]
    board = None
    num_unknowns = 0

    def __init__(self, board):
        self.board = copy.deepcopy(board)
        self.rows = [set() for _ in range(0, 9)]
        self.cols = [set() for _ in range(0, 9)]
        self.blocks = [set() for _ in range(0, 9)]
        self.remaining_in_rows = [set() for _ in range(0, 9)]
        self.remaining_in_cols = [set() for _ in range(0, 9)]
        self.remaining_in_blocks = [set() for _ in range(0, 9)]
        self.possibilities = [[set() for _ in range(0, 9)] for _ in range(0, 9)]
        self.calculate_possibilities()

    def calculate_possibilities(self):
        self.num_unknowns = 0
        for y in range(0, 9):
            for x in range(0, 9):
                val = self.board[y][x]
                if val is not None:
                    self.rows[y].add(val)
                    self.cols[x].add(val)
                    block_num = self.loc_to_block_num(y, x)
                    self.blocks[block_num].add(val)
                else:
                    self.num_unknowns += 1

        for y in range(0, 9):
            for x in range(0, 9):
                if self.board[y][x] is not None:
                    self.possibilities[y][x] = set()
                else:
                    self.possibilities[y][x] = self.all_nums - self.rows[y] - self.cols[x] \
                                               - self.blocks[self.loc_to_block_num(y, x)]
        for n in range(0, 9):
            self.remaining_in_rows[n] = self.all_nums.copy() - self.rows[n]
            self.remaining_in_cols[n] = self.all_nums.copy() - self.cols[n]
            self.remaining_in_blocks[n] = self.all_nums.copy() - self.blocks[n]

    def fill_sole_candidates(self):
        for y in range(0, 9):
            for x in range(0, 9):
                if len(self.possibilities[y][x]) == 1:
                    self.board[y][x] = self.possibilities[y][x].pop()

    def fill_unique_candidates(self):
        # count = 1 since unique candidates
        count = 1
        for y in range(0, 9):
            numbered_cells = self.row_possibilities_to_numbered_cells(y)
            d = SudokuBoard.find_val_with_count_in_numbered_cells(self.remaining_in_rows[y], numbered_cells, count)
            self.set_board_with_row_dict(y, d)
        for x in range(0, 9):
            numbered_cells = self.col_possibilities_to_numbered_cells(x)
            d = SudokuBoard.find_val_with_count_in_numbered_cells(self.remaining_in_cols[x], numbered_cells, count)
            self.set_board_with_col_dict(x, d)
        for block_num in range(0, 9):
            numbered_cells = self.block_possibilities_to_numbered_cells(block_num)
            d = SudokuBoard.find_val_with_count_in_numbered_cells(self.remaining_in_blocks[block_num], numbered_cells, count)
            self.set_board_with_block_dict(block_num, d)

    def set_board_with_row_dict(self, y, d):
        for val in d.keys():
            for x in d[val]:
                self.board[y][x] = val

    def set_board_with_col_dict(self, x, d):
        for val in d.keys():
            for y in d[val]:
                self.board[y][x] = val

    def set_board_with_block_dict(self, block_num, d):
        (y_block, x_block) = self.block_num_to_board_offsets(block_num)

        for val in d.keys():
            for cell_num in d[val]:
                (y_offset, x_offset) = self.cell_num_to_block_offsets(cell_num)
                self.board[y_block+y_offset][x_block+x_offset] = val

    def row_possibilities_to_numbered_cells(self, y):
        numbered_cells = {}
        for x in range(0, 9):
            numbered_cells[x] = self.possibilities[y][x]
        return numbered_cells

    def col_possibilities_to_numbered_cells(self, x):
        numbered_cells = {}
        for y in range(0, 9):
            numbered_cells[y] = self.possibilities[y][x]
        return numbered_cells

    def block_possibilities_to_numbered_cells(self, block_num):
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

    def all_block_rc_interactions(self):
        for block_num in range(0, 9):
            self.block_rc_interaction(block_num)

    def block_rc_interaction(self, block_num):
        numbered_cells = self.block_possibilities_to_numbered_cells(block_num)
        numbered_cells_in_rows = {y: set() for y in range(0, 3)}
        numbered_cells_in_cols = {x: set() for x in range(0, 3)}
        for cell_num in range(0, 9):
            (y_offset, x_offset) = self.cell_num_to_block_offsets(cell_num)
            block_offset = self.loc_to_block_offset(y_offset, x_offset)
            possibilities = numbered_cells[block_offset]
            numbered_cells_in_rows[y_offset].update(possibilities)
            numbered_cells_in_cols[x_offset].update(possibilities)
        # d is a dictionary from val to the row offset in a block
        d = self.find_val_with_count_in_numbered_cells(self.remaining_in_blocks[block_num], numbered_cells_in_rows, 1)
        self.eliminate_row_possibilities_by_block_dict(block_num, d)
        # d is a dictionary from val to the col offset in a block
        d = self.find_val_with_count_in_numbered_cells(self.remaining_in_blocks[block_num], numbered_cells_in_cols, 1)
        self.eliminate_col_possibilities_by_block_dict(block_num, d)

    def eliminate_row_possibilities_by_block_dict(self, block_num, d):
        (y_block, x_block) = self.block_num_to_board_offsets(block_num)
        for val in d.keys():
            for y_offset in d[val]:
                y = y_block + y_offset
                for x in range(0, 9):
                    if SudokuBoard.loc_to_block_num(y, x) != block_num:
                        self.possibilities[y][x].remove(val)

    def eliminate_col_possibilities_by_block_dict(self, block_num, d):
        (y_block, x_block) = self.block_num_to_board_offsets(block_num)
        for val in d.keys():
            for x_offset in d[val]:
                x = x_block + x_offset
                for y in range(0, 9):
                    if SudokuBoard.loc_to_block_num(y, x) != block_num:
                        self.possibilities[y][x].remove(val)

    def all_block_block_interactions(self):
        for i in range(0, 3):
            for j in range(0, 3):
                self.block_block_by_block_row_interaction(i, j)
        for i in range(0, 3):
            for j in range(0, 3):
                self.block_block_by_block_col_interaction(i, j)

    def block_block_by_block_row_interaction(self, square_row, excluded_sq_offset):
        sq_row_offset_1, sq_row_offset_2 = self.get_remaining_2(excluded_sq_offset)
        block_num_1 = self.square_row_and_offset_to_block_num(square_row, sq_row_offset_1)
        block_num_2 = self.square_row_and_offset_to_block_num(square_row, sq_row_offset_2)
        excluded_block_num = self.square_row_and_offset_to_block_num(square_row, excluded_sq_offset)
        block_1_possibilities = self.remaining_in_blocks[block_num_1]
        block_2_possibilities = self.remaining_in_blocks[block_num_2]
        possibilities_in_both_blocks = block_1_possibilities.intersection(block_2_possibilities)
        _, x_block_1 = self.block_num_to_board_offsets(block_num_1)
        _, x_block_2 = self.block_num_to_board_offsets(block_num_2)
        for y_offset in range(0, 3):
            possibilities_by_row = set()
            y = self.square_offset_and_offset_to_num(square_row, y_offset)
            for x_offset in range(0, 3):
                possibilities_by_row.update(self.possibilities[y][x_block_1 + x_offset])
                possibilities_by_row.update(self.possibilities[y][x_block_2 + x_offset])
            for val in possibilities_in_both_blocks:
                if val not in possibilities_by_row:
                    self.eliminate_possibilities_by_block_row(excluded_block_num, y, val)

    def eliminate_possibilities_by_block_row(self, block_num, excluded_y, val):
        _, x_block = self.block_num_to_board_offsets(block_num)
        x_offsets = [i + x_block for i in range(0, 3)]
        y_1, y_2 = self.get_remaining_2(excluded_y)
        for x in x_offsets:
            self.possibilities[y_1][x].discard(val)
            self.possibilities[y_2][x].discard(val)

    def block_block_by_block_col_interaction(self, square_col, excluded_sq_offset):
        sq_col_offset_1, sq_col_offset_2 = self.get_remaining_2(excluded_sq_offset)
        block_num_1 = self.square_col_and_offset_to_block_num(square_col, sq_col_offset_1)
        block_num_2 = self.square_col_and_offset_to_block_num(square_col, sq_col_offset_2)
        excluded_block_num = self.square_col_and_offset_to_block_num(square_col, excluded_sq_offset)
        block_1_possibilities = self.remaining_in_blocks[block_num_1]
        block_2_possibilities = self.remaining_in_blocks[block_num_2]
        possibilities_in_both_blocks = block_1_possibilities.intersection(block_2_possibilities)
        y_block_1, _ = self.block_num_to_board_offsets(block_num_1)
        y_block_2, _ = self.block_num_to_board_offsets(block_num_2)
        for x_offset in range(0, 3):
            possibilities_by_col = set()
            x = self.square_offset_and_offset_to_num(square_col, x_offset)
            for y_offset in range(0, 3):
                p = self.possibilities[y_block_1 + y_offset][x]
                possibilities_by_col.update(self.possibilities[y_block_1 + y_offset][x])
                p = self.possibilities[y_block_2 + y_offset][x]
                possibilities_by_col.update(self.possibilities[y_block_2 + y_offset][x])
            for val in possibilities_in_both_blocks:
                if val not in possibilities_by_col:
                    self.eliminate_possibilities_by_block_col(excluded_block_num, x, val)

    def eliminate_possibilities_by_block_col(self, block_num, excluded_x, val):
        y_block, _ = self.block_num_to_board_offsets(block_num)
        y_offsets = [i + y_block for i in range(0, 3)]
        x_1, x_2 = self.get_remaining_2(excluded_x)
        for y in y_offsets:
            self.possibilities[y][x_1].discard(val)
            self.possibilities[y][x_2].discard(val)

    def solve_next_step(self):
        self.fill_sole_candidates()
        self.calculate_possibilities()

    @staticmethod
    def get_remaining_2(num):
        start = int(num / 3) * 3
        rem = num % 3
        if rem == 0:
            return start + 1, start + 2
        elif rem == 1:
            return start, start + 2
        else:
            return start, start + 1

    # @staticmethod
    # def get_remaining_of_3(excluded_offset):
    #     offsets = {0, 1, 2} - {excluded_offset}
    #     offset_1 = offsets.pop()
    #     offset_2 = offsets.pop()
    #     return offset_1, offset_2

    @staticmethod
    def square_offset_and_offset_to_num(sq_offset, offset):
        return sq_offset * 3 + offset

    @staticmethod
    def cell_num_to_block_offsets(num):
        return int(num / 3), num % 3

    @staticmethod
    def block_num_to_board_offsets(num):
        return int(num / 3) * 3, num % 3 * 3

    @staticmethod
    def loc_to_block_num(y, x):
        return int(x/3)+int(y/3)*3

    @staticmethod
    def loc_to_block_offset(y, x):
        return 3*y+x

    @staticmethod
    def square_row_and_offset_to_block_num(square_row, sq_row_offset):
        return square_row * 3 + sq_row_offset

    @staticmethod
    def square_col_and_offset_to_block_num(square_col, sq_col_offset):
        return square_col + sq_col_offset * 3

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

    @staticmethod
    def rotate_board_cw(board, n=1):
        def rotate_cw(board):
            rotated_board = [[None for _ in range(0, 9)] for _ in range(0, 9)]
            for y in range(0, 9):
                for x in range(0, 9):
                    rotated_board[y][x] = board[8-x][y]
            return rotated_board

        for _ in range(0, n % 4):
            board = rotate_cw(board)
        return board

    @staticmethod
    def rotate_board_ccw(board, n=1):
        def rotate_ccw(board):
            rotated_board = [[None for _ in range(0, 9)] for _ in range(0, 9)]
            for y in range(0, 9):
                for x in range(0, 9):
                    rotated_board[y][x] = board[x][8-y]
            return rotated_board

        for _ in range(0, n % 4):
            board = rotate_ccw(board)
        return board

