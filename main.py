from datetime import datetime
import sys

from afk_parser.afk_parser import AFKParser


def main():
    if len(sys.argv) != 2:
        print(f'Usage: python {__file__}.py "afk from 5pm"')

    utc_offset_timedelta = datetime.now().astimezone().utcoffset()
    assert utc_offset_timedelta
    utc_offset_seconds = utc_offset_timedelta.total_seconds()
    result = AFKParser().parse_dates(phrase=sys.argv[1], tz_offset=utc_offset_seconds)
    assert result
    for timestamp in result:
        print(timestamp)


if __name__ == "__main__":
    main()
