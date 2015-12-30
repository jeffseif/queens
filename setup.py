#! /usr/bin/env python3
from setuptools import setup
from queens import __author__
from queens import __email__
from queens import __program__
from queens import __url__
from queens import __version__


setup(
    author=__author__,
    author_email=__email__,
    install_requires=[],
    name=__program__,
    packages=[__program__],
    platforms='all',
    setup_requires=[
        'setuptools',
        'tox',
    ],
    test_suite='tests',
    tests_require=['pytest'],
    url=__url__,
    version=__version__,
)
