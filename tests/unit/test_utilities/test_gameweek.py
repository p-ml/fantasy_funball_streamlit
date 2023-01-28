import datetime
from unittest.mock import patch

import pytest
import pytz

from src.utilities import determine_gameweek_no
from src.utilities.gameweek import (
    _localise_datetime,
    determine_default_gameweek_no,
    get_gameweek_deadline,
    has_current_gameweek_deadline_passed,
)

GAMEWEEK_UTILITIES_PATH = "src.utilities.gameweek"


@pytest.mark.parametrize(
    "input_timezone, expected_timezone",
    [
        ("utc", pytz.timezone("utc")),
        ("bst", pytz.timezone("Europe/London")),
    ],
)
def test__localise_datetime(dummy_datetime, input_timezone, expected_timezone):
    output = _localise_datetime(
        datetime=dummy_datetime,
        timezone=input_timezone,
    )

    # Expected output has to be created this way, as using the tzinfo argument of
    # the standard datetime constructors does not work with pytz for many timezones
    # more info: http://pytz.sourceforge.net/#localized-times-and-date-arithmetic
    expected_output = expected_timezone.localize(dummy_datetime)

    assert output == expected_output


def test__localise_datetime_unsupported_locale(dummy_datetime):
    with pytest.raises(Exception) as exc:
        _localise_datetime(
            datetime=dummy_datetime,
            timezone="pst",
        )
    assert str(exc.value) == "Timezone not supported."


@pytest.mark.parametrize(
    "current_datetime, expected_output",
    [
        (
            # Before "season" has started
            datetime.datetime(
                year=2021, month=1, day=1, hour=0, minute=0, second=0, tzinfo=None
            ),
            0,
        ),
        (
            # After "season" has started
            datetime.datetime(
                year=2022, month=1, day=3, hour=0, minute=0, second=0, tzinfo=None
            ),
            1,
        ),
    ],
)
@patch(f"{GAMEWEEK_UTILITIES_PATH}.datetime")
def test_determine_gameweek_no(
    mock_datetime,
    current_datetime,
    expected_output,
    dummy_datetime,
):
    mock_gameweek_data = [
        {
            "gameweek_no": 1,
            "deadline": "2022-01-02T12:00:00Z",
        }
    ]

    # current datetime
    mock_datetime.now.return_value = current_datetime

    # stored datetime (retrieved from backend)
    mock_datetime.strptime.return_value = dummy_datetime

    output = determine_gameweek_no(all_gameweek_data=mock_gameweek_data)
    assert output == expected_output


def test_get_gameweek_deadline():
    mock_gameweek_data = [
        {
            "gameweek_no": 1,
            "deadline": "2022-01-01T00:00:00Z",
        }
    ]

    output = get_gameweek_deadline(gameweek_no=1, gameweek_data=mock_gameweek_data)
    expected_output = "Sat 1 January 2022 @ 00:00:00"

    assert output == expected_output


@pytest.mark.parametrize(
    "input_deadline, expected_output",
    [
        ("Sat 1 January 2000 @ 00:00:00", True),
        ("Sat 1 January 2040 @ 00:00:00", False),
    ],
)
@patch(f"{GAMEWEEK_UTILITIES_PATH}.get_gameweek_deadline")
def test_has_current_gameweek_deadline_passed(
    mock_gameweek_deadline,
    input_deadline,
    expected_output,
):
    mock_gameweek_deadline.return_value = input_deadline

    arbitrary_gameweek_no = 1
    output = has_current_gameweek_deadline_passed(
        gameweek_no=arbitrary_gameweek_no,
        gameweek_data=[],
    )

    assert output == expected_output


@pytest.mark.parametrize(
    "deadline_passed, expected_output",
    [
        (True, 2),
        (False, 1),
    ],
)
@patch(f"{GAMEWEEK_UTILITIES_PATH}.determine_gameweek_no")
@patch(f"{GAMEWEEK_UTILITIES_PATH}.has_current_gameweek_deadline_passed")
def test__determine_default_gameweek_no(
    mock_has_deadline_passed,
    mock_gameweek_no,
    deadline_passed,
    expected_output,
):
    mock_gameweek_no.return_value = 1
    mock_has_deadline_passed.return_value = deadline_passed

    mock_gameweek_data = [
        {
            "gameweek_no": 1,
            "deadline": "2022-01-01T00:00:00Z",
        }
    ]

    output = determine_default_gameweek_no(
        all_gameweek_data=mock_gameweek_data,
    )

    assert output == expected_output
