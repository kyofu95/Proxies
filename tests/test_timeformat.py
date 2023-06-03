import pytest
from unittest.mock import MagicMock

from proxies.views import td_format
from datetime import datetime, timedelta


def test_td_format_years():
    assert td_format(timedelta(days=365 * 3)) == "3 years"


def test_td_format_months():
    assert td_format(timedelta(days=30 * 6)) == "6 months"


def test_td_format_days():
    assert td_format(timedelta(days=10)) == "10 days"


def test_td_format_hours():
    assert td_format(timedelta(hours=12)) == "12 hours"


def test_td_format_minutes():
    assert td_format(timedelta(minutes=30)) == "30 minutes"


def test_td_format_seconds():
    assert td_format(timedelta(seconds=45)) == "45 seconds"


@pytest.mark.parametrize(
    "td_input", [timedelta(days=1), timedelta(hours=1), timedelta(minutes=1), timedelta(seconds=1)]
)
def test_td_format_positive_input(td_input):
    output = td_format(td_input)
    assert int(output.split(" ")[0]) == 1


@pytest.mark.parametrize(
    "td_input", [timedelta(days=0), timedelta(hours=0), timedelta(minutes=0), timedelta(seconds=0)]
)
def test_td_format_zero_input(td_input):
    assert td_format(td_input) == ""


@pytest.mark.parametrize(
    "td_input", [timedelta(days=-1), timedelta(hours=-1), timedelta(minutes=-1), timedelta(seconds=-1)]
)
def test_td_format_negative_input(td_input):
    assert td_format(td_input) == ""


def test_td_format_invalid_input():
    class InvalidInput:
        pass

    invalid_input = InvalidInput()
    with pytest.raises(AttributeError):
        td_format(invalid_input)
