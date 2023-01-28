from json import JSONDecodeError
from typing import Dict

import pandas as pd
import streamlit as st

from interface import FunballInterface
from utilities import get_gameweek_deadline
from utilities.gameweek import determine_default_gameweek_no

st.set_page_config(
    page_title="Gameweeks",
    page_icon=":calendar:",
    initial_sidebar_state="expanded",
)


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


def gameweeks_app():
    st.subheader("Gameweeks")

    funball_interface = FunballInterface()
    all_gameweek_data = funball_interface.get_all_gameweek_data()

    default_gameweek_no = determine_default_gameweek_no(
        all_gameweek_data=all_gameweek_data,
    )

    # Revert back to gameweek 38 if season is over (indicated by gameweek 39).
    if default_gameweek_no == 39:
        default_gameweek_no -= 1

    gameweek_no = _display_gameweek_select_box(default_gameweek_no=default_gameweek_no)

    try:
        gameweek_deadline = get_gameweek_deadline(
            gameweek_no=gameweek_no,
            gameweek_data=all_gameweek_data,
        )

        if gameweek_deadline == "Season finished.":
            st.markdown(f"**Season finished.**")

        else:
            single_gameweek_data = funball_interface.get_single_gameweek_data(
                gameweek_no=gameweek_no,
            )
            _display_gameweek_data(
                gameweek_data=single_gameweek_data,
                gameweek_no=gameweek_no,
            )

            st.markdown(f"**Gameweek {gameweek_no} Deadline:** {gameweek_deadline}")

    except (JSONDecodeError, TypeError):
        st.error("Please enter a gameweek number, valid range: 1-38")
        st.stop()


if __name__ == "__main__":
    gameweeks_app()
