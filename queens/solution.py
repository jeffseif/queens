# -*- coding: utf-8 -*-
from queens import GRAY
from queens import PREFIXES
from queens import WHITE


class Solution:

    BAR = GRAY('|')
    EMPTY = WHITE('.')
    QUEEN = WHITE('♕')

    def __init__(self, solution):
        self.process(solution)
        self.LINE = GRAY('+' + '-' * (2 * self.size + 1) + '+')

    def process(self, solution):
        positions = set(
            tuple(
                link.column.name
                for link in row.loop('right', include=True)
            )[: 2]
            for row in solution
        )

        self.size = len(solution)
        self.positions = [
            [
                self.ij_to_columns(index, jndex) in positions
                for jndex in range(self.size)
            ]
            for index in range(self.size)
        ]

    @staticmethod
    def ij_to_columns(index, jndex):
        return '{}{}'.format(PREFIXES[0], index), '{}{}'.format(PREFIXES[1], jndex)

    def __str__(self):
        return '\n'.join(
            self.row_iter()
        )

    def row_iter(self):
        yield self.LINE
        for index in range(self.size):
            row = [self.BAR]
            row.extend(
                self.QUEEN if self.positions[index][jndex] else self.EMPTY
                for jndex in range(self.size)
            )
            row.append(self.BAR)
            yield ' '.join(row)
        yield self.LINE
