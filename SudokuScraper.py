import requests
import pickle
from bs4 import BeautifulSoup
from SudokuPuzzle import SudokuPuzzle
from SudokuSolver import SudokuSolver

__author__ = 'william'


def main():
    # board = save_and_get_new_board(4)
    # print(board)
    # board = read_saved_board(11)
    board = [
        [2, 8, None, None, None, None, 4, 7, 3],
        [5, 3, 4, 8, 2, 7, 1, 9, 6],
        [None, 7, 1, None, 3, 4, None, 8, None],
        [3, None, None, 5, None, None, None, 4, None],
        [None, None, None, 3, 4, None, None, 6, None],
        [4, 6, None, 7, 9, None, 3, 1, None],
        [None, 9, None, 2, None, 3, 6, 5, 4],
        [None, None, 3, None, None, 9, 8, 2, 1],
        [None, None, None, None, 8, None, 9, 3, 7]
    ]
    sp = SudokuPuzzle(board)
    # sp.print_board()

    ss = SudokuSolver(sp)
    ss.do_work()

    # for i in range(0, 8):
    #     filled_cells = sp.fill_unique_candidates()
    #     print("unique candidates " + str(i) + " : " + str(filled_cells))
    #     sp.print_board()
    #     # sp.print_possibilities()
    #     filled_cells = sp.fill_sole_candidates()
    #     print("sole candidates " + str(i) + " : " + str(filled_cells))
    #     sp.print_board()
    #     # sp.print_possibilities()


def save_and_get_new_board(level=1):
    url = "http://show.websudoku.com/" + "?level=" + str(level)
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
