from unittest.mock import Mock, patch

import pytest
from requests import Response

from src.pages.gameweeks import (
    SortedGameweekData,
    _determine_default_gameweek_no,
    _format_gameweek_data,
    _format_kickoffs,
    _retrieve_gameweek_data,
)

GAMEWEEKS_PAGE_PATH = "src.pages.gameweeks"


@pytest.mark.parametrize(
    "deadline_passed, expected_output",
    [
        (True, 2),
        (False, 1),
    ],
)
@patch(f"{GAMEWEEKS_PAGE_PATH}.determine_gameweek_no")
@patch(f"{GAMEWEEKS_PAGE_PATH}.has_current_gameweek_deadline_passed")
def test__determine_default_gameweek_no(
    mock_has_deadline_passed,
    mock_gameweek_no,
    deadline_passed,
    expected_output,
):
    mock_gameweek_no.return_value = 1
    mock_has_deadline_passed.return_value = deadline_passed

    output = _determine_default_gameweek_no()

    assert output == expected_output


def test__format_kickoffs():
    dummy_kickoffs = ["2022-01-01 12:00:00", "2022-02-02 22:00:00"]
    output = _format_kickoffs(kickoffs=dummy_kickoffs)

    expected_output = ["12:00", "22:00"]

    assert output == expected_output


def test__format_gameweek_data():
    dummy_gameweek_data = [
        {
            "id": 2,
            "home_team__team_name": "Spurs",
            "away_team__team_name": "Brentford",
            "gameday__date": "2022-01-01",
            "kickoff": "2022-01-01 12:00:00",
        },
        {
            "id": 1,
            "home_team__team_name": "Liverpool",
            "away_team__team_name": "Norwich",
            "gameday__date": "2022-01-02",
            "kickoff": "2022-01-02 15:00:00",
        },
    ]

    output = _format_gameweek_data(gameweek_data=dummy_gameweek_data)

    expected_output = SortedGameweekData(
        home_teams=["Liverpool", "Spurs"],
        away_teams=["Norwich", "Brentford"],
        game_dates=["2022-01-02", "2022-01-01"],
        kickoffs=["15:00", "12:00"],
    )

    assert output == expected_output


@patch(f"{GAMEWEEKS_PAGE_PATH}.requests")
def test__retrieve_gameweek_data(mock_request):
    dummy_gameweek_data = (
        '[{"id":2,"home_team__team_name":"Spurs","away_team__team_name":"Brentford",'
        '"gameday__date":"2022-01-01","kickoff":"2022-01-01 12:00:00"},{"id":1,'
        '"home_team__team_name":"Liverpool","away_team__team_name":"Norwich",'
        '"gameday__date":"2022-01-02","kickoff":"2022-01-02 15:00:00"}]'
    )
    mock_response = Mock(object=Response)
    mock_response.text = dummy_gameweek_data

    mock_request.get.return_value = mock_response

    arbitrary_gameweek_no = 1
    output = _retrieve_gameweek_data(gameweek_no=arbitrary_gameweek_no)

    expected_output = SortedGameweekData(
        home_teams=["Liverpool", "Spurs"],
        away_teams=["Norwich", "Brentford"],
        game_dates=["2022-01-02", "2022-01-01"],
        kickoffs=["15:00", "12:00"],
    )

    assert output == expected_output
