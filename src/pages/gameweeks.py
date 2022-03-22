from json import JSONDecodeError

import pandas as pd
import streamlit as st

from src.interface.fantasy_funball import FantasyFunballInterface, SortedGameweekData
from src.utilities import (
    determine_gameweek_no,
    get_gameweek_deadline,
    has_current_gameweek_deadline_passed,
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
        fantasy_funball_interface = FantasyFunballInterface()
        gameweek_data = fantasy_funball_interface.get_gameweek_data(
            gameweek_no=gameweek_no
        )

        _display_gameweek_data(
            gameweek_data=gameweek_data,
            gameweek_no=gameweek_no,
        )

    except (JSONDecodeError, TypeError):
        st.error("Please enter a gameweek number, valid range: 1-38")
        st.stop()

    st.markdown(f"**Gameweek {gameweek_no} Deadline:** {gameweek_deadline}")
