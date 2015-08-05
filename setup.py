from setuptools import setup
from budget._version import __version__

setup(
    name = 'budget',
    version = __version__,
    url = 'https://github.com/dfroger/budget',
    description = 'Personal budgeting script',
    license = 'GPL V3',
    author = 'David Froger',
    author_email = 'david.froger@mailoo.org',
    packages = ['budget'],
    entry_points = {
        'console_scripts': [
            'budget = budget.cli:main',
        ],
    },
)
