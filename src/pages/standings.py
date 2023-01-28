import streamlit as st

from logic.standings import (
    _display_gameweek_info,
    _display_gameweek_summary,
    _display_standings,
    _display_update_standings_button,
)

st.set_page_config(
    page_title="Standings",
    page_icon=":bar_chart:",
    initial_sidebar_state="expanded",
)


def standings_app() -> None:
    """
    Standings app, also current homepage.
    Displays info on current gameweek and standings.

    """
    _display_gameweek_info()

    _display_gameweek_summary()

    _display_standings()

    _display_update_standings_button()


if __name__ == "__main__":
    standings_app()
