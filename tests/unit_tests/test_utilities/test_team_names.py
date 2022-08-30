from src.utilities import get_team_names


def test_get_team_names():
    output = get_team_names()
    expected_output = (
        "Arsenal",
        "Aston Villa",
        "Bournemouth",
        "Brentford",
        "Brighton",
        "Chelsea",
        "Crystal Palace",
        "Everton",
        "Fulham",
        "Leicester",
        "Leeds",
        "Liverpool",
        "Man City",
        "Man Utd",
        "Newcastle",
        "Nott'm Forest",
        "Southampton",
        "Spurs",
        "West Ham",
        "Wolves",
    )

    assert output == expected_output
