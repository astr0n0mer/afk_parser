from datetime import datetime

from lib.relativedelta import relativedelta


class extended_datetime(datetime):
    def __add__(self, other):
        """Add a date to a relativedelta or timedelta."""
        if isinstance(other, relativedelta):
            month_diff_sign = -1 if (self.month + other.months) < 0 else 1
            month_diff_value = abs(self.month + other.months) % 12
            years_in_month_diff = abs(self.month + other.months) // 12 + (
                1 if month_diff_sign < 0 else 0
            )
            month = month_diff_value if month_diff_sign > 0 else 12 - month_diff_value
            year = (
                self.year
                + other.years
                + (years_in_month_diff if month_diff_sign > 0 else -years_in_month_diff)
            )
            return self.replace(month=month, year=year) + other.timedelta
        else:
            return super().__add__(other)
