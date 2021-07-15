import json
import os
from json import JSONDecodeError

import pandas as pd
import requests
import streamlit as st
from rest_framework import status

from utilities.team_names import get_team_names


def choices_app():
    st.subheader("View Choices")

    retrieve_choices_form = st.form(key="retrieve_choices")
    funballer_name = retrieve_choices_form.text_input(
        "Funballer Name:", "Patrick"
    ).capitalize()
    retrieve_choices_form.form_submit_button("Retrieve Funballer Choices")

    fantasy_funball_url = os.environ.get("FANTASY_FUNBALL_URL")
    choices = requests.get(f"{fantasy_funball_url}funballer/choices/{funballer_name}")
    try:
        gameweek_json = json.loads(choices.text)

        gameweek_no = [x["gameweek_id__gameweek_no"] for x in gameweek_json]
        team_choice = [x["team_choice__team_name"] for x in gameweek_json]
        player_choice = [
            f"{x['player_choice__first_name']} {x['player_choice__surname']}"
            for x in gameweek_json
        ]

    except (JSONDecodeError, TypeError):
        st.error("Please enter a valid funballer name")
        st.stop()

    st.write(f"{funballer_name}'s Choices:")
    st.write(
        pd.DataFrame(
            {
                "Funballer Name": funballer_name,
                "Gameweek Number": gameweek_no,
                "Team Choice": team_choice,
                "Player Choice": player_choice,
            }
        )
    )

    st.title("")  # Used as divider
    st.subheader("Submit Choices")

    with st.form(key="submit_choices"):
        cols = st.beta_columns(4)
        funballer_name = cols[0].text_input("Funballer Name:")
        gameweek_no = cols[1].number_input("Gameweek No:", 1)
        team_choice = cols[2].selectbox(label="Team Name:", options=get_team_names())
        player_choice = cols[3].text_input("Player Choice:")

        submit_choices = st.form_submit_button("Submit Choices")

    if submit_choices:
        post_payload = {
            "funballer_name": funballer_name,
            "gameweek_no": gameweek_no,
            "team_choice": team_choice,
            "player_choice": player_choice,
        }

        submit_choices_request = requests.post(
            url=f"{fantasy_funball_url}funballer/choices/{funballer_name}",
            data=post_payload,
        )

        if submit_choices_request.status_code == status.HTTP_201_CREATED:
            st.markdown("Gameweek selection submitted! :white_check_mark:")
        elif submit_choices_request.status_code == status.HTTP_200_OK:
            st.markdown("Gameweek selection updated! :ballot_box_with_check:️")
        elif submit_choices_request.status_code in {
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_404_NOT_FOUND,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        }:
            st.error("Please check inputs and try again")
