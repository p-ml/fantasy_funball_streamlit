import json
import os
from collections import namedtuple
from datetime import datetime
from json import JSONDecodeError
from typing import List

import pandas as pd
import pytz
import requests
import streamlit as st

from src.utilities import (
    determine_gameweek_no,
    get_gameweek_deadline,
    has_current_gameweek_deadline_passed,
)

FANTASY_FUNBALL_URL = os.environ.get("FANTASY_FUNBALL_URL")
SortedGameweekData = namedtuple(
    "SortedGameweekData", ["home_teams", "away_teams", "game_dates", "kickoffs"]
)


def _determine_default_gameweek_no() -> int:
    """
    Determines default gameweek no. If deadline has passed for current gameweek,
    the next gameweek no is returned.
    """
    default_gameweek_no = determine_gameweek_no()

    gameweek_deadline_passed = has_current_gameweek_deadline_passed(
        gameweek_no=default_gameweek_no,
    )

    if gameweek_deadline_passed:
        default_gameweek_no += 1

    return default_gameweek_no


def _display_gameweek_select_box(default_gameweek_no: int) -> int:
    """
    Display the gameweek select box, allowing the user to select the desired
    gameweek no.
    """
    gameweek_no = st.number_input(
        "Gameweek Number:", min_value=1, value=default_gameweek_no, max_value=38
    )

    return gameweek_no


def _format_kickoffs(kickoffs: List) -> List:
    """Format game kickoffs into Y-M-D H:M:S"""
    bst = pytz.timezone("Europe/London")

    formatted_kickoffs = [
        datetime.strftime(
            bst.fromutc(datetime.strptime(kickoff, "%Y-%m-%d %H:%M:%S")),
            "%H:%M",
        )
        for kickoff in kickoffs
    ]

    return formatted_kickoffs


def _format_gameweek_data(gameweek_data: List) -> SortedGameweekData:
    """Format gameweek data by sorting by gameweek id"""
    # Sort into ascending order by date, can be done via "id"
    gameweek_sorted = sorted(gameweek_data, key=lambda x: x["id"])

    home_teams = [game["home_team__team_name"] for game in gameweek_sorted]
    away_teams = [game["away_team__team_name"] for game in gameweek_sorted]

    # TODO: potentially duplicated info between gameday__date and kickoff
    game_dates = [game["gameday__date"] for game in gameweek_sorted]
    game_kickoffs = [game["kickoff"] for game in gameweek_sorted]

    formatted_kickoffs = _format_kickoffs(kickoffs=game_kickoffs)

    sorted_gameweek_data = SortedGameweekData(
        home_teams=home_teams,
        away_teams=away_teams,
        game_dates=game_dates,
        kickoffs=formatted_kickoffs,
    )

    return sorted_gameweek_data


def _retrieve_gameweek_data(gameweek_no: int) -> SortedGameweekData:
    """Retrieve gameweek data from backend & format it"""
    gameweek_data_raw = requests.get(f"{FANTASY_FUNBALL_URL}gameweek/{gameweek_no}")

    gameweek_data = json.loads(gameweek_data_raw.text)

    formatted_gameweek_data = _format_gameweek_data(gameweek_data=gameweek_data)

    return formatted_gameweek_data


def _display_gameweek_data(
    gameweek_data: SortedGameweekData,
    gameweek_no: int,
) -> None:
    """Create gameweek dataframe and display it"""
    gameweeks_dataframe = pd.DataFrame(
        {
            "Home Team": gameweek_data.home_teams,
            "Away Team": gameweek_data.away_teams,
            "Kickoff": gameweek_data.kickoffs,
            "Date": gameweek_data.game_dates,
        }
    )

    st.write(f"Gameweek {gameweek_no}:")
    st.write(gameweeks_dataframe)


def gameweeks_app():
    st.subheader("Gameweeks")

    default_gameweek_no = _determine_default_gameweek_no()

    gameweek_no = _display_gameweek_select_box(default_gameweek_no=default_gameweek_no)

    gameweek_deadline = get_gameweek_deadline(gameweek_no=gameweek_no)

    try:
        gameweek_data = _retrieve_gameweek_data(gameweek_no=gameweek_no)

        _display_gameweek_data(
            gameweek_data=gameweek_data,
            gameweek_no=gameweek_no,
        )

    except (JSONDecodeError, TypeError):
        st.error("Please enter a gameweek number, valid range: 1-38")
        st.stop()

    st.markdown(f"**Gameweek {gameweek_no} Deadline:** {gameweek_deadline}")
