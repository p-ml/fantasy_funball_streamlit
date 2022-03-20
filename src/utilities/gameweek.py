import json
from datetime import datetime
from typing import Dict

import pytz
import requests
import streamlit as st

FANTASY_FUNBALL_URL = st.secrets["FANTASY_FUNBALL_URL"]


def _localise_datetime(datetime: datetime, timezone: str) -> datetime:
    """
    Localise datetime into specified timezone. Currently supports
    "utc" and "bst".
    """
    if timezone == "utc":
        tz = pytz.timezone("utc")
    elif timezone == "bst":
        tz = pytz.timezone("Europe/London")
    else:
        raise Exception("Timezone not supported.")

    localised_datetime = tz.localize(datetime)

    return localised_datetime


def _retrieve_gameweek_data() -> Dict:
    gameweek_info = requests.get(f"{FANTASY_FUNBALL_URL}gameweek/all/")
    gameweek_data = json.loads(gameweek_info.text)

    return gameweek_data


def determine_gameweek_no() -> int:
    """Uses local time to determine what gameweek number we are in"""
    # TODO: Can be improved, currently runs through all gameweeks
    gameweek_data = _retrieve_gameweek_data()

    current_datetime = _localise_datetime(datetime=datetime.now(), timezone="utc")

    gameweek_no = 0  # Season hasn't started yet
    for gameweek in gameweek_data:
        # Convert deadline str to datetime
        deadline_datetime = datetime.strptime(
            gameweek["deadline"], "%Y-%m-%dT%H:%M:%SZ"
        )
        localised_deadline_datetime = _localise_datetime(
            datetime=deadline_datetime,
            timezone="utc",
        )

        if current_datetime > localised_deadline_datetime:
            gameweek_no = gameweek["gameweek_no"]

    return gameweek_no


def get_gameweek_deadline(gameweek_no: int) -> str:
    """Gets the deadline for a specific gameweek"""
    # Retrieve list of gameweek objects, sorted by deadline
    gameweek_data = _retrieve_gameweek_data()

    gameweek_deadline_utc = next(
        gameweek["deadline"]
        for gameweek in gameweek_data
        if gameweek["gameweek_no"] == gameweek_no
    )

    # Convert deadline from UTC to BST
    gameweek_deadline_datetime = datetime.strptime(
        gameweek_deadline_utc, "%Y-%m-%dT%H:%M:%SZ"
    )
    localised_gameweek_deadline = _localise_datetime(
        datetime=gameweek_deadline_datetime, timezone="bst"
    )

    # Convert datetime obj back to str, formatted to be displayed in front end
    # in the format: Sat 1 January 2022 @ 00:00:00
    gameweek_deadline = datetime.strftime(
        pytz.timezone("Europe/London").fromutc(localised_gameweek_deadline),
        "%a %-d %B %Y @ %H:%M:%S",
    )

    return gameweek_deadline


def has_current_gameweek_deadline_passed(gameweek_no: int) -> bool:
    current_gameweek_deadline = get_gameweek_deadline(gameweek_no=gameweek_no)

    current_datetime = _localise_datetime(
        datetime=datetime.now(),
        timezone="utc",
    )

    gameweek_deadline = datetime.strptime(
        current_gameweek_deadline,
        "%a %d %B %Y @ %H:%M:%S",
    )
    gameweek_deadline_datetime = _localise_datetime(
        datetime=gameweek_deadline,
        timezone="utc",
    )

    if current_datetime > gameweek_deadline_datetime:
        return True

    return False
