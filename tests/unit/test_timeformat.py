from datetime import timedelta

import pytest

from proxies.utils.format import timedelta_format


def test_timedelta_format_years():
    assert timedelta_format(timedelta(days=365 * 3)) == "3 years"


def test_timedelta_format_months():
    assert timedelta_format(timedelta(days=30 * 6)) == "6 months"


def test_timedelta_format_days():
    assert timedelta_format(timedelta(days=10)) == "10 days"


def test_timedelta_format_hours():
    assert timedelta_format(timedelta(hours=12)) == "12 hours"


def test_timedelta_format_minutes():
    assert timedelta_format(timedelta(minutes=30)) == "30 minutes"


def test_timedelta_format_seconds():
    assert timedelta_format(timedelta(seconds=45)) == "45 seconds"


@pytest.mark.parametrize(
    "td_input", [timedelta(days=1), timedelta(hours=1), timedelta(minutes=1), timedelta(seconds=1)]
)
def test_timedelta_format_positive_input(td_input):
    output = timedelta_format(td_input)
    assert int(output.split(" ")[0]) == 1


@pytest.mark.parametrize(
    "td_input", [timedelta(days=0), timedelta(hours=0), timedelta(minutes=0), timedelta(seconds=0)]
)
def test_timedelta_format_zero_input(td_input):
    assert timedelta_format(td_input) == ""


@pytest.mark.parametrize(
    "td_input", [timedelta(days=-1), timedelta(hours=-1), timedelta(minutes=-1), timedelta(seconds=-1)]
)
def test_timedelta_format_negative_input(td_input):
    assert timedelta_format(td_input) == ""


def test_timedelta_format_invalid_input():
    class InvalidInput:
        pass

    invalid_input = InvalidInput()
    with pytest.raises(AttributeError):
        timedelta_format(invalid_input)
