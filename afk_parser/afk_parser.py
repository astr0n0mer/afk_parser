from datetime import datetime, time, timedelta, timezone
import logging

from parsedatetime import Calendar, VERSION_CONTEXT_STYLE, pdtContext


class AFKParser:
    def __init__(self, logging_level: int = logging.INFO):
        logging.basicConfig(level=logging_level)

    def parse_dates(
        self, phrase: str, tz_offset: float = 0
    ) -> tuple[datetime, datetime] | None:
        custom_timezone = timezone(timedelta(seconds=tz_offset))
        start_datetime = end_datetime = datetime.now(tz=custom_timezone)
        cal = Calendar(version=VERSION_CONTEXT_STYLE)

        parsed_datetimes: tuple[tuple[datetime, pdtContext, int, int, str]] | None = (
            cal.nlp(inputString=phrase, sourceTime=start_datetime)
        )
        if not parsed_datetimes:
            logging.info(f"Could not parse datetime from phrase: {phrase}")
            return None

        if len(parsed_datetimes) == 1:
            parse_result = parsed_datetimes[0]
            parsed_datetime, flag, start_position, end_position, matched_text = (
                parse_result
            )
            if any(keyword in phrase for keyword in ("after", "from", "post")):
                start_datetime = parsed_datetime.replace(tzinfo=custom_timezone)
                end_datetime = datetime.combine(
                    date=start_datetime.date(), time=time.max
                ).replace(tzinfo=custom_timezone)
            elif any(
                flag.accuracy <= accuracy
                for accuracy in [
                    pdtContext.ACU_WEEK,
                    pdtContext.ACU_MONTH,
                    pdtContext.ACU_YEAR,
                ]
            ):
                end_datetime = datetime.combine(
                    date=parsed_datetime.date(), time=time.max
                ).replace(tzinfo=custom_timezone)
            elif flag.accuracy == pdtContext.ACU_DAY:
                start_datetime = max(
                    start_datetime,
                    datetime.combine(
                        date=parsed_datetime, time=time.min, tzinfo=custom_timezone
                    ),
                )
                end_datetime = datetime.combine(
                    date=start_datetime.date(), time=time.max
                ).replace(tzinfo=custom_timezone)
            elif any(
                flag.accuracy <= accuracy
                for accuracy in [
                    pdtContext.ACU_HOUR,
                    pdtContext.ACU_MIN,
                    pdtContext.ACU_SEC,
                ]
            ):
                end_datetime = parsed_datetime.replace(tzinfo=custom_timezone)
        else:
            start_datetime = parsed_datetimes[0][0].replace(tzinfo=custom_timezone)
            end_datetime = parsed_datetimes[1][0].replace(tzinfo=custom_timezone)

            if any(
                parsed_datetimes[1][1].accuracy <= accuracy
                for accuracy in [
                    pdtContext.ACU_HALFDAY,
                    pdtContext.ACU_HOUR,
                    pdtContext.ACU_MIN,
                    pdtContext.ACU_SEC,
                    pdtContext.ACU_NOW,
                ]
            ):
                delta = parsed_datetimes[1][0]
                end_datetime = start_datetime + timedelta(
                    hours=delta.hour, minutes=delta.minute, seconds=delta.second
                )

        return (start_datetime, end_datetime)
