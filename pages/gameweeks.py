import json
import os
from datetime import datetime
from json import JSONDecodeError

import pandas as pd
import pytz
import requests
import streamlit as st

from utilities.helpers import determine_gameweek_no, get_gameweek_deadline


def gameweeks_app():
    st.subheader("Gameweeks")

    default_gameweek_no = determine_gameweek_no()
    gameweek_no = st.number_input("Gameweek Number:", default_gameweek_no)
    gameweek_deadline = get_gameweek_deadline(gameweek_no=gameweek_no)

    fantasy_funball_url = os.environ.get("FANTASY_FUNBALL_URL")
    gameweek = requests.get(f"{fantasy_funball_url}gameweek/{gameweek_no}")

    try:
        gameweek_json = json.loads(gameweek.text)

        game_home_team = [x["home_team__team_name"] for x in gameweek_json]
        game_away_team = [x["away_team__team_name"] for x in gameweek_json]

        # Convert each kickoff time to BST
        bst = pytz.timezone("Europe/London")
        game_kickoff = [
            datetime.strftime(
                bst.fromutc(datetime.strptime(x["kickoff"], "%Y-%m-%d %H:%M:%S")),
                "%H:%M",
            )
            for x in gameweek_json
        ]
        game_date = [x["gameday__date"] for x in gameweek_json]

    except (JSONDecodeError, TypeError):
        st.error("Please enter a gameweek number, valid range: 1-38")
        st.stop()

    st.write(f"Gameweek {gameweek_no}:")
    st.write(
        pd.DataFrame(
            {
                "Home Team": game_home_team,
                "Away Team": game_away_team,
                "Kickoff": game_kickoff,
                "Date": game_date,
            }
        )
    )

    st.markdown(f"**Gameweek {gameweek_no} Deadline:** {gameweek_deadline}")
