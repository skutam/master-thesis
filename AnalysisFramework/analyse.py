from os.path import isfile, realpath

from src import Analysis
from sys import argv, stderr

if __name__ == '__main__':
    if len(argv) != 2:
        print('Please provide as second argument the required text file to be analysed.', file=stderr)
        exit(1)

    if not isfile(argv[1]):
        print(f'Please provide valid file because file: {argv[1]}, could not be found')
        exit(1)

    filepath = realpath(argv[1])

    analysis = Analysis()
    analysis.run_analysis(filepath)
