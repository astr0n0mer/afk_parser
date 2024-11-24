from datetime import datetime, time, timedelta, timezone
import logging
import re

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

        # @return: tuple of tuples in the format (parsed_datetime as
        #  datetime.datetime, flags as int, start_pos as int,
        #  end_pos as int, matched_text as string) or None if there
        #  were no matches

        parsed_datetimes: tuple[tuple[datetime, pdtContext, int, int, str]] | None = (
            cal.nlp(inputString=phrase, sourceTime=start_datetime)
        )
        if not parsed_datetimes:
            logging.info(f"Could not parse datetime from phrase: {phrase}")
            return None

        print(f"{parsed_datetimes=}")

        if len(parsed_datetimes) == 1:
            parse_result = parsed_datetimes[0]
            parsed_datetime, flag, start_position, end_position, matched_text = (
                parse_result
            )
            print(f"{flag=}")
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
            # if flag.accuracy == pdtContext.ACU_DAY or any(s in phrase for s in ('after', 'from', 'post')):
            #     start_datetime = parse_result[0].replace(tzinfo=custom_timezone)
            #     end_datetime = datetime.combine(date=start_datetime, time=time.max).replace(tzinfo=custom_timezone)
            # else:
            #     end_datetime = parse_result[0].replace(tzinfo=custom_timezone)
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

        return (start_datetime, end_datetime)

        # 0 = not parsed at all
        # 1 = parsed as a C{date}
        # 2 = parsed as a C{time}
        # 3 = parsed as a C{datetime}

        # users_local_now = datetime.now(tz=custom_timezone)
        # users_local_time_zone = users_local_now.tzinfo

        # has_two_parts = any(text in phrase for text in ("after", "from")) and any(
        #     text in phrase for text in ("to", "till", "for")
        # )
        #
        # time_struct, parse_status = cal.parseDT(
        #     datetimeString=phrase,
        #     sourceTime=users_local_now,
        #     tzinfo=users_local_time_zone,
        # )
        # start_datetime = time_struct
        # if parse_status == 0:
        #     logging.info(f"Could not parse datetime from phrase: {phrase}")
        #     return None
        #
        # if has_two_parts:
        #     start_phrase, end_phrase, *_ = re.split(
        #         pattern=r"(?:to|till|for)", string=phrase, maxsplit=1
        #     )
        #     time_struct, parse_status = cal.parseDT(
        #         datetimeString=end_phrase,
        #         sourceTime=users_local_now,
        #         tzinfo=users_local_time_zone,
        #     )
        #     # Create a datetime with the specified offset
        #     if parse_status in (1, 3):  # time_struct is a date or datetime
        #         end_datetime = time_struct
        #     elif parse_status == 2:  # time_struct is a time
        #         start_datetime, parse_status = cal.parseDT(
        #             datetimeString=start_phrase,
        #             sourceTime=users_local_now,
        #             tzinfo=users_local_time_zone,
        #         )
        #         end_datetime = start_datetime + (time_struct - users_local_now)
        #     else:
        #         logging.info(f"Could not parse datetime from phrase: {end_phrase}")
        #         return None
        # elif any(text in phrase for text in ("after", "from", "post")):
        #     start_datetime = time_struct
        #     end_datetime = datetime.combine(start_datetime, time.max)
        # elif " on " in phrase and " by " not in phrase:
        #     end_datetime = datetime.combine(time_struct, time.max)
        #     start_datetime = datetime.combine(end_datetime, time.min)
        # else:
        #     start_datetime = datetime.now(tz=users_local_time_zone)
        #     end_datetime = self.correct_end_of_day_datetimes(
        #         phrase=phrase, dt=time_struct
        #     )
        # return (start_datetime, end_datetime)

    def correct_end_of_day_datetimes(self, phrase: str, dt: datetime):
        should_correct_eod_error = "will" not in phrase and any(
            text in phrase
            for text in ("today", "tomorrow", "day", "week", "month", "year")
        )
        if should_correct_eod_error:
            dt = datetime.combine(dt, time.max)
        return dt
