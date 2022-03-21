import streamlit as st

from pages import MultiPage, choices_app, gameweeks_app, players_app, standings_app

st.set_page_config(
    page_title="Fantasy Funball",
    page_icon=":soccer",
    initial_sidebar_state="expanded",
)

with st.spinner(text="Loading..."):  # Displays this whilst loading
    app = MultiPage()

    # Title of the main page
    st.title("Fantasy Funball :soccer:")

    app.add_page(title="Standings", func=standings_app)
    app.add_page(title="Gameweeks", func=gameweeks_app)
    app.add_page(title="Choices", func=choices_app)
    app.add_page(title="Players", func=players_app)

    app.run()
