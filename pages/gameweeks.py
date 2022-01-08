import json
import os
from datetime import datetime
from json import JSONDecodeError

import pandas as pd
import pytz
import requests
import streamlit as st

from utilities.helpers import (
    determine_gameweek_no,
    get_gameweek_deadline,
    has_current_gameweek_deadline_passed,
)


def gameweeks_app():
    st.subheader("Gameweeks")

    default_gameweek_no = determine_gameweek_no()
    gameweek_deadline_passed = has_current_gameweek_deadline_passed(
        gameweek_no=default_gameweek_no,
    )
    if gameweek_deadline_passed:
        default_gameweek_no += 1

    gameweek_no = st.number_input(
        "Gameweek Number:", min_value=1, value=default_gameweek_no, max_value=38
    )
    gameweek_deadline = get_gameweek_deadline(gameweek_no=gameweek_no)

    fantasy_funball_url = os.environ.get("FANTASY_FUNBALL_URL")
    gameweek_raw = requests.get(f"{fantasy_funball_url}gameweek/{gameweek_no}")

    try:
        gameweek_json = json.loads(gameweek_raw.text)

        # Sort into ascending order by date, can be done via "id"
        gameweek_sorted = sorted(gameweek_json, key=lambda x: x["id"])

        game_home_team = [x["home_team__team_name"] for x in gameweek_sorted]
        game_away_team = [x["away_team__team_name"] for x in gameweek_sorted]

        # Convert each kickoff time to BST
        bst = pytz.timezone("Europe/London")
        game_kickoff = [
            datetime.strftime(
                bst.fromutc(datetime.strptime(x["kickoff"], "%Y-%m-%d %H:%M:%S")),
                "%H:%M",
            )
            for x in gameweek_sorted
        ]
        game_date = [x["gameday__date"] for x in gameweek_sorted]

    except (JSONDecodeError, TypeError):
        st.error("Please enter a gameweek number, valid range: 1-38")
        st.stop()

    gameweeks_dataframe = pd.DataFrame(
        {
            "Home Team": game_home_team,
            "Away Team": game_away_team,
            "Kickoff": game_kickoff,
            "Date": game_date,
        }
    )

    st.write(f"Gameweek {gameweek_no}:")
    st.write(gameweeks_dataframe)

    st.markdown(f"**Gameweek {gameweek_no} Deadline:** {gameweek_deadline}")
