import logging
import re
from datetime import datetime, time, timedelta
from typing import Any

import parsedatetime


def extract_datetime(phrase: str) -> datetime | None:
    cal = parsedatetime.Calendar()
    time_struct, parse_status = cal.parse(phrase)
    correct_eod_error = any(
        text in phrase and "will" not in phrase for text in ("eod", "day", "week", "month", "year")
    )

    if parse_status != 0:  # Check if parsing was successful
        datetime_obj = datetime(*time_struct[:6])  # Convert to datetime object
        if correct_eod_error:
            datetime_obj = datetime.combine(datetime_obj, time.max)
        return datetime_obj
    return None


class AFKParser:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)

    def get_afk_start_and_end_time(self, phrase: str) -> tuple[datetime, datetime] | None:
        # has_two_parts = any(i in phrase for i in ('from', 'to'))
        # is_scheduled_afk = 'will' in phrase
        cleaned_phrase = (
            phrase.replace("today", "today eod").replace("tomorrow", "tomorrow eod")
            if "will" not in phrase
            else phrase
        )
        extracted_datetime = extract_datetime(cleaned_phrase)
        start_time = datetime.now()

        if extracted_datetime:
            return (start_time, extracted_datetime)
        return None

    def parse_dates(self, phrase: str) -> tuple[datetime, datetime] | None:
        cal = parsedatetime.Calendar()
        has_two_parts = any(text in phrase for text in ("after", "from")) and any(
            text in phrase for text in ("to", "till", "for")
        )
        end_datetime_type = (
            datetime if any(text in phrase for text in ("to", "till")) else timedelta if "for" in phrase else Any
        )

        time_struct, parse_status = cal.parse(datetimeString=phrase)
        if parse_status == 0:
            logging.info(f"Could not parse datetime from phrase: {phrase}")
            return None

        if has_two_parts:
            start_datetime = datetime(*time_struct[:6])
            start_phrase, end_phrase, *_ = re.split(pattern=r"(?:to|till|for)", string=phrase, maxsplit=1)
            print(f"{start_phrase=} {end_phrase=} ")
            print(f"{start_datetime=}")
            time_struct, parse_status = cal.parse(datetimeString=end_phrase)
            if parse_status in (1, 3):  # time_struct is a date or datetime
                end_datetime = datetime(*time_struct[:6])
            elif parse_status == 2:  # time_struct is a time
                delta = datetime(*time_struct[:6]) - datetime.now()
                end_datetime = start_datetime + delta
            else:
                logging.info(f"Could not parse datetime from phrase: {end_phrase}")
                return None
            print(f"{parse_status=} {time_struct=}")
            print(f"{end_datetime=}")
            # return (start_datetime, end_datetime)
        elif any(text in phrase for text in ("after", "from", "post")):
            start_datetime = datetime(*time_struct[:6])
            end_datetime = datetime.combine(start_datetime, time.max)
        else:
            start_datetime = datetime.now()
            end_datetime = self.correct_end_of_day_datetimes(phrase=phrase, dt=datetime(*time_struct[:6]))
        print(f"{(start_datetime, end_datetime)=}")
        return (start_datetime, end_datetime)

    def correct_end_of_day_datetimes(self, phrase: str, dt: datetime):
        should_correct_eod_error = "will" not in phrase and any(
            text in phrase for text in ("today", "tomorrow", "day", "week", "month", "year")
        )
        if should_correct_eod_error:
            dt = datetime.combine(dt, time.max)
        return dt


def main():
    result = AFKParser().parse_dates(phrase="afk on 5pm")


if __name__ == "__main__":
    main()
