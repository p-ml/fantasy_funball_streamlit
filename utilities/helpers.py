import json
import os
from datetime import datetime

import pytz
import requests


def determine_gameweek_no():
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

    # Get upcoming gameweek
    gameweek_no += 1

    return gameweek_no
