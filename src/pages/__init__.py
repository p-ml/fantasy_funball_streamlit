from src.pages.about import about_app
from src.pages.choices import choices_app
from src.pages.gameweeks import gameweeks_app
from src.pages.page_manager import MultiPage
from src.pages.players import players_app
from src.pages.standings import standings_app

__all__ = [
    standings_app,
    gameweeks_app,
    choices_app,
    players_app,
    about_app,
    MultiPage,
]
