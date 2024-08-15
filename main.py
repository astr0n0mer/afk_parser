from datetime import datetime
from typing import Tuple

from lib.afk_parser import extract_datetime


def main():
    phrases: list[Tuple[str, datetime]] = [
        # calculate start_time, end_time is EOD
        (
            "afk after 5pm for 1 hr",
            datetime.now().replace(hour=17, minute=0, second=0, microsecond=0),
        ),  # TODO: add test for the end date as well
    ]
    for phrase in phrases:
        phrase = (
            phrase[0].replace("today", "today eod").replace("tomorrow", "tomorrow eod")
            if "will" not in phrase[0]
            else phrase[0],
            phrase[1],
        )
        extracted_datetime = extract_datetime(phrase[0])

        if extracted_datetime:
            print(
                phrase[0],
                "\t",
                extracted_datetime,
                "\t",
                f"(expected: {phrase[1]})",
                "\t",
                extracted_datetime.strftime("%Y-%m-%d %H:%M:%S") == phrase[1].strftime("%Y-%m-%d %H:%M:%S"),
            )
            # assert extracted_datetime.strftime("%Y-%m-%d %H:%M:%S") == phrase[1].strftime(
            #     "%Y-%m-%d %H:%M:%S",
            # ), f'{extracted_datetime.strftime("%Y-%m-%d %H:%M:%S")} \t {phrase[1].strftime("%Y-%m-%d %H:%M:%S")}'
        else:
            print("Could not parse the input phrase.")


if __name__ == "__main__":
    main()
