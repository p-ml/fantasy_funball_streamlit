# Fantasy Funball Streamlit
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/p-ml/fantasy_funball_streamlit/fantasy_funball.py)
![Testing Workflow](https://github.com/p-ml/fantasy_funball_streamlit/actions/workflows/testing_workflow.yml/badge.svg)

Simple Streamlit app to act as frontend for Fantasy Funball, hosted on streamlit sharing.

## Project Structure
- `src/interface`: Handles interactions with the backend _fantasy_funball_ API. 
- `src/pages`: Home of the Streamlit functions & pages.
- `src/utilities`: Utility functions used throughout the application.


## Testing
`pytest` is used for testing, and can be run with: `pytest tests/`. A GitHub Action
has been set up to run the tests on every push.


## Deployment
The app can be run locally with `python -m streamlit fantasy_funball.py`, which will use
port 8501 by default.

The app is hosted on Streamlit Sharing, where any push to `master` will be automatically deployed.


## Dependency Management & Linting
Poetry is used for dependency management, while a combination of `isort`, `black` and `flake8` are used for 
linting. These are enforced by `pre-commit` hooks (see `.pre-commit-config.yaml`) which 
can be installed locally via `pre-commit install`. Linting and testing config can be found in `tox.ini`.