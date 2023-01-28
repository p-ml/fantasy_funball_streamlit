import json
import os
from json import JSONDecodeError
from typing import Dict, List

import requests
import streamlit as st

from interface.formatter import FunballInterfaceFormatter
from utilities import ChoicesData, SubmitChoiceData, ValidTeamSelections, divider


class FunballInterface:
    def __init__(self):
        self.funball_url = os.environ.get("FANTASY_FUNBALL_URL")
        self.formatter = FunballInterfaceFormatter()

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
            choices_data = json.loads(choices.text)
            if not view_all_choices:
                choices_data = [
                    x
                    for x in choices_data
                    if x["gameweek_id__gameweek_no"] in range(1, gameweek_no_limit)
                ]

            formatted_choices_data = self.formatter.format_choices_data(
                choices_data=choices_data,
            )

            return formatted_choices_data

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

    def get_all_player_data(self) -> List:
        """Retrieve data on ALL players from the backend"""
        raw_player_data = requests.get(f"{self.funball_url}players/")
        player_data = json.loads(raw_player_data.text)

        return player_data

    def get_all_players_from_team(self, team_name: str) -> Dict:
        """Retrieve player data from the funball backend"""
        players = requests.get(f"{self.funball_url}{team_name}/players/")
        player_data = json.loads(players.text)

        formatted_player_data = self.formatter.format_all_players_from_team(
            player_data=player_data,
        )

        return formatted_player_data

    def get_funballer_valid_team_selections(
        self, funballer_name: str
    ) -> ValidTeamSelections:
        """Retrieve the remaining available team selections for the requested funballer"""
        remaining_valid_teams_raw = requests.get(
            f"{self.funball_url}funballer/choices/valid_teams/{funballer_name}"
        )
        remaining_valid_teams = json.loads(remaining_valid_teams_raw.text)

        valid_team_selections = self.formatter.format_funballer_valid_team_selections(
            remaining_valid_teams_data=remaining_valid_teams,
        )

        return valid_team_selections

    def get_single_gameweek_data(self, gameweek_no: int) -> Dict:
        """Retrieve gameweek data from backend & format it"""
        gameweek_data_raw = requests.get(f"{self.funball_url}gameweek/{gameweek_no}")

        gameweek_data = json.loads(gameweek_data_raw.text)

        formatted_gameweek_data = self.formatter.format_gameweek_data(
            gameweek_data=gameweek_data
        )

        return formatted_gameweek_data

    def get_all_gameweek_data(self) -> List:
        """Retrieve data on all gameweeks"""
        gameweek_info = requests.get(f"{self.funball_url}gameweek/all/")
        gameweek_data = json.loads(gameweek_info.text)

        return gameweek_data

    def get_funballer_data(self) -> Dict:
        """Retrieve all funballer data from backend"""
        funballers = requests.get(f"{self.funball_url}funballer/")
        funballers_text = json.loads(funballers.text)

        funballer_data = self.formatter.format_funballer_data(
            funballer_data=funballers_text
        )

        return funballer_data

    def get_gameweek_summary(self) -> Dict:
        """Retrieves gameweek summary from backend"""
        gameweek_summary = requests.get(f"{self.funball_url}gameweek/summary/")
        gameweek_summary_text = json.loads(gameweek_summary.text)

        return gameweek_summary_text

    def update_standings(self) -> None:
        """Wrapper to make update_standings request callable"""
        requests.get(f"{self.funball_url}update_database/")
