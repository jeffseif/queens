queens
======

A Solution to the n-queens problem, using [the DLX algorithm](http://arxiv.org/abs/cs/0011047v1).
This is a stepping-stone to a better algorithm for [sudoku](http://github.com/jeffseif/sudoku).

How to run unit tests
---------------------

    > virtualenv venv --python=$(which python3) && source venv/bin/activate
    > make && ./queens/main.py
    > make test
