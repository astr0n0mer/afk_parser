import logging
import re
from datetime import UTC, datetime, time, timedelta

import parsedatetime


class AFKParser:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)

    def parse_dates(
        self, phrase: str, tz_offset: float = 0
    ) -> tuple[datetime, datetime] | None:
        users_local_now = datetime.now(tz=UTC) + timedelta(seconds=tz_offset)
        cal = parsedatetime.Calendar()
        has_two_parts = any(text in phrase for text in ("after", "from")) and any(
            text in phrase for text in ("to", "till", "for")
        )

        time_struct, parse_status = cal.parse(
            datetimeString=phrase, sourceTime=users_local_now
        )
        if parse_status == 0:
            logging.info(f"Could not parse datetime from phrase: {phrase}")
            return None

        if has_two_parts:
            start_datetime = datetime(*time_struct[:6])
            start_phrase, end_phrase, *_ = re.split(
                pattern=r"(?:to|till|for)", string=phrase, maxsplit=1
            )
            time_struct, parse_status = cal.parse(datetimeString=end_phrase)
            if parse_status in (1, 3):  # time_struct is a date or datetime
                end_datetime = datetime(*time_struct[:6])
            elif parse_status == 2:  # time_struct is a time
                delta_seconds = (
                    datetime(*time_struct[:6]).timestamp() - datetime.now().timestamp()
                )
                end_datetime = start_datetime + timedelta(seconds=delta_seconds)
            else:
                logging.info(f"Could not parse datetime from phrase: {end_phrase}")
                return None
        elif any(text in phrase for text in ("after", "from", "post")):
            start_datetime = datetime(*time_struct[:6])
            end_datetime = datetime.combine(start_datetime, time.max)
        elif " on " in phrase and " by " not in phrase:
            end_datetime = datetime.combine(datetime(*time_struct[:6]), time.max)
            start_datetime = datetime.combine(end_datetime, time.min)
        else:
            start_datetime = datetime.now(tz=UTC) + timedelta(seconds=tz_offset)
            end_datetime = self.correct_end_of_day_datetimes(
                phrase=phrase, dt=datetime(*time_struct[:6])
            )
        return (start_datetime, end_datetime)

    def correct_end_of_day_datetimes(self, phrase: str, dt: datetime):
        should_correct_eod_error = "will" not in phrase and any(
            text in phrase
            for text in ("today", "tomorrow", "day", "week", "month", "year")
        )
        if should_correct_eod_error:
            dt = datetime.combine(dt, time.max)
        return dt
