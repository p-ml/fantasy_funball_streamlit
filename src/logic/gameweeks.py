from json import JSONDecodeError
from typing import Dict

import pandas as pd
import streamlit as st

from interface import FunballInterface
from utilities import get_gameweek_deadline
from utilities.gameweek import determine_default_gameweek_no


def display_gameweek_select_box(default_gameweek_no: int) -> int:
    """
    Display the gameweek select box, allowing the user to select the desired
    gameweek no.
    """
    gameweek_no = st.number_input(
        "Gameweek Number:", min_value=1, value=default_gameweek_no, max_value=38
    )

    return gameweek_no


def display_gameweek_data(
    gameweek_data: Dict,
    gameweek_no: int,
) -> None:
    """Create gameweek dataframe and display it"""
    gameweeks_dataframe = pd.DataFrame(
        {
            "Home Team": gameweek_data["home_teams"],
            "Away Team": gameweek_data["away_teams"],
            "Kickoff": gameweek_data["game_kickoffs"],
            "Date": gameweek_data["game_dates"],
        }
    )

    st.write(f"Gameweek {gameweek_no}:")
    st.write(gameweeks_dataframe)
