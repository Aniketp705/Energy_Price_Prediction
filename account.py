import streamlit as st
import re
import firebase_admin
from firebase_admin import credentials, auth, firestore
import home

db = firestore.client()


"""
This module provides a Streamlit application for user authentication using Firebase.
Functions:
    app(): Main function to run the Streamlit app.
        - Handles user login and registration.
        - Manages session state for user authentication.
    Login(): Authenticates a user using Firebase Authentication.
        - Retrieves user by email.
        - Updates session state upon successful login.
        - Displays error message for invalid email or password.
    signout(): Signs out the current user.
        - Resets session state for user authentication.
Dependencies:
    - streamlit: For creating the web application interface.
    - re: For regular expression operations.
    - firebase_admin: For Firebase Authentication.
    - firebase_admin.credentials: For Firebase credentials.
    - firebase_admin.auth: For Firebase Authentication methods.
Session State Variables:
    - username: Stores the username of the logged-in user.
    - email: Stores the email of the logged-in user.
    - signout: Boolean flag to indicate if the user is signed out.
    - signedout: Boolean flag to indicate if the user is signed out.
Usage:
    Run the Streamlit app and navigate through the login and registration options.
    The app will handle user authentication and session management.
"""






def app():

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'email' not in st.session_state:
        st.session_state.email = ''

    #created a function to login
    def Login():
        try:
            user = auth.get_user_by_email(email)
            # print(user.uid)
            st.success('Login successful')

            st.session_state.username = user.uid
            st.session_state.email = user.email
            st.session_state.signout = True
            st.session_state.signedout = True


        except:
            st.error('Invalid email or password')

    #created a function to signout
    def signout():
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ''




    if 'signedout' not in st.session_state:
        st.session_state.signedout = False
    if 'signout' not in st.session_state:
        st.session_state.signout = False

    if not st.session_state['signedout']:

        st.title('Login / Register')

        choice = st.radio('Select an option', ['Login', 'Register'])
        if choice == 'Login':
            st.write('Login')
            email = st.text_input('Email')

            if email:
                if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    pass
                else:
                    st.error('Invalid email')

            st.text_input('Password', type='password')

            st.button('Login', on_click=Login)

        elif choice == 'Register':
            st.write('Register')
            
            email = st.text_input('Email')

            if email:
                if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    pass
                else:
                    st.error('Invalid email')

            username = st.text_input('Enter unique username')

            password = st.text_input('Password', type='password')
            confirm_pass = st.text_input('Confirm Password', type='password')

            if password != confirm_pass:
                st.error('Passwords do not match')

            if st.button('Register'):
                user = auth.create_user(email = email, password = password, uid = username)
                st.success('User created successfully')

    if st.session_state.signout:
        st.title('Account')
        st.text(f"Name:{st.session_state.username}")
        st.text(f"Email:{st.session_state.email}")
        st.button('Sign out', on_click=signout)

