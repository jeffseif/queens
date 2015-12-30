#! /usr/bin/env python3
from queens import __version__
from queens import __author__
from queens import __year__


FLIP = {
    'left': 'right',
    'right': 'left',
    'up': 'down',
    'down': 'up',
}
DEFAULT_SIZE = 8


def find_column_of_smallest_size(head):
    size = int(1e9)
    smallest = None
    for column in head.loop('right'):
        if column.size < size:
            size = column.size
            smallest = column
    return smallest


class Link:
    """Two-dimensional doubly-linked list element, with an associated column.
    Only column-type Link instances have a size (the number of child Links)
    and a name (for pretty printing)."""

    __slots__ = [
        'left',
        'right',
        'up',
        'down',
        'column',
        'size',
        'name',
    ]

    def __init__(self, column=None, name=''):
        self.column = column
        self.name = name

        self.size = 0
        self.left = self.right = self.up = self.down = None

    def __str__(self):
        return self.name

    def loop(self, direction, include=False):
        """Traverse doubly-linked-list Links in a loop of a certain direction."""
        if include:
            yield self

        link = getattr(self, direction)
        while link != self:
            yield link
            link = getattr(link, direction)

    def attach(self, other, direction):
        """Attach a Link on one side."""
        link = getattr(self, direction)

        setattr(self, direction, other)
        setattr(other, FLIP[direction], self)

        if link is not None:
            setattr(link, FLIP[direction], other)
            setattr(other, direction, link)

    def cover(self):
        """In the set cover problem sense: consider the column-type Link as
        being covered and thus remove it from the Web of Links which remain
        to be covered."""
        self.left.right = self.right
        self.right.left = self.left

        for row in self.loop('down'):
            for link in row.loop('right'):
                link.down.up = link.up
                link.up.down = link.down
                link.column.size -= 1

    def uncover(self):
        """The reverse of cover.  In the set cover problem sense: consider the
        column-type Link as not being covered and thus add it to the Web of
        Links which remain to be covered."""
        for row in self.loop('up'):
            for link in row.loop('left'):
                link.column.size += 1
                link.down.up = link
                link.up.down = link

        self.right.left = self
        self.left.right = self


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
            column = find_column_of_smallest_size(head)

        column.cover()

        for row in column.loop('down'):

            solution.append(row)
            for link in row.loop('right'):
                link.column.cover()

            yield from self.search(head, solution)

            for link in solution.pop().loop('left'):
                link.column.uncover()

        column.uncover()


def print_solution(solution):
    for row in solution:
        print(','.join(map(str, row.loop('right', include=True))))


def main():
    import argparse

    __version__author__year__ = '{} | {} {}'.format(
        __version__,
        __author__,
        __year__,
    )

    parser = argparse.ArgumentParser(
        description='N-queens solver',
        epilog='Version {}'.format(__version__author__year__)
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {}'.format(__version__author__year__),
    )
    parser.add_argument(
        'size',
        nargs='?',
        default=DEFAULT_SIZE,
        type=int,
        help='Number of queens (e.g., %(default)s)',
    )
    args = parser.parse_args()

    web = Web(size=args.size)
    for index, solution in enumerate(web.solve()):
        print(index)
        print_solution(solution)


if __name__ == '__main__':
    import sys
    sys.exit(main())
