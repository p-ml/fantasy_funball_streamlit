import json
import os

import pandas as pd
import requests
import streamlit as st

FANTASY_FUNBALL_URL = os.environ.get("FANTASY_FUNBALL_URL")


def _update_standings():
    """Wrapper to make update_standings request callable"""
    requests.get(f"{FANTASY_FUNBALL_URL}update_database/"),


def standings_app():
    st.subheader("Weekly Summary")
    summary = requests.get(f"{FANTASY_FUNBALL_URL}gameweek/summary/")
    summary_text = json.loads(summary.text)
    st.markdown(summary_text["text"])

    st.title("")  # Used as divider

    st.subheader("Standings")
    funballers = requests.get(f"{FANTASY_FUNBALL_URL}funballer/")
    funballers_text = json.loads(funballers.text)

    funballer_names = [x["first_name"] for x in funballers_text]
    funballer_team_points = [x["team_points"] for x in funballers_text]
    funballer_player_points = [x["player_points"] for x in funballers_text]
    funballer_points = [x["points"] for x in funballers_text]

    st.write("Funball Standings:")
    standings_dataframe = pd.DataFrame(
        {
            "Name": funballer_names,
            "Team Points": funballer_team_points,
            "Player Points": funballer_player_points,
            "Total Points": funballer_points,
        }
    ).sort_values(by="Total Points", ascending=False)

    st.write(standings_dataframe)

    update_standings_button = st.button(
        label="Update Standings",
        on_click=_update_standings(),
    )

    if update_standings_button:
        st.markdown("Standings updated! :white_check_mark:")
