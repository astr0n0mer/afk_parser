import sys

from lib.afk_parser import AFKParser


def main():
    if len(sys.argv) > 1:
        print(AFKParser().parse_dates(phrase=sys.argv[1]))
    else:
        print(f'Usage: python {__file__}.py "afk from 5pm"')


if __name__ == "__main__":
    main()
