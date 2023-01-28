import streamlit as st

from interface import FunballInterface
from logic.choices import (
    _create_choices_dataframe,
    _create_submit_choices_form,
    _display_choices_dataframe,
    _display_choices_form,
    _display_funballers_remaining_picks,
)
from utilities.gameweek import determine_default_gameweek_no

st.set_page_config(
    page_title="Choices",
    page_icon=":soccer:",
    initial_sidebar_state="expanded",
)


def choices_app():
    st.subheader("View Choices")

    funballer_name = _display_choices_form()
    funball_interface = FunballInterface()

    all_gameweek_data = funball_interface.get_all_gameweek_data()

    gameweek_no_limit = determine_default_gameweek_no(
        all_gameweek_data=all_gameweek_data,
    )

    choices_data = funball_interface.get_choices_data(
        funballer_name=funballer_name,
        gameweek_no_limit=gameweek_no_limit,
    )

    choices_dataframe = _create_choices_dataframe(
        funballer_name=funballer_name,
        choices_data=choices_data,
    )

    _display_choices_dataframe(choices_dataframe=choices_dataframe)

    submit_choice_data = _create_submit_choices_form(
        default_gameweek_no=gameweek_no_limit,
    )

    if submit_choice_data.submit:
        funball_interface.post_choice(payload=submit_choice_data)

    _display_funballers_remaining_picks(funballer_name=funballer_name)


if __name__ == "__main__":
    choices_app()
