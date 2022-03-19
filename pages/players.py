import json
from collections import namedtuple
from typing import Dict

import pandas as pd
import requests
import streamlit as st

from utilities.team_names import get_team_names

FANTASY_FUNBALL_URL = st.secrets["FANTASY_FUNBALL_URL"]
SortedPlayerData = namedtuple("SortedPlayerData", ["player_names", "goals", "assists"])


def _display_retrieve_players_form() -> str:
    """Display the retrieve players form, returns the name of the requested team name"""
    retrieve_players_form = st.form(key="retrieve_team_players")
    team_name = retrieve_players_form.selectbox(
        label="Team Name:", options=get_team_names()
    )
    retrieve_players_form.form_submit_button("Retrieve Players")

    return team_name


def _retrieve_player_data(team_name: str) -> Dict:
    """Retrieve player data from the funball backend"""
    players = requests.get(f"{FANTASY_FUNBALL_URL}{team_name}/players/")
    players_text = json.loads(players.text)

    player_names = [f"{x['first_name']} {x['surname']}" for x in players_text]
    goals = [x["goals"] for x in players_text]
    assists = [x["assists"] for x in players_text]

    player_data = {
        "player_names": player_names,
        "goals": goals,
        "assists": assists,
    }

    return player_data


def _sort_player_data(player_data: Dict) -> SortedPlayerData:
    """Sort player data by goals scored"""
    player_data = zip(
        player_data["goals"], player_data["assists"], player_data["player_names"]
    )
    player_data_sorted = sorted(player_data, reverse=True)

    goals, assists, player_names = map(list, zip(*player_data_sorted))

    sorted_player_data = SortedPlayerData(
        goals=goals,
        assists=assists,
        player_names=player_names,
    )

    return sorted_player_data


def _display_player_data(team_name: str, player_data: SortedPlayerData) -> None:
    """Constructs a pandas dataframe and displays it"""
    st.write(f"{team_name} Players:")
    st.write(
        pd.DataFrame(
            {
                "Player Name": player_data.player_names,
                "Goals": player_data.goals,
                "Assists": player_data.assists,
            }
        )
    )


def players_app():
    st.subheader("Players")

    team_name = _display_retrieve_players_form()

    player_data = _retrieve_player_data(team_name=team_name)

    sorted_player_data = _sort_player_data(player_data=player_data)

    _display_player_data(team_name=team_name, player_data=sorted_player_data)
