#! /usr/bin/env python3


FLIP = {
    'l': 'r',
    'r': 'l',
    'u': 'd',
    'd': 'u',
}
SIZE = 4


def loop_iter(*heads):
    for head in heads:
        yield from head.loop('r')


class Link:

    def __init__(self, l=None, r=None, u=None, d=None, column=None, size=0, name=''):
        self.l = l
        self.r = r
        self.u = u
        self.d = d
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
        self.l.r = self.r
        self.r.l = self.l

        for row in self.loop('d'):
            for link in row.loop('r'):
                link.d.u = link.u
                link.u.d = link.d
                link.column.size -= 1

    def uncover(self):
        for row in self.loop('u'):
            for link in row.loop('l'):
                link.column.size += 1
                link.d.u = link
                link.u.d = link

        self.r.l = self
        self.l.r = self


class Web:

    def __init__(self):
        self.make_primary_columns()
        self.make_secondary_columns()
        self.make_links()

    def make_primary_columns(self):
        self.primary = Link(name='primary')
        self.primary.pend(self.primary, 'r')
        previous = self.primary
        for prefix in ('R', 'F'):
            for index in range(SIZE):
                name = '{}{}'.format(prefix, index)
                column = Link(name=name)
                column.pend(column, 'u')

                previous.pend(column, 'r')
                previous = column

    def make_secondary_columns(self):
        self.secondary = Link(name='secondary')
        self.secondary.pend(self.secondary, 'r')
        previous = self.secondary
        for prefix in ('A', 'B'):
            for index in range(2 * SIZE - 1):
                name = '{}{}'.format(prefix, index)
                column = Link(name=name)
                column.pend(column, 'u')

                previous.pend(column, 'r')
                previous = column

    def make_links(self):
        for index in range(SIZE):
            for jndex in range(SIZE):
                name_i = 'R{}'.format(index)
                name_j = 'F{}'.format(jndex)
                name_a = 'A{}'.format(index + jndex)
                name_b = 'B{}'.format(SIZE - 1 - index + jndex)

                previous = None
                for column in loop_iter(self.primary, self.secondary):
                    if column.name in (name_i, name_j, name_a, name_b):
                        link = Link(column=column,name=column.name)
                        column.pend(link, 'u')
                        column.size += 1

                        if previous is None:
                            link.pend(link, 'r')
                        else:
                            previous.pend(link, 'r')
                        previous = link

    def print_column_rows(self):
        for column in loop_iter(self.primary, self.secondary):
            print(column, ': ', ','.join(map(str, column.loop('d'))))

    def print_column_sizes(self):
        for column in loop_iter(self.primary, self.secondary):
            print(column, column.size)


def search(head, solution):
    column = head.r
    if column == head:
        for row in solution:
            print(','.join(map(str, row.loop('r', include=True))))
        exit()
    else:
        size = SIZE ** 2
        the_column = None
        for column in head.loop('r'):
            if column.size < size:
                size = column.size
                the_column = column
        column = the_column

    column.cover()

    for row in column.loop('d'):

        solution.append(row)
        for link in row.loop('r'):
            link.column.cover()
        search(head, solution)

        row = solution.pop()
        for link in row.loop('l'):
            link.column.uncover()

    column.uncover()


def main():
    web = Web()
    web.print_column_rows()
    web.print_column_sizes()
    # print_links(l)
    search(web.primary, [])


if __name__ == '__main__':
    main()
