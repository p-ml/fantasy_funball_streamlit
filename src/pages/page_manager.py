from typing import Callable

import streamlit as st
from streamlit_option_menu import option_menu


class MultiPage:
    def __init__(self) -> None:
        self.pages = []

    def add_page(self, title: str, func: Callable) -> None:
        self.pages.append({"title": title, "function": func})

    def run(self) -> None:
        # Dropdown to select the page to run
        with st.sidebar:
            selected = option_menu(
                "Navigation",
                [page["title"] for page in self.pages],
                menu_icon="list",
                icons=[
                    "arrow-down-up",
                    "book-half",
                    "grid",
                    "calendar3",
                    "people",
                ],
                default_index=1,
            )

        selected_page = next(
            page["function"] for page in self.pages if page["title"] == selected
        )
        selected_page()
