class Solution:

    def __init__(self, solution):
        self.solution = solution

    def __str__(self):
        return '\n'.join(
            ','.join(map(str, row.loop('right', include=True)))
            for row in self.solution
        )
