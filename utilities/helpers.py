import json
import os
from datetime import datetime

import pytz
import requests


def determine_gameweek_no() -> int:
    """Uses local time to determine what gameweek number we are in"""
    # Retrieve list of gameweek objects, sorted by deadline
    fantasy_funball_url = os.environ.get("FANTASY_FUNBALL_URL")

    gameweek_info = requests.get(f"{fantasy_funball_url}gameweek/all/")
    gameweek_json = json.loads(gameweek_info.text)

    # Get current datetime
    current_datetime_tz_unaware = datetime.now()
    utc = pytz.timezone("UTC")
    current_datetime = utc.localize(current_datetime_tz_unaware)

    gameweek_no = 0  # Season hasn't started yet
    for gameweek in gameweek_json:
        # Convert deadline str to datetime
        deadline_datetime = datetime.strptime(
            gameweek["deadline"], "%Y-%m-%dT%H:%M:%SZ"
        )
        utc = pytz.timezone("UTC")
        deadline_datetime_aware = utc.localize(deadline_datetime)

        if current_datetime > deadline_datetime_aware:
            gameweek_no = gameweek["gameweek_no"]

    return gameweek_no


def get_gameweek_deadline(gameweek_no: int) -> str:
    """Gets the deadline for a specific gameweek"""
    # Retrieve list of gameweek objects, sorted by deadline
    fantasy_funball_url = os.environ.get("FANTASY_FUNBALL_URL")

    gameweek_info = requests.get(f"{fantasy_funball_url}gameweek/all/")
    gameweek_json = json.loads(gameweek_info.text)

    gameweek_deadline_utc = next(
        gameweek["deadline"]
        for gameweek in gameweek_json
        if gameweek["gameweek_no"] == gameweek_no
    )

    # Convert deadline from UTC
    gameweek_deadline_datetime = datetime.strptime(
        gameweek_deadline_utc, "%Y-%m-%dT%H:%M:%SZ"
    )
    bst = pytz.timezone("Europe/London")
    deadline_datetime_aware = bst.localize(gameweek_deadline_datetime)

    # Convert datetime obj back to str
    gameweek_deadline = datetime.strftime(
        bst.fromutc(deadline_datetime_aware),
        "%a %-d %B %Y @ %H:%M:%S",
    )

    return gameweek_deadline


def has_current_gameweek_deadline_passed():
    gameweek_no = determine_gameweek_no()
    current_gameweek_deadline = get_gameweek_deadline(gameweek_no=gameweek_no)

    # Get current datetime
    current_datetime_tz_unaware = datetime.now()
    utc = pytz.timezone("UTC")
    current_datetime = utc.localize(current_datetime_tz_unaware)

    gameweek_deadline = datetime.strptime(
        current_gameweek_deadline,
        "%a %d %B %Y @ %H:%M:%S",
    )
    gameweek_deadline_datetime = utc.localize(gameweek_deadline)

    if current_datetime > gameweek_deadline_datetime:
        return True

    return False


if __name__ == "__main__":
    has_current_gameweek_deadline_passed()
