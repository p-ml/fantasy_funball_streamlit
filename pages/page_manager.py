from typing import Callable

import streamlit as st


class MultiPage:
    def __init__(self) -> None:
        self.pages = []

    def add_page(self, title: str, func: Callable) -> None:
        self.pages.append({"title": title, "function": func})

    def run(self) -> None:
        # Dropdown to select the page to run
        page = st.sidebar.selectbox(
            "App Navigation", self.pages, format_func=lambda page: page["title"]
        )

        # run the app function
        page["function"]()
