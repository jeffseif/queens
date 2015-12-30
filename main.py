#! /usr/bin/env python3


FLIP = {
    'left': 'right',
    'right': 'left',
    'up': 'down',
    'down': 'up',
}
SIZE = 8


def get_smallest_column(head):
    size = SIZE ** 2
    smallest = None
    for column in head.loop('right'):
        if column.size < size:
            size = column.size
            smallest = column
    return smallest


class Link:

    def __init__(self, left=None, right=None, up=None, down=None, column=None, size=0, name=''):
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.column = column
        self.size = size
        self.name = name

    def __str__(self):
        return self.name

    def loop(self, direction, include=False):
        if include:
            yield self

        link = getattr(self, direction)
        while link != self:
            yield link
            link = getattr(link, direction)

    def pend(self, other, direction):
        link = getattr(self, direction)

        setattr(self, direction, other)
        setattr(other, FLIP[direction], self)

        if link is not None:
            setattr(link, FLIP[direction], other)
            setattr(other, direction, link)

    def cover(self):
        self.left.right = self.right
        self.right.left = self.left

        for row in self.loop('down'):
            for link in row.loop('right'):
                link.down.up = link.up
                link.up.down = link.down
                link.column.size -= 1

    def uncover(self):
        for row in self.loop('up'):
            for link in row.loop('left'):
                link.column.size += 1
                link.down.up = link
                link.up.down = link

        self.right.left = self
        self.left.right = self


class Web:

    def __init__(self):
        self.make_primary_columns()
        self.make_secondary_columns()
        self.make_links()

    def column_iter(self):
        for head in (self.primary, self.secondary):
            yield from head.loop('right')

    def make_primary_columns(self):
        self.primary = Link(name='primary')
        self.primary.pend(self.primary, 'right')
        previous = self.primary
        for prefix in ('R', 'F'):
            for index in range(SIZE):
                name = '{}{}'.format(prefix, index)
                column = Link(name=name)
                column.pend(column, 'up')

                previous.pend(column, 'right')
                previous = column

    def make_secondary_columns(self):
        self.secondary = Link(name='secondary')
        self.secondary.pend(self.secondary, 'right')
        previous = self.secondary
        for prefix in ('A', 'B'):
            for index in range(2 * SIZE - 1):
                name = '{}{}'.format(prefix, index)
                column = Link(name=name)
                column.pend(column, 'up')

                previous.pend(column, 'right')
                previous = column

    def make_links(self):
        for index in range(SIZE):
            for jndex in range(SIZE):
                name_i = 'R{}'.format(index)
                name_j = 'F{}'.format(jndex)
                name_a = 'A{}'.format(index + jndex)
                name_b = 'B{}'.format(SIZE - 1 - index + jndex)

                previous = None
                for column in self.column_iter():
                    if column.name in (name_i, name_j, name_a, name_b):
                        link = Link(column=column,name=column.name)
                        column.pend(link, 'up')
                        column.size += 1

                        if previous is None:
                            link.pend(link, 'right')
                        else:
                            previous.pend(link, 'right')
                        previous = link

    def print_columns(self):
        print(','.join(map(str, self.column_iter())))

    def print_column_rows(self):
        for column in self.column_iter():
            print('{}:'.format(column), ','.join(map(str, column.loop('down'))))

    def solve(self):
        yield from self.search(self.primary, [])

    def search(self, head, solution):
        column = head.right
        if column == head:
            yield solution
            return
        else:
            column = get_smallest_column(head)

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
    web = Web()
    web.print_columns()
    web.print_column_rows()
    for index, solution in enumerate(web.solve()):
        print(index)
        print_solution(solution)


if __name__ == '__main__':
    main()
