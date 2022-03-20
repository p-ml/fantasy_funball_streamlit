import json
from typing import Dict

import pandas as pd
import requests
import streamlit as st

from src.utilities import (
    determine_gameweek_no,
    divider,
    get_gameweek_deadline,
    has_current_gameweek_deadline_passed,
)

FANTASY_FUNBALL_URL = st.secrets["FANTASY_FUNBALL_URL"]


def _retrieve_gameweek_summary() -> Dict:
    """Retrieves gameweek summary from backend"""
    gameweek_summary = requests.get(f"{FANTASY_FUNBALL_URL}gameweek/summary/")
    gameweek_summary_text = json.loads(gameweek_summary.text)

    return gameweek_summary_text


def _display_gameweek_summary() -> None:
    """Displays gameweek summary section"""
    st.subheader("Weekly Summary")

    gameweek_summary = _retrieve_gameweek_summary()
    st.markdown(gameweek_summary["text"])

    divider()


def _format_funballer_data(funballer_data: Dict) -> Dict:
    """Parses and formats the raw funballer data"""
    funballer_names = [x["first_name"] for x in funballer_data]
    funballer_team_points = [x["team_points"] for x in funballer_data]
    funballer_player_points = [x["player_points"] for x in funballer_data]
    funballer_points = [x["points"] for x in funballer_data]

    funballer_data = {
        "funballer_names": funballer_names,
        "funballer_team_points": funballer_team_points,
        "funballer_player_points": funballer_player_points,
        "funballer_points": funballer_points,
    }

    return funballer_data


def _retrieve_funballer_data() -> Dict:
    """Retrieve funballer data from backend"""
    funballers = requests.get(f"{FANTASY_FUNBALL_URL}funballer/")
    funballers_text = json.loads(funballers.text)

    funballer_data = _format_funballer_data(funballer_data=funballers_text)

    return funballer_data


def _create_standings_dataframe(funballer_data: Dict) -> pd.DataFrame:
    """Creates standings dataframe"""
    standings_dataframe = pd.DataFrame(
        {
            "Name": funballer_data["funballer_names"],
            "Team Points": funballer_data["funballer_team_points"],
            "Player Points": funballer_data["funballer_player_points"],
            "Total Points": funballer_data["funballer_points"],
        }
    ).sort_values(by="Total Points", ascending=False)

    return standings_dataframe


def _display_gameweek_info() -> None:
    """
    Determine gameweek no - if deadline has passed, show info
    for next gameweek
    """
    gameweek_no = determine_gameweek_no()
    gameweek_deadline_passed = has_current_gameweek_deadline_passed(
        gameweek_no=gameweek_no
    )
    if gameweek_deadline_passed:
        gameweek_no += 1

    gameweek_deadline = get_gameweek_deadline(gameweek_no=gameweek_no)

    st.markdown(
        f"**Current Gameweek:** {gameweek_no}  \n"
        f"**Gameweek {gameweek_no} Deadline:** {gameweek_deadline}"
    )
    divider()


def _display_standings() -> None:
    """Displays current standings"""
    st.subheader("Standings")

    funballer_data = _retrieve_funballer_data()
    standings_dataframe = _create_standings_dataframe(funballer_data=funballer_data)

    st.write(standings_dataframe)
    divider()


def _update_standings() -> None:
    """Wrapper to make update_standings request callable"""
    requests.get(f"{FANTASY_FUNBALL_URL}update_database/"),


def _display_update_standings_button() -> None:
    update_standings_button = st.button(
        label="Update Standings",
        on_click=_update_standings(),
    )

    if update_standings_button:
        st.markdown("Standings updated! :white_check_mark:")


def standings_app() -> None:
    """
    Standings app, also current homepage.
    Displays info on current gameweek and standings.

    """
    _display_gameweek_info()

    _display_gameweek_summary()

    _display_standings()

    _display_update_standings_button()
