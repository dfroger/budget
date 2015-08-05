#!/usr/bin/env python

import budget 

import argparse

def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', metavar='FILE.BUDGET',
        help="Account file to read.")
    args = parser.parse_args()
    return args

def main():
    args = parse_command_line()
    a = budget.Account.from_file(args.filepath)
    print(a.make_report())

if __name__ == '__main__':
    main()

