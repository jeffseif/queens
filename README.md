# queens

A solution to the [n-queens puzzle](https://en.wikipedia.org/wiki/Eight_queens_puzzle).

Casting the puzzle as a [set cover problem](https://en.wikipedia.org/wiki/Set_cover_problem), it is solved using [the DLX algorithm](http://arxiv.org/abs/cs/0011047v1).
This project is a stepping-stone to a better algorithm for [my sudoku project](http://github.com/jeffseif/sudoku).

## Installation

    > pip install -e git+https://github.com/jeffseif/queens.git#egg=queens

## Development

    > git clone git@github.com:jeffseif/queens.git
    > cd queens
    > virtualenv venv --python=$(which python3)
    > source venv/bin/activate
    > make
    > make test

## Example invocation

    > ./queens/main.py --help
    usage: main.py [-h] [--version] [size]

    N-queens solver

    positional arguments:
      size        Number of queens (e.g., 8)

      optional arguments:
        -h, --help  show this help message and exit
          --version   show program's version number and exit

          Version 1.0.0 | Jeffrey Seifried 2016

    > ./queens/main.py 4
    0
    +---------+
    | . ♕ . . |
    | . . . ♕ |
    | ♕ . . . |
    | . . ♕ . |
    +---------+
    1
    +---------+
    | . . ♕ . |
    | ♕ . . . |
    | . . . ♕ |
    | . ♕ . . |
    +---------+
