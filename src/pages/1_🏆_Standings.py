import streamlit as st

from logic.standings import (
    display_gameweek_info,
    display_gameweek_summary,
    display_standings,
    display_update_standings_button,
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
    display_gameweek_info()

    display_gameweek_summary()

    display_standings()

    display_update_standings_button()


if __name__ == "__main__":
    standings_app()
