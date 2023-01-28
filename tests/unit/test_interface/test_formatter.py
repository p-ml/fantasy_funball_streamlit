from interface.formatter import FunballInterfaceFormatter


def test_format_kickoffs():
    formatter = FunballInterfaceFormatter()
    dummy_kickoffs = ["2022-01-01 12:00:00", "2022-02-02 22:00:00"]
    output = formatter._format_kickoffs(kickoffs=dummy_kickoffs)

    expected_output = ["12:00", "22:00"]

    assert output == expected_output


def test_format_gameweek_data():
    formatter = FunballInterfaceFormatter()

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

    output = formatter.format_gameweek_data(gameweek_data=dummy_gameweek_data)

    expected_output = {
        "home_teams": ["Liverpool", "Spurs"],
        "away_teams": ["Norwich", "Brentford"],
        "game_dates": ["2022-01-02", "2022-01-01"],
        "game_kickoffs": ["15:00", "12:00"],
    }

    assert output == expected_output


def test_format_funballer_data():
    formatter = FunballInterfaceFormatter()

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

    output = formatter.format_funballer_data(funballer_data=dummy_funballer_data)

    expected_output = {
        "funballer_names": ["Patrick", "Kev"],
        "funballer_team_points": [10, 5],
        "funballer_player_points": [10, 5],
        "funballer_points": [20, 10],
    }

    assert output == expected_output
