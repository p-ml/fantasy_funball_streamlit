import json
import os

import pandas as pd
import requests
import streamlit as st

from utilities.team_names import get_team_names


def players_app():
    st.subheader("Players")

    retrieve_players_form = st.form(key="retrieve_team_players")
    team_name = retrieve_players_form.selectbox(
        label="Team Name:", options=get_team_names()
    )
    retrieve_players_form.form_submit_button("Retrieve Players")

    fantasy_funball_url = os.environ.get("FANTASY_FUNBALL_URL")
    players = requests.get(f"{fantasy_funball_url}{team_name}/players/")
    players_text = json.loads(players.text)

    player_name = [f"{x['first_name']} {x['surname']}" for x in players_text]
    goals = [x["goals"] for x in players_text]
    assists = [x["assists"] for x in players_text]

    st.write(f"{team_name} Players:")
    st.write(
        pd.DataFrame(
            {
                "Player Name": player_name,
                "Goals": goals,
                "Assists": assists,
            }
        )
    )
