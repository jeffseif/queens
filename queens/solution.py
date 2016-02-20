# -*- coding: utf-8 -*-
from queens import GRAY
from queens import WHITE


class Solution:

    BAR = GRAY('|')
    EMPTY = WHITE('.')
    QUEEN = WHITE('♕')

    def __init__(self, solution):
        self.process(solution)
        self.size = len(solution)
        self.LINE = GRAY('+' + '-' * (2 * self.size + 1) + '+')

    def process(self, solution):
        self.positions = {
            tuple(
                link.column.name[1]
                for link in row.loop('right', include=True)
            )[: 2]
            for row in solution
        }

    def __str__(self):
        return '\n'.join(
            self.row_iter()
        )

    def row_iter(self):
        yield self.LINE
        for index in range(self.size):
            row = [self.BAR]
            row.extend(
                self.QUEEN if (index, jndex) in self.positions else self.EMPTY
                for jndex in range(self.size)
            )
            row.append(self.BAR)
            yield ' '.join(row)
        yield self.LINE
