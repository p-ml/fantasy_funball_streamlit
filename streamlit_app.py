import streamlit as st

from page_manager import MultiPage
from pages.demo_page import app as demo_app

app = MultiPage()

# Title of the main page
st.title("Fantasy Funball :soccer:")

# Add all your applications (pages) here
app.add_page("Demo", demo_app)

# The main app
app.run()
