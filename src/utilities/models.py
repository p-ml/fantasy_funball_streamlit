from collections import namedtuple

ChoicesData = namedtuple(
    "ChoicesData",
    [
        "gameweek_no",
        "team_choice",
        "player_choice",
        "player_point_awarded",
        "team_point_awarded",
    ],
)

ValidTeamSelections = namedtuple(
    "ValidTeamSelections",
    [
        "team_names",
        "remaining_selections",
    ],
)

ColourMap = namedtuple(
    "ColourMap",
    [
        "team_points",
        "player_points",
    ],
)

SortedPlayerData = namedtuple("SortedPlayerData", ["player_names", "goals", "assists"])

SubmitChoiceData = namedtuple(
    "SubmitChoiceData",
    [
        "pin",
        "gameweek_no",
        "team_choice",
        "player_choice",
        "submit",
    ],
)
