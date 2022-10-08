from queens import __author__
from queens import __version__
from queens import __year__
from queens.matrix import Matrix
from queens.solution import Solution


DEFAULT_SIZE = 8


def main():
    import argparse

    __version__author__year__ = "{} | {} {}".format(
        __version__,
        __author__,
        __year__,
    )

    parser = argparse.ArgumentParser(
        description="N-queens solver",
        epilog="Version {}".format(__version__author__year__),
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s {}".format(__version__author__year__),
    )
    parser.add_argument(
        "size",
        nargs="?",
        default=DEFAULT_SIZE,
        type=int,
        help="Number of queens (e.g., %(default)s)",
    )
    args = parser.parse_args()

    matrix = Matrix(size=args.size)
    for index, solution in enumerate(matrix.solve()):
        print(index)
        print(Solution(solution))


if __name__ == "__main__":
    import sys

    sys.exit(main())
