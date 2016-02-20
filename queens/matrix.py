from queens import PREFIXES
from queens.link import Link


class Matrix:
    """A data structure for DLX (dancing links algorithm X).  (Doubly-linked)
    head Links link to a list of column Links -- corresponding to constraints
    for the set cover problem.  Column Links additionally link to rows which
    link to their own list of contraints they cover -- corresponding to choices
    or possible configurations which assemble to a solution.
    """

    def __init__(self, size):
        self.size = size
        self.solution = []

        self.make_primary_columns()
        self.make_secondary_columns()
        self.make_and_attach_rows()

    def make_primary_columns(self):
        self.primary = Link(name='primary')
        self.primary.attach(self.primary, 'right')
        previous = self.primary
        for prefix in PREFIXES[: 2]:
            for index in range(self.size):
                name = (prefix, index)
                column = Link(name=name)
                column.attach(column, 'up')

                previous.attach(column, 'right')
                previous = column

    def make_secondary_columns(self):
        self.secondary = Link(name='secondary')
        self.secondary.attach(self.secondary, 'right')
        previous = self.secondary
        for prefix in PREFIXES[2:]:
            for index in range(2 * self.size - 1):
                name = (prefix, index)
                column = Link(name=name)
                column.attach(column, 'up')

                previous.attach(column, 'right')
                previous = column

    def make_and_attach_rows(self):
        for index in range(self.size):
            for jndex in range(self.size):
                names = self.get_names_from_ij(self.size, index, jndex)

                previous = None
                for column in self.column_link_iter():
                    if column.name in names:
                        row = Link(column=column, name=column.name)
                        column.attach(row, 'up')
                        column.size += 1

                        if previous is None:
                            row.attach(row, 'right')
                        else:
                            previous.attach(row, 'right')
                        previous = row

    @staticmethod
    def get_names_from_ij(size, index, jndex):
        return (
            # Rank
            (PREFIXES[0], index),
            # File
            (PREFIXES[1], jndex),
            # Diagonal a
            (PREFIXES[2], index + jndex),
            # Diagonal b
            (PREFIXES[3], size - 1 - index + jndex),
        )

    def column_link_iter(self):
        for head in (self.primary, self.secondary):
            yield from head.loop('right')

    def print_columns(self):
        print(','.join(map(str, self.column_link_iter())))

    def print_column_rows(self):
        for column in self.column_link_iter():
            print('{}:'.format(column), ','.join(map(str, column.loop('down'))))

    def solve(self):
        yield from self.search(self.primary, self.solution)

    def search(self, head, solution):
        """The heart of the DLX algorithm."""
        column = head.right
        if column == head:
            yield solution
            return
        else:
            column = self.find_column_of_smallest_size(head)

        column.cover()

        for row in column.loop('down'):

            solution.append(row)
            for link in row.loop('right'):
                link.column.cover()

            yield from self.search(head, solution)

            for link in solution.pop().loop('left'):
                link.column.uncover()

        column.uncover()

    @staticmethod
    def find_column_of_smallest_size(head):
        size = int(1e9)
        smallest = None
        for column in head.loop('right'):
            if column.size < size:
                size = column.size
                smallest = column
        return smallest
