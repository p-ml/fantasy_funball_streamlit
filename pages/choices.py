import json
import os
from json import JSONDecodeError
from typing import List

import requests
import streamlit as st
from pandas import DataFrame
from rest_framework import status

from utilities.helpers import (
    determine_gameweek_no,
    has_current_gameweek_deadline_passed,
)
from utilities.team_names import get_team_names


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


@st.experimental_memo
def get_funballer_name_from_pin(funballer_pin: str):
    """Gets funballer name from their pin"""
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
def remaining_teams_styler(s):
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


def choices_app():
    st.subheader("View Choices")

    with st.form(key="retrieve_choices"):
        cols = st.columns(2)
        funballer_name = (
            cols[0]
            .text_input(
                "Funballer Name:",
                "Patrick",
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

    gameweek_no_limit = determine_gameweek_no()
    current_gameweek_deadline_passed = has_current_gameweek_deadline_passed(
        gameweek_no=gameweek_no_limit,
    )
    if current_gameweek_deadline_passed:
        gameweek_no_limit += 1

    fantasy_funball_url = os.environ.get("FANTASY_FUNBALL_URL")
    choices = requests.get(f"{fantasy_funball_url}funballer/choices/{funballer_name}")

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

    except (JSONDecodeError, TypeError):
        st.error("Please enter a valid funballer name")
        st.stop()

    st.write(f"{funballer_name}'s Choices:")

    team_result = [
        {
            "team": team,
            "team_point_awarded": team_processed,
        }
        for team, team_processed in zip(team_choice, team_point_awarded)
    ]

    player_result = [
        {
            "player": player,
            "player_point_awarded": player_processed,
        }
        for player, player_processed in zip(player_choice, player_point_awarded)
    ]

    team_point_awarded_colour_mapping = [
        True if result["team_point_awarded"] else False for result in team_result
    ]
    player_point_awarded_colour_mapping = [
        True if result["player_point_awarded"] else False for result in player_result
    ]

    choices_dataframe = DataFrame(
        {
            "Funballer Name": funballer_name,
            "Gameweek Number": gameweek_no,
            "Team Choice": team_choice,
            "Player Choice": player_choice,
        }
    )
    choices_dataframe = choices_dataframe.set_index("Gameweek Number", drop=False)

    df_styler = DataframeStyler(
        dataframe=choices_dataframe,
        winning_teams_colourmap=team_point_awarded_colour_mapping,
        winning_players_colourmap=player_point_awarded_colour_mapping,
    )

    int_styled_dataframe = choices_dataframe.style.apply(
        df_styler.format_winning_teams, axis=None
    )
    final_styled_dataframe = int_styled_dataframe.apply(
        df_styler.format_winning_players, axis=None
    )
    st.dataframe(final_styled_dataframe)

    st.title("")  # Used as divider
    st.subheader("Submit Choices")

    raw_player_data = requests.get(f"{fantasy_funball_url}players/")
    player_data_json = json.loads(raw_player_data.text)
    player_names = [player["name"] for player in player_data_json]

    with st.form(key="submit_choices"):
        cols_top = st.columns(2)
        pin = cols_top[0].text_input("Funballer Pin:")
        gameweek_no = cols_top[1].number_input("Gameweek No:", gameweek_no_limit)
        cols_bottom = st.columns(2)
        team_choice = cols_bottom[0].selectbox(
            label="Team Choice:", options=get_team_names()
        )
        player_choice_name = cols_bottom[1].selectbox(
            label="Player Choice:", options=player_names
        )
        player_choice_id = next(
            player["id"]
            for player in player_data_json
            if player_choice_name == player["name"]
        )

        submit_choices = st.form_submit_button("Submit Choices")

    if submit_choices:
        post_payload = {
            "gameweek_no": gameweek_no,
            "team_choice": team_choice,
            "player_choice": player_choice_id,
        }

        submit_choices_request = requests.post(
            url=f"{fantasy_funball_url}funballer/choices/submit/{pin}",
            data=post_payload,
        )

        if submit_choices_request.status_code == status.HTTP_201_CREATED:
            st.markdown("Gameweek selection submitted! :white_check_mark:")
        elif submit_choices_request.status_code == status.HTTP_200_OK:
            st.markdown("Gameweek selection updated! :ballot_box_with_check:️")
        elif submit_choices_request.status_code in {
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_404_NOT_FOUND,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        }:
            error_message = json.loads(submit_choices_request.text)["detail"]
            st.error(f"{error_message}")

    # ------------------ Funballer remaining team picks --------------------
    st.title("")  # Used as divider
    st.subheader(f"Remaining Team Picks for {funballer_name}")
    remaining_valid_teams_raw = requests.get(
        f"{fantasy_funball_url}funballer/choices/valid_teams/{funballer_name}")
    remaining_valid_teams = json.loads(remaining_valid_teams_raw.text)

    team_names = [response["team_name"] for response in remaining_valid_teams]
    remaining_selections = [response["remaining_selections"] for response in remaining_valid_teams]
    remaining_teams_dataframe = DataFrame(
        {
            "Team Name": team_names,
            "Remaining Selections": remaining_selections,
        },
    )
    styled_remaining_teams_dataframe = remaining_teams_dataframe.style.apply(
        remaining_teams_styler, axis=None,
    )
    st.dataframe(styled_remaining_teams_dataframe)
