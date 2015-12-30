from queens.link import Link


class Web:
    """A data structure for DLX (dancing links algorithm X).  (Doubly-linked)
    head Links link to a list of column Links -- corresponding to constraints
    for the set cover problem.  Column Links additionally link to rows which
    link to their own list of contraints they cover -- corresponding to choices
    or possible configurations which assemble to a solution.
    """

    def __init__(self, size):
        self.size = size

        self.make_primary_columns()
        self.make_secondary_columns()
        self.make_and_attach_rows()

    def column_link_iter(self):
        for head in (self.primary, self.secondary):
            yield from head.loop('right')

    def make_primary_columns(self):
        self.primary = Link(name='primary')
        self.primary.attach(self.primary, 'right')
        previous = self.primary
        for prefix in ('R', 'F'):
            for index in range(self.size):
                name = '{}{}'.format(prefix, index)
                column = Link(name=name)
                column.attach(column, 'up')

                previous.attach(column, 'right')
                previous = column

    def make_secondary_columns(self):
        self.secondary = Link(name='secondary')
        self.secondary.attach(self.secondary, 'right')
        previous = self.secondary
        for prefix in ('A', 'B'):
            for index in range(2 * self.size - 1):
                name = '{}{}'.format(prefix, index)
                column = Link(name=name)
                column.attach(column, 'up')

                previous.attach(column, 'right')
                previous = column

    def make_and_attach_rows(self):
        for index in range(self.size):
            for jndex in range(self.size):
                name_i = 'R{}'.format(index)
                name_j = 'F{}'.format(jndex)
                name_a = 'A{}'.format(index + jndex)
                name_b = 'B{}'.format(self.size - 1 - index + jndex)

                previous = None
                for column in self.column_link_iter():
                    if column.name in (name_i, name_j, name_a, name_b):
                        row = Link(column=column, name=column.name)
                        column.attach(row, 'up')
                        column.size += 1

                        if previous is None:
                            row.attach(row, 'right')
                        else:
                            previous.attach(row, 'right')
                        previous = row

    def print_columns(self):
        print(','.join(map(str, self.column_link_iter())))

    def print_column_rows(self):
        for column in self.column_link_iter():
            print('{}:'.format(column), ','.join(map(str, column.loop('down'))))

    def solve(self):
        yield from self.search(self.primary, [])

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
