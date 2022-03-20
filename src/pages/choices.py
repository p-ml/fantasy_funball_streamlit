import json
from collections import namedtuple
from json import JSONDecodeError
from typing import List

import requests
import streamlit as st
from pandas import DataFrame

from src.utilities import (
    determine_gameweek_no,
    divider,
    get_team_names,
    has_current_gameweek_deadline_passed,
)

FANTASY_FUNBALL_URL = st.secrets["FANTASY_FUNBALL_URL"]
ChoicesData = namedtuple(
    "ChoicesData",
    [
        "gameweek_no",
        "team_choice",
        "player_choice",
        "player_point_awarded",
        "team_point_awarded",
    ],
)
ColourMap = namedtuple(
    "ColourMap",
    [
        "team_points",
        "player_points",
    ],
)
SubmitChoiceData = namedtuple(
    "SubmitChoiceData",
    [
        "pin",
        "gameweek_no",
        "team_choice",
        "player_choice",
        "submit",
    ],
)


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


def _display_choices_form() -> str:
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
                value="Patrick",
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


def _determine_gameweek_no_limit() -> int:
    """
    Determines the gameweek number limit, returns the number of the next
    gameweek if the current gameweek deadline has passed.
    """
    gameweek_no_limit = determine_gameweek_no()
    current_gameweek_deadline_passed = has_current_gameweek_deadline_passed(
        gameweek_no=gameweek_no_limit,
    )
    if current_gameweek_deadline_passed:
        gameweek_no_limit += 1

    return gameweek_no_limit


def _retrieve_choices_data(funballer_name: str, gameweek_no_limit: int) -> ChoicesData:
    """
    Retrieve choices data from the backend. Only displays all future choices
    if the requested funballer matches that stored in the streamlit session.
    """
    choices = requests.get(f"{FANTASY_FUNBALL_URL}funballer/choices/{funballer_name}")

    if funballer_name == st.session_state.get("funballer_name"):
        view_all_choices = True
    else:
        view_all_choices = False

    try:
        gameweek_json = json.loads(choices.text)
        if not view_all_choices:
            gameweek_data = [
                x
                for x in gameweek_json
                if x["gameweek_id__gameweek_no"] in range(1, gameweek_no_limit)
            ]
        else:
            gameweek_data = gameweek_json

        gameweek_no = [x["gameweek_id__gameweek_no"] for x in gameweek_data]
        team_choice = [x["team_choice__team_name"] for x in gameweek_data]
        player_choice = [
            f"{x['player_choice__first_name']} {x['player_choice__surname']}"
            for x in gameweek_data
        ]
        player_point_awarded = [x["player_point_awarded"] for x in gameweek_data]
        team_point_awarded = [x["team_point_awarded"] for x in gameweek_data]

        choices_data = ChoicesData(
            gameweek_no=gameweek_no,
            team_choice=team_choice,
            player_choice=player_choice,
            player_point_awarded=player_point_awarded,
            team_point_awarded=team_point_awarded,
        )

        return choices_data

    except (JSONDecodeError, TypeError):
        st.error("Please enter a valid funballer name")
        st.stop()


def _create_choices_colour_map(choices_data: ChoicesData) -> ColourMap:
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
        True if result["player_point_awarded"] else False
        for result in player_result_data
    ]

    colour_map = ColourMap(
        team_points=team_point_awarded_colour_mapping,
        player_points=player_point_awarded_colour_mapping,
    )

    return colour_map


def _style_choices_dataframe(
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


def _create_choices_dataframe(
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
    indexed_choices_dataframe = choices_dataframe.set_index(
        "Gameweek Number", drop=False
    )

    colour_map = _create_choices_colour_map(choices_data=choices_data)

    styled_choices_dataframe = _style_choices_dataframe(
        choices_dataframe=indexed_choices_dataframe,
        colour_map=colour_map,
    )

    return styled_choices_dataframe


def _display_choices_dataframe(choices_dataframe: DataFrame) -> None:
    """Display choices dataframe"""
    st.dataframe(choices_dataframe)
    divider()


def _retrieve_player_data() -> List:
    """Retrieve player data from the backend"""
    raw_player_data = requests.get(f"{FANTASY_FUNBALL_URL}players/")
    player_data = json.loads(raw_player_data.text)

    return player_data


def _create_submit_choices_form(default_gameweek_no: int) -> SubmitChoiceData:
    st.subheader("Submit Choices")

    player_data = _retrieve_player_data()
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
            player["id"]
            for player in player_data
            if player_choice_name == player["name"]
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


def _post_choice(submit_choices_data: SubmitChoiceData) -> None:
    """Send POST request to backend with submitted choice payload"""
    post_payload = {
        "gameweek_no": submit_choices_data.gameweek_no,
        "team_choice": submit_choices_data.team_choice,
        "player_choice": submit_choices_data.player_choice,
    }

    submit_choices_request = requests.post(
        url=f"{FANTASY_FUNBALL_URL}funballer/choices/submit/{submit_choices_data.pin}",
        data=post_payload,
    )

    if submit_choices_request.status_code == 201:
        st.markdown("Gameweek selection submitted! :white_check_mark:")
    elif submit_choices_request.status_code == 200:
        st.markdown("Gameweek selection updated! :ballot_box_with_check:️")
    elif submit_choices_request.status_code in {400, 404, 500}:
        error_message = json.loads(submit_choices_request.text)["detail"]
        st.error(f"{error_message}")

    divider()


def _display_funballers_remaining_picks(funballer_name: str) -> None:
    """Display the remaining available team picks for the requested funballer"""
    st.subheader(f"Remaining Team Picks for {funballer_name}")

    remaining_valid_teams_raw = requests.get(
        f"{FANTASY_FUNBALL_URL}funballer/choices/valid_teams/{funballer_name}"
    )
    remaining_valid_teams = json.loads(remaining_valid_teams_raw.text)

    team_names = [response["team_name"] for response in remaining_valid_teams]
    remaining_selections = [
        response["remaining_selections"] for response in remaining_valid_teams
    ]

    remaining_teams_dataframe = DataFrame(
        {
            "Team Name": team_names,
            "Remaining Selections": remaining_selections,
        },
    )
    styled_remaining_teams_dataframe = remaining_teams_dataframe.style.apply(
        remaining_teams_styler,
        axis=None,
    )
    st.dataframe(styled_remaining_teams_dataframe)


def choices_app():
    st.subheader("View Choices")

    funballer_name = _display_choices_form()

    gameweek_no_limit = _determine_gameweek_no_limit()

    choices_data = _retrieve_choices_data(
        funballer_name=funballer_name,
        gameweek_no_limit=gameweek_no_limit,
    )

    choices_dataframe = _create_choices_dataframe(
        funballer_name=funballer_name,
        choices_data=choices_data,
    )

    _display_choices_dataframe(choices_dataframe=choices_dataframe)

    submit_choice_data = _create_submit_choices_form(
        default_gameweek_no=gameweek_no_limit,
    )

    if submit_choice_data.submit:
        _post_choice(submit_choices_data=submit_choice_data)

    _display_funballers_remaining_picks(funballer_name=funballer_name)
