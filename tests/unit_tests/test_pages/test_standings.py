import pandas as pd
from pandas._testing import assert_frame_equal

from pages.Standings import _create_standings_dataframe

STANDINGS_PAGE_PATH = "src.pages.standings"


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
