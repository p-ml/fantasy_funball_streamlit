from src.utilities import get_team_names


def test_get_team_names():
    output = get_team_names()
    expected_output = (
        "Arsenal",
        "Aston Villa",
        "Brentford",
        "Brighton",
        "Burnley",
        "Chelsea",
        "Crystal Palace",
        "Everton",
        "Leicester",
        "Leeds",
        "Liverpool",
        "Man City",
        "Man Utd",
        "Newcastle",
        "Norwich",
        "Southampton",
        "Spurs",
        "Watford",
        "West Ham",
        "Wolves",
    )

    assert output == expected_output
