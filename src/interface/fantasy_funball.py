import json
import os
from collections import namedtuple
from json import JSONDecodeError
from typing import List

import requests
import streamlit as st

from src.utilities import divider

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

ValidTeamSelections = namedtuple(
    "ValidTeamSelections",
    [
        "team_names",
        "remaining_selections",
    ],
)


class FantasyFunballInterface:
    def __init__(self):
        self.funball_url = os.environ.get("FANTASY_FUNBALL_URL")

    def get_choices_data(
        self, funballer_name: str, gameweek_no_limit: int
    ) -> ChoicesData:
        """
        Retrieve choices data from the backend. Only displays all future choices
        if the requested funballer matches that stored in the streamlit session.
        """
        choices = requests.get(f"{self.funball_url}funballer/choices/{funballer_name}")

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

    def post_choice(self, payload: SubmitChoiceData) -> None:
        """Send POST request to backend with submitted choice payload"""
        post_payload = {
            "gameweek_no": payload.gameweek_no,
            "team_choice": payload.team_choice,
            "player_choice": payload.player_choice,
        }

        submit_choices_request = requests.post(
            url=f"{self.funball_url}funballer/choices/submit/{payload.pin}",
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

    def get_player_data(self) -> List:
        """Retrieve player data from the backend"""
        # TODO: similar function in `src.pages.players`
        raw_player_data = requests.get(f"{self.funball_url}players/")
        player_data = json.loads(raw_player_data.text)

        return player_data

    def get_funballer_valid_team_picks(self, funballer_name: str) -> ValidTeamSelections:
        """Retrieve the remaining available team selections for the requested funballer"""
        remaining_valid_teams_raw = requests.get(
            f"{self.funball_url}funballer/choices/valid_teams/{funballer_name}"
        )
        remaining_valid_teams = json.loads(remaining_valid_teams_raw.text)

        team_names = [response["team_name"] for response in remaining_valid_teams]
        remaining_selections = [
            response["remaining_selections"] for response in remaining_valid_teams
        ]

        valid_team_selections = ValidTeamSelections(
            team_names=team_names,
            remaining_selections=remaining_selections,
        )

        return valid_team_selections
