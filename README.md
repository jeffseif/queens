queens
======

A solution to the [n-queens problem](https://en.wikipedia.org/wiki/Eight_queens_puzzle).

Casting the game as a [set cover problem](https://en.wikipedia.org/wiki/Set_cover_problem), it is solved using [the DLX algorithm](http://arxiv.org/abs/cs/0011047v1).
This project is a stepping-stone to a better algorithm for [my sudoku project](http://github.com/jeffseif/sudoku).

Entering virtualenv
-------------------

    > virtualenv venv --python=$(which python3) && source venv/bin/activate

Example invocation
------------------

    > make && ./queens/main.py --help
    ...
    usage: main.py [-h] [--version] [size]

    N-queens solver

    positional arguments:
      size        Number of queens (e.g., 8)

      optional arguments:
        -h, --help  show this help message and exit
          --version   show program's version number and exit

          Version 1.0.0 | Jeffrey Seifried 2016

    > make && ./queens/main.py 4
    ...
    0
    R0,F1,A1,B4
    R1,F3,A4,B5
    R2,F0,A2,B1
    R3,F2,A5,B2
    1
    R0,F2,A2,B5
    R1,F0,A1,B2
    R2,F3,A5,B4
    R3,F1,A4,B1

How to run unit tests
---------------------

    > make test
