"""Console entry point"""

from argparse import ArgumentParser
from sys import stderr


def run():

    parser = ArgumentParser(description='PopArt networks')

    parser.add_argument('input', type=str, help='Path to input file')
    parser.add_argument('output', type=str, help='Path to output file')

    parser.add_argument('--mst', type=bool, default=False, help='Build minimum spanning tree network')
    parser.add_argument('--mjt', type=bool, default=False, help='Build median joining network')
    parser.add_argument('--tsw', type=bool, default=False, help='Build tight span walker network')
    parser.add_argument('--tcs', type=bool, default=False, help='Build TCS network')

    parser.parse_args()

    print('Not implemented yet...', file=stderr)


if __name__ == '__main__':
    run()
