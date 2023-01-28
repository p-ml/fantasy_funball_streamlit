from logic.players import SortedPlayerData, sort_player_data


def test_sort_player_data():
    mock_player_data = {
        "player_names": ["test player one", "test player two"],
        "goals": [1, 2],
        "assists": [2, 0],
    }

    output = sort_player_data(player_data=mock_player_data)

    expected_output = SortedPlayerData(
        goals=[2, 1],
        assists=[0, 2],
        player_names=["test player two", "test player one"],
    )

    assert output == expected_output
