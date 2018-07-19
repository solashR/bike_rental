import random
import datetime

import pytest

from bike_rental import billing


HOUR_PRICE = billing.BikeRate.ByHour.base_price
DAY_PRICE = billing.BikeRate.ByDay.base_price
WEEK_PRICE = billing.BikeRate.ByWeek.base_price


class TestBikeRate(object):

    @pytest.mark.parametrize(
        'minutes, expected_cost', [
            (30, HOUR_PRICE),
            (60, HOUR_PRICE),
            (90, HOUR_PRICE * 2),
            (120, HOUR_PRICE * 2)
        ])
    def test_by_hour(self, minutes, expected_cost):
        duration = datetime.timedelta(minutes=minutes)
        assert billing.BikeRate.ByHour.cost(duration) == expected_cost

    @pytest.mark.parametrize(
        'hours, expected_cost', [
            (22, DAY_PRICE),
            (26, DAY_PRICE * 2),
            (48, DAY_PRICE * 2)
        ])
    def test_by_day(self, hours, expected_cost):
        duration = datetime.timedelta(hours=hours)
        assert billing.BikeRate.ByDay.cost(duration) == expected_cost

    @pytest.mark.parametrize(
        'days, expected_cost', [
            (6, WEEK_PRICE),
            (7, WEEK_PRICE),
            (21, WEEK_PRICE * 3)
        ])
    def test_by_week(self, days, expected_cost):
        duration = datetime.timedelta(days=days)
        assert billing.BikeRate.ByWeek.cost(duration) == expected_cost

    @pytest.mark.parametrize('duration', [
        datetime.timedelta(),
        datetime.timedelta(seconds=-1)
    ])
    def test_illegal_duration(self, duration):
        rate = random.choice(list(billing.BikeRate))
        with pytest.raises(billing.InvalidDuration):
            rate.cost(duration)


def _bike(**kwargs) -> billing.BikeRental:
    duration = datetime.timedelta(**kwargs)
    return billing.BikeRental(duration)


class TestBikeRental(object):

    @pytest.mark.parametrize('duration', [
        datetime.timedelta(),
        datetime.timedelta(seconds=-1)
    ])
    def test_illegal_duration(self, duration):
        with pytest.raises(billing.InvalidDuration):
            billing.BikeRental(duration)

    @pytest.mark.parametrize('rental, expected_cost', [
        (_bike(hours=1), HOUR_PRICE),
        (_bike(hours=4), HOUR_PRICE * 4),
        (_bike(hours=5), DAY_PRICE),
        (_bike(days=1), DAY_PRICE),
        (_bike(days=3), DAY_PRICE * 3),
        (_bike(days=4), WEEK_PRICE),
        (_bike(weeks=1), WEEK_PRICE),
        (_bike(weeks=5), WEEK_PRICE * 5)
    ])
    def test_best_price(self, rental, expected_cost):
        assert rental.best_price() == expected_cost
