from typing import List

import streamlit as st
from pandas import DataFrame

from utilities import ChoicesData, ColourMap, SubmitChoiceData, divider, get_team_names


class DataframeStyler:
    def __init__(
        self,
        dataframe: DataFrame,
        winning_teams_colourmap: List[int],
        winning_players_colourmap: List[int],
    ):
        self.styled_dataframe = DataFrame(
            "", index=dataframe.index, columns=dataframe.columns
        )

        self.winning_teams_colourmap = winning_teams_colourmap
        self.winning_players_colourmap = winning_players_colourmap

        self.win_colour = "background-color: green"
        self.lose_colour = "background-color: red"

    def format_winning_teams(self, *_) -> DataFrame:
        team_choice_column_index = 2
        for index, value in enumerate(self.winning_teams_colourmap):
            if value:
                self.styled_dataframe.iloc[
                    index, team_choice_column_index
                ] = self.win_colour
            else:
                self.styled_dataframe.iloc[
                    index, team_choice_column_index
                ] = self.lose_colour

        return self.styled_dataframe

    def format_winning_players(self, *_) -> DataFrame:
        player_choice_column_index = 3
        for index, value in enumerate(self.winning_players_colourmap):
            if value:
                self.styled_dataframe.iloc[
                    index, player_choice_column_index
                ] = self.win_colour
            else:
                self.styled_dataframe.iloc[
                    index, player_choice_column_index
                ] = self.lose_colour

        return self.styled_dataframe


def get_funballer_name_from_pin(funballer_pin: str) -> None:
    """Gets funballer name from their pin, adds user to streamlit session state"""
    funballers = [
        {
            "first_name": "Patrick",
            "pin": "1050",
        },
        {
            "first_name": "Ben",
            "pin": "8251",
        },
        {
            "first_name": "Henry",
            "pin": "5064",
        },
        {
            "first_name": "Will",
            "pin": "8285",
        },
        {
            "first_name": "Theo",
            "pin": "9306",
        },
        {
            "first_name": "Gordon",
            "pin": "0625",
        },
        {
            "first_name": "Josh",
            "pin": "9839",
        },
        {
            "first_name": "Adam",
            "pin": "9308",
        },
        {
            "first_name": "Ilya",
            "pin": "0322",
        },
        {
            "first_name": "Steve",
            "pin": "2361",
        },
    ]

    funballer_name = next(
        funballer["first_name"]
        for funballer in funballers
        if funballer["pin"] == funballer_pin
    )

    st.session_state.funballer_name = funballer_name


@st.experimental_memo
def remaining_teams_styler(s) -> DataFrame:
    green = "background-color: green"
    orange = "background-color: orange"
    red = "background-color: red"

    dataframe = s.copy()

    green_mask = dataframe["Remaining Selections"] == 2
    orange_mask = dataframe["Remaining Selections"] == 1
    red_mask = dataframe["Remaining Selections"] == 0

    dataframe.loc[green_mask, :] = green
    dataframe.loc[orange_mask, :] = orange
    dataframe.loc[red_mask, :] = red

    return dataframe


def display_choices_form() -> str:
    """
    Display the choices form, allowing user to select who's choices they want to
    see
    """
    with st.form(key="retrieve_choices"):
        cols = st.columns(2)
        funballer_name = (
            cols[0]
            .text_input(
                label="Funballer Name:",
                value=st.session_state["autheticated_user"].title(),
            )
            .capitalize()
        )
        funballer_pin = cols[1].text_input("Funballer Pin:")

        retrieve_choices_bool = st.form_submit_button("Retrieve Funballer Choices")
        st.write("Your pin is required to view your future choices.")

    if retrieve_choices_bool:
        try:
            get_funballer_name_from_pin(funballer_pin=funballer_pin)
        except StopIteration:
            pass

    return funballer_name


def create_choices_colour_map(choices_data: ChoicesData) -> ColourMap:
    """
    Create dataframe colour map for points awarded for team and player choices.
    """
    team_result_data = [
        {
            "team": team_name,
            "team_point_awarded": team_point_awarded,
        }
        for team_name, team_point_awarded in zip(
            choices_data.team_choice, choices_data.team_point_awarded
        )
    ]

    player_result_data = [
        {
            "player": player_name,
            "player_point_awarded": player_point_awarded,
        }
        for player_name, player_point_awarded in zip(
            choices_data.player_choice, choices_data.player_point_awarded
        )
    ]

    team_point_awarded_colour_mapping = [
        True if result["team_point_awarded"] else False for result in team_result_data
    ]
    player_point_awarded_colour_mapping = [
        True if result["player_point_awarded"] else False for result in player_result_data
    ]

    colour_map = ColourMap(
        team_points=team_point_awarded_colour_mapping,
        player_points=player_point_awarded_colour_mapping,
    )

    return colour_map


def style_choices_dataframe(
    choices_dataframe: DataFrame,
    colour_map: ColourMap,
) -> DataFrame:
    df_styler = DataframeStyler(
        dataframe=choices_dataframe,
        winning_teams_colourmap=colour_map.team_points,
        winning_players_colourmap=colour_map.player_points,
    )

    int_styled_dataframe = choices_dataframe.style.apply(
        df_styler.format_winning_teams, axis=None
    )
    final_styled_dataframe = int_styled_dataframe.apply(
        df_styler.format_winning_players, axis=None
    )

    return final_styled_dataframe


def create_choices_dataframe(
    funballer_name: str,
    choices_data: ChoicesData,
) -> DataFrame:
    """Create the choices dataframe"""
    st.write(f"{funballer_name}'s Choices:")

    choices_dataframe = DataFrame(
        {
            "Funballer Name": funballer_name,
            "Gameweek Number": choices_data.gameweek_no,
            "Team Choice": choices_data.team_choice,
            "Player Choice": choices_data.player_choice,
        }
    )
    indexed_choices_dataframe = choices_dataframe.set_index("Gameweek Number", drop=False)

    colour_map = _create_choices_colour_map(choices_data=choices_data)

    styled_choices_dataframe = _style_choices_dataframe(
        choices_dataframe=indexed_choices_dataframe,
        colour_map=colour_map,
    )

    return styled_choices_dataframe


def display_choices_dataframe(choices_dataframe: DataFrame) -> None:
    """Display choices dataframe"""
    st.dataframe(choices_dataframe)
    divider()


def create_submit_choices_form(default_gameweek_no: int) -> SubmitChoiceData:
    st.subheader("Submit Choices")

    player_data = FUNBALL_INTERFACE.get_all_player_data()

    player_names = [player["name"] for player in player_data]

    with st.form(key="submit_choices"):
        cols_top = st.columns(2)
        pin = cols_top[0].text_input("Funballer Pin:")
        gameweek_no = cols_top[1].number_input("Gameweek No:", default_gameweek_no)

        cols_bottom = st.columns(2)
        team_choice = cols_bottom[0].selectbox(
            label="Team Choice:", options=get_team_names()
        )
        player_choice_name = cols_bottom[1].selectbox(
            label="Player Choice:", options=player_names
        )
        player_choice_id = next(
            player["id"] for player in player_data if player_choice_name == player["name"]
        )

        submit_choices = st.form_submit_button("Submit Choices")

        submit_choice_data = SubmitChoiceData(
            pin=pin,
            gameweek_no=gameweek_no,
            team_choice=team_choice,
            player_choice=player_choice_id,
            submit=submit_choices,
        )

        return submit_choice_data


def display_funballers_remaining_picks(funballer_name: str) -> None:
    """Display the remaining available team picks for the requested funballer"""
    st.subheader(f"Remaining Team Picks for {funballer_name}")

    valid_team_selections = FUNBALL_INTERFACE.get_funballer_valid_team_selections(
        funballer_name=funballer_name,
    )

    remaining_teams_dataframe = DataFrame(
        {
            "Team Name": valid_team_selections.team_names,
            "Remaining Selections": valid_team_selections.remaining_selections,
        },
    )
    styled_remaining_teams_dataframe = remaining_teams_dataframe.style.apply(
        remaining_teams_styler,
        axis=None,
    )
    st.dataframe(styled_remaining_teams_dataframe)
