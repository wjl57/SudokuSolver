import json
import os
from flask import Flask, jsonify, request
from flask.json import JSONEncoder
from flask_restful import abort, Api
from SudokuLogger import SudokuStepLog
from SudokuPuzzle import SudokuPuzzle
from SudokuSolver import SudokuSolver

__author__ = 'william'


class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, list):
            return json.dumps(obj)
        if isinstance(obj, SudokuStepLog):
            return obj.to_json()
        return super(MyJSONEncoder, self).default(obj)

app = Flask(__name__, static_folder="public")
app.json_encoder = MyJSONEncoder
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
api = Api(app)


@app.route('/')
@app.route('/index')
def index():
    # return "Hello, World!"
    try:
        return app.send_static_file('index.html')
    except Exception as e:
        print(e)


@app.route('/api/sudoku/calc_possibilities', methods=['POST'])
def calculate_possibilities():
    board = request.json['board']
    sp = SudokuPuzzle(board)
    return jsonify({'possibilities': sp.get_possibilities()})


@app.route('/api/sudoku/solve_step', methods=['POST'])
def solve_step():
    board = request.json['board']
    sp = SudokuPuzzle(board)
    ss = SudokuSolver(sp)
    ss.solve_next_step()
    log = ss.sudoku_logger.sudoku_log
    try:
        return jsonify({'board': ss.sudoku_puzzle.get_board(), 'steps_log': log})
    except Exception as e:
        print(e)


@app.route('/api/sudoku/solve_puzzle', methods=['POST'])
def solve_puzzle():
    print(request.json)
    print(request.json['board'])
    # params = request.json.to_dict()
    # print(params)
    board = request.json['board']
    sp = SudokuPuzzle(board)
    ss = SudokuSolver(sp)
    ss.do_work()
    log = ss.sudoku_logger.sudoku_log
    try:
        return jsonify({'board': ss.sudoku_puzzle.get_board(), 'steps_log': log})
    except Exception as e:
        print(e)

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 8000)))
