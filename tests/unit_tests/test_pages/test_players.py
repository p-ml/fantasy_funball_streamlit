from unittest.mock import Mock, patch

from requests import Response

from src.pages.players import SortedPlayerData, _retrieve_player_data, _sort_player_data

PLAYER_PAGE_PATH = "src.pages.players"


@patch(f"{PLAYER_PAGE_PATH}.requests")
def test__retrieve_player_data(mock_requests):
    mock_request_response = Mock(object=Response)
    mock_request_response.text = (
        '[{"id":1,"first_name":"test","surname":"player","goals":1,"assists":2}]'
    )

    mock_requests.get.return_value = mock_request_response

    output = _retrieve_player_data(team_name="Arsenal")

    expected_output = {
        "player_names": ["test player"],
        "goals": [1],
        "assists": [2],
    }

    assert output == expected_output


def test__sort_player_data():
    mock_player_data = {
        "player_names": ["test player one", "test player two"],
        "goals": [1, 2],
        "assists": [2, 0],
    }

    output = _sort_player_data(player_data=mock_player_data)

    expected_output = SortedPlayerData(
        goals=[2, 1],
        assists=[0, 2],
        player_names=["test player two", "test player one"],
    )

    assert output == expected_output
