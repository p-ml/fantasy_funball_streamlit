import json
import os
from json import JSONDecodeError

import pandas as pd
import requests
import streamlit as st
from rest_framework import status

from utilities.helpers import determine_gameweek_no
from utilities.team_names import get_team_names


def get_funballer_name_from_pin(funballer_pin: str):
    """Gets funballer name from their pin"""
    funballers = [
        {
            "first_name": "Patrick",
            "pin": "1050",
        },
        {
            "first_name": "Ben",
            "pin": "8251",
        },
        {
            "first_name": "Henry",
            "pin": "5064",
        },
        {
            "first_name": "Will",
            "pin": "8285",
        },
        {
            "first_name": "Theo",
            "pin": "9306",
        },
        {
            "first_name": "Gordon",
            "pin": "0625",
        },
        {
            "first_name": "Josh",
            "pin": "9839",
        },
        {
            "first_name": "Adam",
            "pin": "9308",
        },
        {
            "first_name": "Ilya",
            "pin": "0322",
        },
        {
            "first_name": "Steve",
            "pin": "2361",
        },
    ]

    funballer_name = next(
        funballer["first_name"]
        for funballer in funballers
        if funballer["pin"] == funballer_pin
    )

    st.session_state.funballer_name = funballer_name


def choices_app():
    st.subheader("Login")
    login_form = st.form(key="login")
    funballer_pin = login_form.text_input("Funballer Pin:")
    login_bool = login_form.form_submit_button("Login")

    if login_bool:
        get_funballer_name_from_pin(funballer_pin=funballer_pin)

    st.title("")  # Used as divider

    st.subheader("View Choices")
    retrieve_choices_form = st.form(key="retrieve_choices")
    funballer_name = retrieve_choices_form.text_input(
        "Funballer Name:", "Patrick"
    ).capitalize()
    retrieve_choices_form.form_submit_button("Retrieve Funballer Choices")

    current_gameweek_no = determine_gameweek_no()

    fantasy_funball_url = os.environ.get("FANTASY_FUNBALL_URL")
    choices = requests.get(f"{fantasy_funball_url}funballer/choices/{funballer_name}")

    if funballer_name == st.session_state.get("funballer_name"):
        view_all_choices = True
    else:
        view_all_choices = False

    try:
        gameweek_json = json.loads(choices.text)

        if not view_all_choices:
            gameweek_data = [
                x
                for x in gameweek_json
                if x["gameweek_id__gameweek_no"] in range(1, current_gameweek_no - 1)
            ]
        else:
            gameweek_data = gameweek_json

        gameweek_no = [x["gameweek_id__gameweek_no"] for x in gameweek_data]
        team_choice = [x["team_choice__team_name"] for x in gameweek_data]
        player_choice = [
            f"{x['player_choice__first_name']} {x['player_choice__surname']}"
            for x in gameweek_data
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

    raw_player_data = requests.get(f"{fantasy_funball_url}players/")
    player_data_json = json.loads(raw_player_data.text)
    player_names = [player["name"] for player in player_data_json]

    with st.form(key="submit_choices"):
        cols_top = st.beta_columns(2)
        pin = cols_top[0].text_input("Funballer Pin:")
        gameweek_no = cols_top[1].number_input("Gameweek No:", 1)
        cols_bottom = st.beta_columns(2)
        team_choice = cols_bottom[0].selectbox(
            label="Team Choice:", options=get_team_names()
        )
        player_choice_name = cols_bottom[1].selectbox(
            label="Player Choice:", options=player_names
        )
        player_choice_id = next(
            player["id"]
            for player in player_data_json
            if player_choice_name == player["name"]
        )

        submit_choices = st.form_submit_button("Submit Choices")

    if submit_choices:
        post_payload = {
            "gameweek_no": gameweek_no,
            "team_choice": team_choice,
            "player_choice": player_choice_id,
        }

        submit_choices_request = requests.post(
            url=f"{fantasy_funball_url}funballer/choices/submit/{pin}",
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
            error_message = json.loads(submit_choices_request.text)["detail"]
            st.error(f"{error_message}")
