__author__ = 'Jeffrey Seifried'
__email__ = 'jeffrey.seifried@gmail.com'
__program__ = 'queens'
__url__ = 'http://github.com/jeffseif/{}'.format(__program__)
__version__ = '1.0.0'
__year__ = '2016'

PREFIXES = ('R', 'F', 'A', 'B')


def Colorize(color, weight=1):
    """Function for bash-style color formatting."""
    def inner(value):
        return template.format(value)

    template = '\033[{:d};{:d}m{{:s}}\033[0m'.format(weight, color)
    return inner


GRAY = Colorize(90)
WHITE = Colorize(37)
