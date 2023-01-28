import datetime

import pytest


@pytest.fixture
def dummy_datetime():
    return datetime.datetime(
        year=2022,
        month=1,
        day=2,
        hour=12,
        minute=0,
        second=0,
        tzinfo=None,
    )
