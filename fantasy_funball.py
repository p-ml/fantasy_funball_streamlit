import streamlit as st

from page_manager import MultiPage
from pages.standings import app as standings_app
from pages.gameweeks import app as gameweeks_app

app = MultiPage()

# Title of the main page
st.title("Fantasy Funball :soccer:")

# Add all your applications (pages) here
app.add_page("Standings", standings_app)
app.add_page("Gameweeks", gameweeks_app)

# The main app
app.run()
