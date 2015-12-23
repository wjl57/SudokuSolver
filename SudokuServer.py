import os
from flask_restful import abort, Api
# from SudokuPuzzle import SudokuPuzzle
# from SudokuSolver import SudokuSolver

__author__ = 'william'

from flask import Flask, jsonify, request

app = Flask(__name__)
api = Api(app)


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/api/sudoku/solvepuzzle', methods=['POST'])
def solve_puzzle():
    # if not request.json or not 'board' in request.json:
    #     abort(400)
    board = [[1,2,3],[4,5,6]]
    # board = request.json['board']
    return jsonify(board=board)

#     if not request.json or not 'board' in request.json:
#         abort(400)

    # request.json['board']
    # ss = SudokuSolver(SudokuPuzzle(request.json['board']))

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 8000)))
