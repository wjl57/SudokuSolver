from collections import Counter, defaultdict

__author__ = 'william'


class SudokuBoard:

    all_nums = set(i for i in range(1, 10))
    rows = [set() for _ in range(0, 9)]
    cols = [set() for _ in range(0, 9)]
    blocks = [set() for _ in range(0, 9)]
    remaining_rows = [set() for _ in range(0, 9)]
    # [all_nums.copy() for _ in range(0, 9)]
    remaining_cols = [set() for _ in range(0, 9)]
    # [all_nums.copy() for _ in range(0, 9)]
    remaining_blocks = [set() for _ in range(0, 9)]
    # [all_nums.copy() for _ in range(0, 9)]
    possibilities = [[set() for _ in range(0, 9)] for _ in range(0, 9)]
    board = None
    num_unknowns = 0

    def __init__(self, board):
        self.board = board
        self.calculate_possibilities()

    def calculate_possibilities(self):
        self.num_unknowns = 0
        for i in range(0, 9):
            for j in range(0, 9):
                val = self.board[i][j]
                if val is not None:
                    self.rows[i].add(val)
                    self.cols[j].add(val)
                    index = self.loc_to_block(i, j)
                    self.blocks[index].add(val)
                else:
                    self.num_unknowns += 1

        for i in range(0, 9):
            for j in range(0, 9):
                if self.board[i][j] is not None:
                    self.possibilities[i][j] = set()
                else:
                    self.possibilities[i][j] = self.all_nums - self.rows[i] - self.cols[j] \
                                               - self.blocks[self.loc_to_block(i, j)]
        for n in range(0, 9):
            self.remaining_rows[n] = self.all_nums.copy() - self.rows[n]
            self.remaining_cols[n] = self.all_nums.copy() - self.cols[n]
            self.remaining_blocks[n] = self.all_nums.copy() - self.blocks[n]

    def print_possibilities(self):
        for i in range(0, 9):
            for j in range(0, 9):
                print(i, j, self.board[i][j], self.possibilities[i][j])

    def fill_sole_candidates(self):
        for i in range(0, 9):
            for j in range(0, 9):
                if len(self.possibilities[i][j]) == 1:
                    self.board[i][j] = self.possibilities[i][j].pop()

    def fill_unique_candidates(self):
        for i in range(0, 9):
            d = defaultdict(int)
            for j in range(0, 9):
                for val in self.possibilities[i][j]:
                    d[val] += 1
            for val in d:
                if d[val] == 1:
                    self.board[i][j] = val
        for j in range(0, 9):
            d = defaultdict(int)
            for i in range(0, 9):
                for val in self.possibilities[i][j]:
                    d[val] += 1
            for val in d:
                if d[val] == 1:
                    self.board[i][j] = val

    def row_to_numbered_cells(self, row_num):
        numbered_cells = {}
        for i in range(0, 9):
            numbered_cells[i] = self.possibilities[row_num][i]
        return numbered_cells

    def col_to_numbered_cells(self, col_num):
        numbered_cells = {}
        for j in range(0, 9):
            numbered_cells[j] = self.possibilities[j][col_num]
        return numbered_cells

    def block_to_numbered_cells(self, block_num):
        numbered_cells = {}
        (x_block, y_block) = self.num_to_offsets(block_num)
        num = 0
        for x_offset in range(0, 3):
            for y_offset in range(0, 3):
                numbered_cells[num] = self.possibilities[x_block + x_offset][y_block + y_offset]
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

    # def verify_solution(self):
    #     for row in self.rows:
    #         if len(row) != 9:
    #             return False
    #     for col in self.cols:
    #         if len(col) != 9:
    #             return False
    #     for block in self.blocks:
    #         if len(block) != 9:
    #             return False
    #     return True

    @staticmethod
    def num_to_offsets(self):
        return self % 3, int(self / 3)

    def verify_board_full(self):
        return self.num_unknowns == 0

    @staticmethod
    def loc_to_block(r, c):
        return int(r/3)+int(c/3)*3

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

