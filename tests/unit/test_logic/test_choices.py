from logic.choices import ChoicesData, ColourMap, create_choices_colour_map


def test_create_choices_colour_map():
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

    output = create_choices_colour_map(choices_data=dummy_choices_data)

    assert output == expected_output
