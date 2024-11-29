import streamlit as st
from streamlit_option_menu import option_menu
import firebase_admin
from firebase_admin import credentials, auth, firestore
import home
import about, account, home




st.set_page_config(page_title="Energy Price Prediction", page_icon=":bulb:")


class MultiApp:
    def __init__(self):
        self.apps = [
            home,
            account,
            about
        ]

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run():

        with st.sidebar:
            app = option_menu(
                menu_title='Menu',
                options=['Home', 'Account', 'About'],
                icons=['house-fill', 'person-fill', 'info-circle-fill'],
                menu_icon='🔍',
                default_index=0
            )

        if app == 'Home':
            home.app()
        elif app == 'Account':
            account.app()
        elif app == 'About':
            about.app()

    run()