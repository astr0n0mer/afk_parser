from datetime import datetime, time, timedelta, timezone
import logging
import re

import parsedatetime


class AFKParser:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)

    def parse_dates(
        self, phrase: str, tz_offset: float = 0
    ) -> tuple[datetime, datetime] | None:
        custom_timezone = timezone(timedelta(seconds=tz_offset))
        users_local_now = datetime.now(tz=custom_timezone)
        users_local_time_zone = users_local_now.tzinfo

        cal = parsedatetime.Calendar()
        has_two_parts = any(text in phrase for text in ("after", "from")) and any(
            text in phrase for text in ("to", "till", "for")
        )

        time_struct, parse_status = cal.parseDT(
            datetimeString=phrase,
            sourceTime=users_local_now,
            tzinfo=users_local_time_zone,
        )
        start_datetime = time_struct
        if parse_status == 0:
            logging.info(f"Could not parse datetime from phrase: {phrase}")
            return None

        if has_two_parts:
            start_phrase, end_phrase, *_ = re.split(
                pattern=r"(?:to|till|for)", string=phrase, maxsplit=1
            )
            time_struct, parse_status = cal.parseDT(
                datetimeString=end_phrase,
                sourceTime=users_local_now,
                tzinfo=users_local_time_zone,
            )
            # Create a datetime with the specified offset
            if parse_status in (1, 3):  # time_struct is a date or datetime
                end_datetime = time_struct
            elif parse_status == 2:  # time_struct is a time
                start_datetime, parse_status = cal.parseDT(
                    datetimeString=start_phrase,
                    sourceTime=users_local_now,
                    tzinfo=users_local_time_zone,
                )
                end_datetime = start_datetime + (time_struct - users_local_now)
            else:
                logging.info(f"Could not parse datetime from phrase: {end_phrase}")
                return None
        elif any(text in phrase for text in ("after", "from", "post")):
            start_datetime = time_struct
            end_datetime = datetime.combine(start_datetime, time.max)
        elif " on " in phrase and " by " not in phrase:
            end_datetime = datetime.combine(time_struct, time.max)
            start_datetime = datetime.combine(end_datetime, time.min)
        else:
            start_datetime = datetime.now(tz=users_local_time_zone)
            end_datetime = self.correct_end_of_day_datetimes(
                phrase=phrase, dt=time_struct
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
