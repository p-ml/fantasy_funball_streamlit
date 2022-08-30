import streamlit as st


@st.experimental_memo
def get_team_names() -> tuple:
    return (
        "Arsenal",
        "Aston Villa",
        "Bournemouth",
        "Brentford",
        "Brighton",
        "Chelsea",
        "Crystal Palace",
        "Everton",
        "Fulham",
        "Leicester",
        "Leeds",
        "Liverpool",
        "Man City",
        "Man Utd",
        "Newcastle",
        "Nottingham Forest",
        "Southampton",
        "Spurs",
        "West Ham",
        "Wolves",
    )
