from json import JSONDecodeError
from unittest.mock import Mock, patch

import pytest
from requests import Response

from src.pages.choices import (
    ChoicesData,
    ColourMap,
    _create_choices_colour_map,
    _determine_gameweek_no_limit,
    _retrieve_choices_data,
    _retrieve_player_data,
)

CHOICES_PAGE_PATH = "src.pages.choices"


@pytest.mark.parametrize(
    "deadline_passed, expected_output",
    [
        (True, 2),
        (False, 1),
    ],
)
@patch(f"{CHOICES_PAGE_PATH}.determine_gameweek_no")
@patch(f"{CHOICES_PAGE_PATH}.has_current_gameweek_deadline_passed")
def test__determine_gameweek_no_limit(
    mock_has_deadline_passed,
    mock_gameweek_no,
    deadline_passed,
    expected_output,
):
    mock_gameweek_no.return_value = 1
    mock_has_deadline_passed.return_value = deadline_passed

    output = _determine_gameweek_no_limit()

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
@patch(f"{CHOICES_PAGE_PATH}.st")
@patch(f"{CHOICES_PAGE_PATH}.requests")
def test__retrieve_choices_data(
    mock_request,
    mock_streamlit,
    session_funballer_name,
    expected_output,
):

    mock_response = Mock(object=Response)
    mock_response.text = '[{"id":2,"funballer_id":1,"player_choice__first_name":"Hugo","player_choice__surname":"Lloris","team_choice__team_name":"Liverpool","player_has_been_steved":false,"team_has_been_steved":false,"gameweek_id__gameweek_no":1,"team_point_awarded":true,"player_point_awarded":false},{"id":1,"funballer_id":1,"player_choice__first_name":"Harry","player_choice__surname":"Kane","team_choice__team_name":"Spurs","player_has_been_steved":true,"team_has_been_steved":false,"gameweek_id__gameweek_no":2,"team_point_awarded":true,"player_point_awarded":false}]'

    mock_request.get.return_value = mock_response
    mock_streamlit.session_state.get.return_value = session_funballer_name

    output = _retrieve_choices_data(
        funballer_name="test",
        gameweek_no_limit=2,
    )

    assert output == expected_output


def test__create_choices_colour_map():
    dummy_choices_data = ChoicesData(
        gameweek_no=[1],
        team_choice=["Spurs"],
        player_choice=["Hugo Lloris"],
        player_point_awarded=[False],
        team_point_awarded=[True],
    )

    expected_output = ColourMap(
        team_points=[True],
        player_points=[False],
    )

    output = _create_choices_colour_map(choices_data=dummy_choices_data)

    assert output == expected_output


@patch(f"{CHOICES_PAGE_PATH}.requests")
def test__retrieve_player_data(mock_request):
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

    output = _retrieve_player_data()

    assert output == expected_output
