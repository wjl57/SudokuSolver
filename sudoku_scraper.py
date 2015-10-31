import requests
import pickle
from bs4 import BeautifulSoup
from SudokuBoard import SudokuBoard

__author__ = 'william'


def main():
    # board = save_and_get_new_board()
    board = read_saved_board(2)
    sb = SudokuBoard(board)
    sb.print_board()
    print(sb.board)
    print(sb.rows)
    print(sb.cols)
    print(sb.blocks)
    print("Num unknowns: ", sb.num_unknowns)
    # while not sb.verify_board_full():
    #     sb.solve_next_step()
    #     sb.print_board()
    #     print("Num unknowns: ", sb.num_unknowns)

    # nc = sb.row_to_numbered_cells(0)
    # print(nc)
    # nc = sb.col_to_numbered_cells(0)
    # print(nc)
    # nc = sb.block_to_numbered_cells(0)
    # print(nc)
    # d = SudokuBoard.find_val_with_count_in_numbered_cells(sb.remaining_blocks[2], nc, 1)
    # print(d)
    # sb.set_board_with_block_values(2, d)
    # sb.calculate_possibilities()
    # sb.print_board()


def save_and_get_new_board():
    url = "http://show.websudoku.com/"
    response = requests.get(url)
    html = response.content

    soup = BeautifulSoup(html, "html.parser")

    puzzle_grid = soup.find(id="puzzle_grid")

    board = [[None for _ in range(0, 9)] for _ in range(0, 9)]
    for i in range(0, 9):
        for j in range(0, 9):
            dom_id = "c" + str(i) + str(j)
            square = puzzle_grid.find(id=dom_id)
            # print(square.prettify())
            try:
                value = int(square.find('input').get('value'))
                if value is not None:
                    board[i][j] = value
            except:
                pass
    file = open('boards.txt', 'ab')
    pickle.dump(board, file)
    return board


def read_saved_board(num):
    file = open('boards.txt', 'rb')
    for i in range(0, num):
        pickle.load(file)
    return pickle.load(file)



if __name__ == "__main__": main()
