from datetime import datetime
import sys

from afk_parser.afk_parser import AFKParser


def main():
    if len(sys.argv) > 1:
        utc_offset_seconds = datetime.now().astimezone().utcoffset().total_seconds()
        result = AFKParser().parse_dates(
            phrase=sys.argv[1], tz_offset=utc_offset_seconds
        )
        for timestamp in result:
            print(timestamp)
    else:
        print(f'Usage: python {__file__}.py "afk from 5pm"')


if __name__ == "__main__":
    main()
