import streamlit as st


def about_app():
    st.subheader("Game Overview")
    st.markdown(
        """
            Each funballer chooses one team and one player for each gameweek. If their chosen team wins, they'll be 
            awarded 1 point. Likewise if their chosen player scores or assists, they'll be awarded 1 point.

            All choices must be made by the gameweek deadline, which is typically 90 minutes before the first kickoff
            of the gameweek.

            Throughout the season, each funballer can choose any team twice and any player once.

            If a chosen team does not play in a gameweek, that funballer will be randomly allocated a team from the 
            remaining teams they have not already chosen twice.

            A player must start or be subbed on to have count as "played". If a chosen player does not make it onto 
            the pitch, the funballer will be randomly allocated a midfielder or forward (that they have not already chosen) 
            from any Premier League team.

            The app will check for results once a day (at midnight) and update standings accordingly.

            The Premier League Fantasy Football API is used as a data source.
        """
    )
