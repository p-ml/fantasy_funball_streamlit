import streamlit as st


@st.experimental_memo
def get_team_names() -> tuple:
    return (
        "Arsenal",
        "Aston Villa",
        "Brentford",
        "Brighton",
        "Burnley",
        "Chelsea",
        "Crystal Palace",
        "Everton",
        "Leicester",
        "Leeds",
        "Liverpool",
        "Man City",
        "Man Utd",
        "Newcastle",
        "Norwich",
        "Southampton",
        "Spurs",
        "Watford",
        "West Ham",
        "Wolves",
    )
