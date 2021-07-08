import json
import os

import pandas as pd
import requests
import streamlit as st


def app():
    st.title("Gameweeks")
    gameweek_no = st.text_input("Gameweek Number:", 1)

    fantasy_funball_url = os.environ.get("FANTASY_FUNBALL_URL")
    gameweek = requests.get(f"{fantasy_funball_url}gameweek/{gameweek_no}")
    gameweek_json = json.loads(gameweek.text)

    game_id = [x["id"] for x in gameweek_json]
    game_home_team = [x["home_team"] for x in gameweek_json]
    game_away_team = [x["away_team"] for x in gameweek_json]
    game_kickoff = [x["kickoff"] for x in gameweek_json]

    st.write(f"Gameweek {gameweek_no}:")
    st.write(
        pd.DataFrame(
            {
                "Game ID": game_id,
                "Home Team": game_home_team,
                "Away Team": game_away_team,
                "Kickoff": game_kickoff,
            }
        )
    )
