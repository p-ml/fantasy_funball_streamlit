from typing import Dict

import pandas as pd
import streamlit as st

from src.interface import FunballInterface
from src.utilities import (
    determine_gameweek_no,
    divider,
    get_gameweek_deadline,
    has_current_gameweek_deadline_passed,
)

FUNBALL_INTERFACE = FunballInterface()


def _display_gameweek_summary() -> None:
    """Displays gameweek summary section"""
    st.subheader("Weekly Summary")

    gameweek_summary = FUNBALL_INTERFACE.get_gameweek_summary()
    st.markdown(gameweek_summary["text"])

    divider()


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
    Determine gameweek no. - if deadline has passed, show info
    for next gameweek
    """
    gameweek_data = FUNBALL_INTERFACE.get_all_gameweek_data()
    gameweek_no = determine_gameweek_no(all_gameweek_data=gameweek_data)

    # Season not started yet
    if gameweek_no == 0:
        gameweek_no += 1

    gameweek_deadline_passed = has_current_gameweek_deadline_passed(
        gameweek_no=gameweek_no,
        gameweek_data=gameweek_data,
    )
    if gameweek_deadline_passed:
        gameweek_no += 1

    gameweek_deadline = get_gameweek_deadline(
        gameweek_no=gameweek_no,
        gameweek_data=gameweek_data,
    )

    if gameweek_no > 38:
        st.markdown(f"**Season finished.**")
    else:
        st.markdown(
            f"**Current Gameweek:** {gameweek_no}  \n"
            f"**Gameweek {gameweek_no} Deadline:** {gameweek_deadline}"
        )

    divider()


def _display_standings() -> None:
    """Displays current standings"""
    st.subheader("Standings")

    funballer_data = FUNBALL_INTERFACE.get_funballer_data()
    standings_dataframe = _create_standings_dataframe(funballer_data=funballer_data)

    st.write(standings_dataframe)
    divider()


def _display_update_standings_button() -> None:
    update_standings_button = st.button(
        label="Update Standings",
        on_click=FUNBALL_INTERFACE.update_standings(),
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
