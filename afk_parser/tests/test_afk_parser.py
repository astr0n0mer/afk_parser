import os
import sys
from datetime import datetime, time, timedelta

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from afk_parser.afk_parser import AFKParser
from lib.extended_datetime import extended_datetime
from lib.relativedelta import relativedelta


def format_datetime(d: datetime) -> str:
    return d.strftime("%Y-%m-%d %H:%M:%S")


@pytest.fixture()
def afk_parser() -> AFKParser:
    return AFKParser()


@pytest.mark.parametrize(
    "phrase, expected_datetimes",
    [
        #! start_time is now, calculate end_time
        ("afk for 0 min", (datetime.now(), datetime.now() + timedelta(minutes=0))),
        ("afk for -30 min", (datetime.now(), datetime.now() + timedelta(minutes=-30))),
        ("afk for 30 min", (datetime.now(), datetime.now() + timedelta(minutes=30))),
        ("afk for 30 mins", (datetime.now(), datetime.now() + timedelta(minutes=30))),
        ("afk for 60 mins", (datetime.now(), datetime.now() + timedelta(minutes=60))),
        ("afk for an hour", (datetime.now(), datetime.now() + timedelta(hours=1))),
        ("afk for 1 hour", (datetime.now(), datetime.now() + timedelta(hours=1))),
        ("afk for 1 hr", (datetime.now(), datetime.now() + timedelta(hours=1))),
        ("afk for 3h", (datetime.now(), datetime.now() + timedelta(hours=3))),
        ("afk for 3hr", (datetime.now(), datetime.now() + timedelta(hours=3))),
        ("afk for 3 hours", (datetime.now(), datetime.now() + timedelta(hours=3))),
        (
            "afk till 8am",
            (
                datetime.now(),
                datetime.now().replace(hour=8, minute=0, second=0, microsecond=0),
            ),
        ),
        (
            "afk till 12am",
            (
                datetime.now(),
                datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
            ),
        ),
        (
            "afk till 8pm",
            (
                datetime.now(),
                datetime.now().replace(hour=20, minute=0, second=0, microsecond=0),
            ),
        ),
        (
            "afk till 12pm",
            (
                datetime.now(),
                datetime.now().replace(hour=12, minute=0, second=0, microsecond=0),
            ),
        ),
        ("afk today", (datetime.now(), datetime.combine(datetime.now(), time.max))),
        (
            "afk tomorrow",
            (
                datetime.now(),
                datetime.combine(datetime.now() + timedelta(days=1), time.max),
            ),
        ),
        (
            "afk for 2 days",
            (
                datetime.now(),
                datetime.combine(datetime.now() + timedelta(days=2), time.max),
            ),
        ),
        (
            "afk for 10 days",
            (
                datetime.now(),
                datetime.combine(datetime.now() + timedelta(days=10), time.max),
            ),
        ),
        (
            "afk for a week",
            (
                datetime.now(),
                datetime.combine(datetime.now() + timedelta(weeks=1), time.max),
            ),
        ),
        (
            "afk for 1 week",
            (
                datetime.now(),
                datetime.combine(datetime.now() + timedelta(weeks=1), time.max),
            ),
        ),
        (
            "afk for 3 weeks",
            (
                datetime.now(),
                datetime.combine(datetime.now() + timedelta(weeks=3), time.max),
            ),
        ),
        (
            "afk for 1 month",
            (
                datetime.now(),
                datetime.combine(
                    extended_datetime.now() + relativedelta(months=1), time.max
                ),
            ),
        ),
        (
            "afk for 6 months",
            (
                datetime.now(),
                datetime.combine(
                    extended_datetime.now() + relativedelta(months=6), time.max
                ),
            ),
        ),
        (
            "afk for 12 months",
            (
                datetime.now(),
                datetime.combine(
                    extended_datetime.now() + relativedelta(months=12), time.max
                ),
            ),
        ),
        (
            "afk for -1 month",
            (
                datetime.now(),
                datetime.combine(
                    extended_datetime.now() + relativedelta(months=-1), time.max
                ),
            ),
        ),
        (
            "afk for -6 months",
            (
                datetime.now(),
                datetime.combine(
                    extended_datetime.now() + relativedelta(months=-6), time.max
                ),
            ),
        ),
        (
            "afk for -12 months",
            (
                datetime.now(),
                datetime.combine(
                    extended_datetime.now() + relativedelta(months=-12), time.max
                ),
            ),
        ),
        (
            "afk for 1 year",
            (
                datetime.now(),
                datetime.combine(
                    extended_datetime.now() + relativedelta(years=1), time.max
                ),
            ),
        ),
        (
            "afk for 2 years",
            (
                datetime.now(),
                datetime.combine(
                    extended_datetime.now() + relativedelta(years=2), time.max
                ),
            ),
        ),
        (
            "afk for -1 year",
            (
                datetime.now(),
                datetime.combine(
                    extended_datetime.now() + relativedelta(years=-1), time.max
                ),
            ),
        ),
        (
            "afk for -2 years",
            (
                datetime.now(),
                datetime.combine(
                    extended_datetime.now() + relativedelta(years=-2), time.max
                ),
            ),
        ),
        (
            "will start late at 11am",
            (
                datetime.now(),
                datetime.now().replace(hour=11, minute=0, second=0, microsecond=0),
            ),
        ),
        (
            "will start late today at 11am",
            (
                datetime.now(),
                datetime.now().replace(hour=11, minute=0, second=0, microsecond=0),
            ),
        ),
        (
            "will start late at 11am tomorrow",
            (
                datetime.now(),
                datetime.now().replace(hour=11, minute=0, second=0, microsecond=0)
                + timedelta(days=1),
            ),
        ),
        (
            "will start late by 12pm tomorrow",
            (
                datetime.now(),
                datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
                + timedelta(days=1),
            ),
        ),
        (
            "will start late by 1pm tomorrow",
            (
                datetime.now(),
                datetime.now().replace(hour=13, minute=0, second=0, microsecond=0)
                + timedelta(days=1),
            ),
        ),
        (
            "will start late by 1pm on monday",
            (
                datetime.now(),
                datetime.now().replace(hour=13, minute=0, second=0, microsecond=0)
                + timedelta(days=7 - datetime.now().weekday()),
            ),
        ),
        #! calculate start_time, end_time is EOD
        (
            "afk post 5pm",
            (
                datetime.now().replace(hour=17, minute=0, second=0, microsecond=0),
                datetime.combine(datetime.now(), time.max),
            ),
        ),
        (
            "afk post 5:30pm",
            (
                datetime.now().replace(hour=17, minute=30, second=0, microsecond=0),
                datetime.combine(
                    datetime.now().replace(hour=17, minute=30, second=0, microsecond=0),
                    time.max,
                ),
            ),
        ),
        (
            "afk from 5pm",
            (
                datetime.now().replace(hour=17, minute=0, second=0, microsecond=0),
                datetime.combine(
                    datetime.now().replace(hour=17, minute=0, second=0, microsecond=0),
                    time.max,
                ),
            ),
        ),
        (
            "afk from 5:30pm",
            (
                datetime.now().replace(hour=17, minute=30, second=0, microsecond=0),
                datetime.combine(
                    datetime.now().replace(hour=17, minute=30, second=0, microsecond=0),
                    time.max,
                ),
            ),
        ),
        (
            "afk after 5pm",
            (
                datetime.now().replace(hour=17, minute=0, second=0, microsecond=0),
                datetime.combine(
                    datetime.now().replace(hour=17, minute=0, second=0, microsecond=0),
                    time.max,
                ),
            ),
        ),
        (
            "afk after 5:30pm",
            (
                datetime.now().replace(hour=17, minute=30, second=0, microsecond=0),
                datetime.combine(
                    datetime.now().replace(hour=17, minute=30, second=0, microsecond=0),
                    time.max,
                ),
            ),
        ),
        #! calculate both start_time and end_time
        (
            "afk on monday",
            (
                datetime.combine(datetime.now(), time.min)
                + timedelta(
                    days=7 - datetime.now().weekday()
                ),  # ? should this be just datetime.now()
                datetime.combine(datetime.now(), time.max)
                + timedelta(days=7 - datetime.now().weekday()),
            ),
        ),
        (
            "afk from 4pm for 1 hr",
            (
                datetime.now().replace(hour=16, minute=0, second=0, microsecond=0),
                datetime.now().replace(hour=16, minute=0, second=0, microsecond=0)
                + timedelta(hours=1, seconds=-1),
            ),
        ),
        (
            "afk after 5pm for 2 hr",
            (
                datetime.now().replace(hour=17, minute=0, second=0, microsecond=0),
                datetime.now().replace(hour=17, minute=0, second=0, microsecond=0)
                + timedelta(hours=2, seconds=-1),
            ),
        ),
    ],
)
def test_extract_datetime(
    afk_parser: AFKParser, phrase: str, expected_datetimes: tuple[datetime, datetime]
) -> None:
    result = afk_parser.parse_dates(phrase=phrase)
    assert result is not None, f"Couldn't parse phrase: {phrase}"
    start_datetime, end_datetime = result
    expected_start_datetime, expected_end_datetime = expected_datetimes
    assert format_datetime(start_datetime) == format_datetime(expected_start_datetime)
    assert format_datetime(end_datetime) == format_datetime(expected_end_datetime)
