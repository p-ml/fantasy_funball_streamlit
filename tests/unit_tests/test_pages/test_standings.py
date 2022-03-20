from unittest.mock import Mock, patch

import pandas as pd
from pandas._testing import assert_frame_equal
from requests import Response

from src.pages.standings import (
    _create_standings_dataframe,
    _format_funballer_data,
    _retrieve_funballer_data,
    _retrieve_gameweek_summary,
)

STANDINGS_PAGE_PATH = "src.pages.standings"


@patch(f"{STANDINGS_PAGE_PATH}.requests")
def test__retrieve_gameweek_summary(mock_request):
    mock_response = Mock(object=Response)
    mock_response.text = '{"text":"Test Gameweek Summary"}'
    mock_request.get.return_value = mock_response

    output = _retrieve_gameweek_summary()

    expected_output = {"text": "Test Gameweek Summary"}
    assert output == expected_output


def test__format_funballer_data():
    dummy_funballer_data = [
        {
            "first_name": "Patrick",
            "team_points": 10,
            "player_points": 10,
            "points": 20,
        },
        {
            "first_name": "Kev",
            "team_points": 5,
            "player_points": 5,
            "points": 10,
        },
    ]

    output = _format_funballer_data(funballer_data=dummy_funballer_data)

    expected_output = {
        "funballer_names": ["Patrick", "Kev"],
        "funballer_team_points": [10, 5],
        "funballer_player_points": [10, 5],
        "funballer_points": [20, 10],
    }

    assert output == expected_output


@patch(f"{STANDINGS_PAGE_PATH}.requests")
def test__retrieve_funballer_data(mock_request):
    mock_response = Mock(object=Response)
    mock_response.text = (
        '[{"id":32,"first_name":"Test","surname":"Funballer","player_points":10,'
        '"team_points":5,"points":15,"pin":"1234"}]'
    )
    mock_request.get.return_value = mock_response

    output = _retrieve_funballer_data()
    expected_output = {
        "funballer_names": ["Test"],
        "funballer_player_points": [10],
        "funballer_team_points": [5],
        "funballer_points": [15],
    }

    assert output == expected_output


def test__create_standings_dataframe():
    dummy_funballer_data = {
        "funballer_names": ["Test One", "Test Two"],
        "funballer_player_points": [1, 10],
        "funballer_team_points": [2, 20],
        "funballer_points": [3, 30],
    }

    output = _create_standings_dataframe(
        funballer_data=dummy_funballer_data,
    )

    expected_output = pd.DataFrame(
        {
            "Name": ["Test Two", "Test One"],
            "Team Points": [20, 2],
            "Player Points": [10, 1],
            "Total Points": [30, 3],
        }
    )
    expected_output.index = range(1, -1, -1)

    # Use pandas 'assert_frame_equal' for DataFrame comparison
    assert_frame_equal(left=output, right=expected_output)
