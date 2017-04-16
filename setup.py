from setuptools import setup

from queens import __author__
from queens import __email__
from queens import __program__
from queens import __url__
from queens import __version__


setup(
    author=__author__,
    author_email=__email__,
    dependency_links=[
        'https://github.com/jeffseif/colors.git#egg=colors',
    ],
    install_requires=[],
    name=__program__,
    packages=[__program__],
    platforms='all',
    setup_requires=[
        'setuptools',
        'tox',
    ],
    test_suite='tests',
    url=__url__,
    version=__version__,
)
