from datetime import datetime
from typing import List

import pytz


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


def determine_gameweek_no(all_gameweek_data: List) -> int:
    """Uses local time to determine what gameweek number we are in"""
    # TODO: Can be improved, currently runs through all gameweeks
    current_datetime = _localise_datetime(datetime=datetime.now(), timezone="utc")

    gameweek_no = 0  # Season hasn't started yet
    for gameweek in all_gameweek_data:
        # Convert deadline str to datetime
        deadline_datetime = datetime.strptime(gameweek["deadline"], "%Y-%m-%dT%H:%M:%SZ")
        localised_deadline_datetime = _localise_datetime(
            datetime=deadline_datetime,
            timezone="utc",
        )

        if current_datetime > localised_deadline_datetime:
            gameweek_no = gameweek["gameweek_no"]

    return gameweek_no


def get_gameweek_deadline(gameweek_no: int, gameweek_data: List) -> str:
    """Gets the deadline for a specific gameweek"""
    # Season not started yet
    if gameweek_no == 0:
        gameweek_no += 1

    try:
        gameweek_deadline_utc = next(
            gameweek["deadline"]
            for gameweek in gameweek_data
            if gameweek["gameweek_no"] == gameweek_no
        )
    except StopIteration:
        return "Season finished."

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


def has_current_gameweek_deadline_passed(
    gameweek_no: int,
    gameweek_data: List,
) -> bool:
    current_gameweek_deadline = get_gameweek_deadline(
        gameweek_no=gameweek_no,
        gameweek_data=gameweek_data,
    )

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


def determine_default_gameweek_no(all_gameweek_data: List) -> int:
    """
    Determines the default gameweek no - returns the number of the next
    gameweek if the current gameweek deadline has passed.
    """
    gameweek_no_limit = determine_gameweek_no(all_gameweek_data=all_gameweek_data)

    if gameweek_no_limit == 0:
        gameweek_no_limit += 1

    current_gameweek_deadline_passed = has_current_gameweek_deadline_passed(
        gameweek_no=gameweek_no_limit,
        gameweek_data=all_gameweek_data,
    )
    if current_gameweek_deadline_passed:
        gameweek_no_limit += 1

    return gameweek_no_limit
