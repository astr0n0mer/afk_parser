from datetime import timedelta


class relativedelta(timedelta):
    __slots__ = "_timedelta", "_years", "_months"

    def __new__(cls, months=0, years=0, timedelta=timedelta()):
        self = timedelta.__new__(cls)
        self._months = months
        self._years = years
        self._timedelta = timedelta
        return self

    def __add__(self, other):
        if isinstance(other, relativedelta):
            # for CPython compatibility, we cannot use
            # our __class__ here, but need a real relativedelta
            self._timedelta += other._timedelta
            month_diff = self._months - other._months
            self._months += month_diff if month_diff >= 0 else 12 - abs(month_diff)
            self._years += other._years - (0 if month_diff >= 0 else 1)
            return relativedelta(
                months=self._months, years=self._years, timedelta=self._timedelta
            )
        else:
            return relativedelta(
                months=self._months,
                years=self._years,
                timedelta=self._timedelta + other,
            )

    @property
    def months(self):
        """Months"""
        return self._months

    @property
    def years(self):
        """Years"""
        return self._years

    @property
    def timedelta(self):
        """Timedelta"""
        return self._timedelta
