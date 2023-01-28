from typing import Dict

import pandas as pd
import streamlit as st

from utilities.models import SortedPlayerData
from utilities.team_names import get_team_names


def display_retrieve_players_form() -> str:
    """Display the retrieve players form, returns the name of the requested team name"""
    retrieve_players_form = st.form(key="retrieve_team_players")
    team_name = retrieve_players_form.selectbox(
        label="Team Name:", options=get_team_names()
    )
    retrieve_players_form.form_submit_button("Retrieve Players")

    return team_name


def sort_player_data(player_data: Dict) -> SortedPlayerData:
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


def display_player_data(team_name: str, player_data: SortedPlayerData) -> None:
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
