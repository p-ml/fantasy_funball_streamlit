import streamlit as st

from interface import FunballInterface
from logic.players import (
    _display_player_data,
    _display_retrieve_players_form,
    _sort_player_data,
)

st.set_page_config(
    page_title="Players",
    page_icon=":man_running:",
    initial_sidebar_state="expanded",
)


def players_app():
    st.subheader("Players")

    team_name = _display_retrieve_players_form()

    funball_interface = FunballInterface()
    player_data = funball_interface.get_all_players_from_team(team_name=team_name)

    sorted_player_data = _sort_player_data(player_data=player_data)

    _display_player_data(team_name=team_name, player_data=sorted_player_data)


if __name__ == "__main__":
    players_app()
