from src.pages.players import SortedPlayerData, _sort_player_data

PLAYER_PAGE_PATH = "src.pages.players"


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
