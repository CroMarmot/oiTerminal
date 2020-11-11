#!/usr/bin/env python3

import argparse


def main():
    parser = argparse.ArgumentParser(description='oiTerminal cli')
    parser.add_argument('ops', metavar='params', type=str, nargs='+',
                        help='an integer for the accumulator')

    args = parser.parse_args()
    folder = '.oiTerminal'

    ops = args.ops
    if ops[0] == 'problem':
        from oiTerminal.cli import problem
        problem.main(argv=ops[1:], folder=folder)
    elif ops[0] == 'config':
        from oiTerminal.cli import config
        config.main(folder=folder)
    elif ops[0] == 'init':
        from oiTerminal.cli import init
        init.main(folder=folder)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
