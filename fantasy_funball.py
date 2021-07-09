import streamlit as st

from pages import MultiPage, choices_app, gameweeks_app, standings_app

app = MultiPage()

# Title of the main page
st.title("Fantasy Funball :soccer:")

# Add all your applications (pages) here
app.add_page("Standings", standings_app)
app.add_page("Gameweeks", gameweeks_app)
app.add_page("Choices", choices_app)

# The main app
app.run()
