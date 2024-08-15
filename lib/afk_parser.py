from datetime import datetime, time

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
