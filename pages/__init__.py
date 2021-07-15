from .choices import choices_app
from .gameweeks import gameweeks_app
from .page_manager import MultiPage
from .players import players_app
from .standings import standings_app

__all__ = [
    standings_app,
    gameweeks_app,
    choices_app,
    players_app,
    MultiPage,
]
