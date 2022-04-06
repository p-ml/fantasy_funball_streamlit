from datetime import datetime
from typing import Dict, List

import pytz

from src.utilities import ChoicesData, ValidTeamSelections


class FunballInterfaceFormatter:
    @classmethod
    def _format_kickoffs(cls, kickoffs: List) -> List:
        """Format game kickoffs into Y-M-D H:M:S"""
        bst = pytz.timezone("Europe/London")

        formatted_kickoffs = [
            datetime.strftime(
                bst.fromutc(datetime.strptime(kickoff, "%Y-%m-%d %H:%M:%S")),
                "%H:%M",
            )
            for kickoff in kickoffs
        ]

        return formatted_kickoffs

    def format_gameweek_data(self, gameweek_data: List) -> Dict:
        """Format gameweek data by sorting by gameweek id"""
        # Sort into ascending order by date, can be done via "id"
        gameweek_sorted = sorted(gameweek_data, key=lambda x: x["id"])

        home_teams = [game["home_team__team_name"] for game in gameweek_sorted]
        away_teams = [game["away_team__team_name"] for game in gameweek_sorted]

        # TODO: potentially duplicated info between gameday__date and kickoff
        game_dates = [game["gameday__date"] for game in gameweek_sorted]
        game_kickoffs = [game["kickoff"] for game in gameweek_sorted]

        formatted_kickoffs = self._format_kickoffs(kickoffs=game_kickoffs)

        sorted_gameweek_data = {
            "home_teams": home_teams,
            "away_teams": away_teams,
            "game_dates": game_dates,
            "game_kickoffs": formatted_kickoffs,
        }

        return sorted_gameweek_data

    @classmethod
    def format_funballer_valid_team_selections(
        cls, remaining_valid_teams_data: List
    ) -> ValidTeamSelections:
        team_names = [response["team_name"] for response in remaining_valid_teams_data]
        remaining_selections = [
            response["remaining_selections"] for response in remaining_valid_teams_data
        ]

        valid_team_selections = ValidTeamSelections(
            team_names=team_names,
            remaining_selections=remaining_selections,
        )

        return valid_team_selections

    @classmethod
    def format_choices_data(cls, choices_data: List) -> ChoicesData:
        gameweek_no = [x["gameweek_id__gameweek_no"] for x in choices_data]
        team_choice = [x["team_choice__team_name"] for x in choices_data]
        player_choice = [
            f"{x['player_choice__first_name']} {x['player_choice__surname']}"
            for x in choices_data
        ]
        player_point_awarded = [x["player_point_awarded"] for x in choices_data]
        team_point_awarded = [x["team_point_awarded"] for x in choices_data]

        choices_data = ChoicesData(
            gameweek_no=gameweek_no,
            team_choice=team_choice,
            player_choice=player_choice,
            player_point_awarded=player_point_awarded,
            team_point_awarded=team_point_awarded,
        )

        return choices_data

    @classmethod
    def format_all_players_from_team(cls, player_data: List) -> Dict:
        player_names = [f"{x['first_name']} {x['surname']}" for x in player_data]
        goals = [x["goals"] for x in player_data]
        assists = [x["assists"] for x in player_data]

        formatted_player_data = {
            "player_names": player_names,
            "goals": goals,
            "assists": assists,
        }

        return formatted_player_data

    def format_funballer_data(self, funballer_data: List) -> Dict:
        funballer_names = [x["first_name"] for x in funballer_data]
        funballer_team_points = [x["team_points"] for x in funballer_data]
        funballer_player_points = [x["player_points"] for x in funballer_data]
        funballer_points = [x["points"] for x in funballer_data]

        funballer_data = {
            "funballer_names": funballer_names,
            "funballer_team_points": funballer_team_points,
            "funballer_player_points": funballer_player_points,
            "funballer_points": funballer_points,
        }

        return funballer_data
