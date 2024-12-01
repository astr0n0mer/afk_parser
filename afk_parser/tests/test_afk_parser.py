import os
import sys
from datetime import datetime, time, timedelta, timezone

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from afk_parser.afk_parser import AFKParser
from dateutil.relativedelta import relativedelta


@pytest.fixture
def datetime_comparison_flex() -> timedelta:
    return timedelta(seconds=3)


@pytest.fixture()
def afk_parser() -> AFKParser:
    return AFKParser()


@pytest.mark.parametrize(
    "phrase, expected_datetimes",
    [
        # INFO: start_time is now, calculate end_time
        (
            "afk for 0 min",
            (datetime.now(), datetime.now() + timedelta(minutes=0)),
        ),
        (
            "afk for -30 min",
            (datetime.now(), datetime.now() + timedelta(minutes=-30)),
        ),
        (
            "afk for 30 min",
            (datetime.now(), datetime.now() + timedelta(minutes=30)),
        ),
        (
            "afk for 30 mins",
            (datetime.now(), datetime.now() + timedelta(minutes=30)),
        ),
        (
            "afk for 60 mins",
            (datetime.now(), datetime.now() + timedelta(minutes=60)),
        ),
        (
            "afk for an hour",
            (datetime.now(), datetime.now() + timedelta(hours=1)),
        ),
        (
            "afk for 1 hour",
            (datetime.now(), datetime.now() + timedelta(hours=1)),
        ),
        (
            "afk for 1 hr",
            (datetime.now(), datetime.now() + timedelta(hours=1)),
        ),
        (
            "afk for 3h",
            (datetime.now(), datetime.now() + timedelta(hours=3)),
        ),
        (
            "afk for 3hr",
            (datetime.now(), datetime.now() + timedelta(hours=3)),
        ),
        (
            "afk for 3 hours",
            (datetime.now(), datetime.now() + timedelta(hours=3)),
        ),
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
        (
            "afk today",
            (datetime.now(), datetime.combine(datetime.now(), time.max)),
        ),
        (
            "afk tomorrow",
            (
                datetime.combine(datetime.now() + timedelta(days=1), time.min),
                datetime.combine(datetime.now() + timedelta(days=1), time.max),
            ),
        ),
        (
            "afk for 2 days",
            (
                datetime.combine(datetime.now() + timedelta(days=2), time.min),
                datetime.combine(datetime.now() + timedelta(days=2), time.max),
            ),
        ),
        (
            "afk for 10 days",
            (
                datetime.combine(datetime.now() + timedelta(days=10), time.min),
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
                datetime.combine(datetime.now() + relativedelta(months=1), time.max),
            ),
        ),
        (
            "afk for 6 months",
            (
                datetime.now(),
                datetime.combine(datetime.now() + relativedelta(months=6), time.max),
            ),
        ),
        (
            "afk for 12 months",
            (
                datetime.now(),
                datetime.combine(datetime.now() + relativedelta(months=12), time.max),
            ),
        ),
        (
            "afk for -1 month",
            (
                datetime.now(),
                datetime.combine(datetime.now() + relativedelta(months=-1), time.max),
            ),
        ),
        (
            "afk for -6 months",
            (
                datetime.now(),
                datetime.combine(datetime.now() + relativedelta(months=-6), time.max),
            ),
        ),
        (
            "afk for -12 months",
            (
                datetime.now(),
                datetime.combine(datetime.now() + relativedelta(months=-12), time.max),
            ),
        ),
        (
            "afk for 1 year",
            (
                datetime.now(),
                datetime.combine(datetime.now() + relativedelta(years=1), time.max),
            ),
        ),
        (
            "afk for 2 years",
            (
                datetime.now(),
                datetime.combine(datetime.now() + relativedelta(years=2), time.max),
            ),
        ),
        (
            "afk for -1 year",
            (
                datetime.now(),
                datetime.combine(datetime.now() + relativedelta(years=-1), time.max),
            ),
        ),
        (
            "afk for -2 years",
            (
                datetime.now(),
                datetime.combine(datetime.now() + relativedelta(years=-2), time.max),
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
        # INFO: calculate start_time, end_time is EOD
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
        # INFO: calculate both start_time and end_time
        (
            "afk on monday",
            (
                datetime.combine(datetime.now(), time.min)
                + timedelta(days=7 - datetime.now().weekday()),
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
def test_extract_datetime__with_local_tz(
    afk_parser: AFKParser,
    phrase: str,
    expected_datetimes: tuple[datetime, datetime],
    datetime_comparison_flex: timedelta,
) -> None:
    utc_offset_timedelta = datetime.now().astimezone().utcoffset()
    if utc_offset_timedelta is None:
        raise ValueError(f"{utc_offset_timedelta=}")

    utc_offset_seconds = utc_offset_timedelta.total_seconds()
    custom_timezone = timezone(timedelta(seconds=utc_offset_seconds))

    result = afk_parser.parse_dates(phrase=phrase, tz_offset=utc_offset_seconds)
    assert result is not None, f"Couldn't parse phrase: {phrase}"
    start_datetime, end_datetime = result
    expected_start_datetime, expected_end_datetime = (
        dt.replace(tzinfo=custom_timezone) for dt in expected_datetimes
    )
    assert abs(expected_start_datetime - start_datetime) <= datetime_comparison_flex
    assert abs(expected_end_datetime - end_datetime) <= datetime_comparison_flex
