from unittest.mock import Mock, patch

import pytest
from requests import Response

from src.interface import FunballInterface
from src.utilities import ChoicesData

INTERFACE_PATH = "src.interface.fantasy_funball"

FUNBALL_INTERFACE = FunballInterface()


@patch(f"{INTERFACE_PATH}.requests")
def test_get_single_gameweek_data(mock_request):
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
    output = FUNBALL_INTERFACE.get_single_gameweek_data(gameweek_no=arbitrary_gameweek_no)

    expected_output = {
        "home_teams": ["Liverpool", "Spurs"],
        "away_teams": ["Norwich", "Brentford"],
        "game_dates": ["2022-01-02", "2022-01-01"],
        "game_kickoffs": ["15:00", "12:00"],
    }

    assert output == expected_output


@patch(f"{INTERFACE_PATH}.requests")
def test_get_all_player_data(mock_request):
    mock_request_response = Mock(object=Response)
    mock_request_response.text = (
        '[{"id":1,"first_name":"test","surname":"player","goals":1,"assists":2}]'
    )

    mock_request.get.return_value = mock_request_response

    expected_output = [
        {
            "id": 1,
            "first_name": "test",
            "surname": "player",
            "goals": 1,
            "assists": 2,
        }
    ]

    output = FUNBALL_INTERFACE.get_all_player_data()

    assert output == expected_output


@pytest.mark.parametrize(
    "session_funballer_name, expected_output",
    [
        (
            "test",
            ChoicesData(
                gameweek_no=[1, 2],
                team_choice=["Liverpool", "Spurs"],
                player_choice=["Hugo Lloris", "Harry Kane"],
                player_point_awarded=[False, False],
                team_point_awarded=[True, True],
            ),
        ),
        (
            "blah",
            ChoicesData(
                gameweek_no=[1],
                team_choice=["Liverpool"],
                player_choice=["Hugo Lloris"],
                player_point_awarded=[False],
                team_point_awarded=[True],
            ),
        ),
    ],
)
@patch(f"{INTERFACE_PATH}.st")
@patch(f"{INTERFACE_PATH}.requests")
def test_get_choices_data(
    mock_request,
    mock_streamlit,
    session_funballer_name,
    expected_output,
):

    mock_response = Mock(object=Response)
    mock_response.text = (
        '[{"id":2,"funballer_id":1,"player_choice__first_name":"Hugo",'
        '"player_choice__surname":"Lloris","team_choice__team_name":'
        '"Liverpool","player_has_been_steved":false,"team_has_been_steved":false,'
        '"gameweek_id__gameweek_no":1,"team_point_awarded":true,'
        '"player_point_awarded":false},{"id":1,"funballer_id":1,'
        '"player_choice__first_name":"Harry","player_choice__surname":"Kane",'
        '"team_choice__team_name":"Spurs","player_has_been_steved":true,'
        '"team_has_been_steved":false,"gameweek_id__gameweek_no":2,'
        '"team_point_awarded":true,"player_point_awarded":false}]'
    )

    mock_request.get.return_value = mock_response
    mock_streamlit.session_state.get.return_value = session_funballer_name

    output = FUNBALL_INTERFACE.get_choices_data(
        funballer_name="test",
        gameweek_no_limit=2,
    )

    assert output == expected_output


@patch(f"{INTERFACE_PATH}.requests")
def test_get_gameweek_summary(mock_request):
    mock_response = Mock(object=Response)
    mock_response.text = '{"text":"Test Gameweek Summary"}'
    mock_request.get.return_value = mock_response

    output = FUNBALL_INTERFACE.get_gameweek_summary()

    expected_output = {"text": "Test Gameweek Summary"}
    assert output == expected_output


@patch(f"{INTERFACE_PATH}.requests")
def test_get_funballer_data(mock_request):
    mock_response = Mock(object=Response)
    mock_response.text = (
        '[{"id":32,"first_name":"Test","surname":"Funballer","player_points":10,'
        '"team_points":5,"points":15,"pin":"1234"}]'
    )
    mock_request.get.return_value = mock_response

    output = FUNBALL_INTERFACE.get_funballer_data()
    expected_output = {
        "funballer_names": ["Test"],
        "funballer_player_points": [10],
        "funballer_team_points": [5],
        "funballer_points": [15],
    }

    assert output == expected_output
