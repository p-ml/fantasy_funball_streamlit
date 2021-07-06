import json
import os

import pandas as pd
import requests
import streamlit as st


def app():
    st.title("Demo Page")

    fantasy_funball_url = os.environ.get("FANTASY_FUNBALL_URL")
    funballers = requests.get(f"{fantasy_funball_url}funballer/")
    funballers_text = json.loads(funballers.text)

    funballer_names = [x["first_name"] for x in funballers_text]
    funballer_team_points = [x["team_points"] for x in funballers_text]
    funballer_player_points = [x["player_points"] for x in funballers_text]
    funballer_points = [x["points"] for x in funballers_text]

    st.write("Funball Standings:")
    st.write(
        pd.DataFrame(
            {
                "Name": funballer_names,
                "Team Points": funballer_team_points,
                "Player Points": funballer_player_points,
                "Total Points": funballer_points,
            }
        )
    )

    form = st.form(key="my_form")
    text = form.text_input(label="Enter some text")
    submit_button = form.form_submit_button(label="Submit")
