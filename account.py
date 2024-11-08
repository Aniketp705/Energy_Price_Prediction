import streamlit as st
import re
import firebase_admin
from firebase_admin import credentials, auth, firestore
import home

# Initialize Firestore client for database interactions
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
Session State Variables:
    - username: Stores the username of the logged-in user.
    - email: Stores the email of the logged-in user.
    - signout: Boolean flag to indicate if the user is signed out.
    - signedout: Boolean flag to indicate if the user is signed out.
"""

def app():
    # Initialize session state variables if not already set
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'email' not in st.session_state:
        st.session_state.email = ''

    # Login function to authenticate user using Firebase
    def Login():
        try:
            user = auth.get_user_by_email(email)
            st.success('Login successful')

            # Update session state upon successful login
            st.session_state.username = user.uid
            st.session_state.email = user.email
            st.session_state.signout = True
            st.session_state.signedout = True
        except:
            st.error('Invalid email or password')

    # Function to handle user signout
    def signout():
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ''

    # Initialize additional session state variables
    if 'signedout' not in st.session_state:
        st.session_state.signedout = False
    if 'signout' not in st.session_state:
        st.session_state.signout = False

    # Display login or registration options if user is not signed in
    if not st.session_state['signedout']:
        st.title('Login / Register')

        choice = st.radio('Select an option', ['Login', 'Register'])

        # Login form
        if choice == 'Login':
            st.write('Login')
            email = st.text_input('Email')

            # Basic email validation
            if email:
                if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    st.error('Invalid email')

            # Password input and login button
            st.text_input('Password', type='password')
            st.button('Login', on_click=Login)

        # Registration form
        elif choice == 'Register':
            st.write('Register')
            email = st.text_input('Email')

            # Basic email validation
            if email:
                if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    st.error('Invalid email')

            username = st.text_input('Enter unique username')
            password = st.text_input('Password', type='password')
            confirm_pass = st.text_input('Confirm Password', type='password')

            # Ensure password and confirm password match
            if password != confirm_pass:
                st.error('Passwords do not match')

            # Register the new user if all conditions are met
            if st.button('Register'):
                user = auth.create_user(email=email, password=password, uid=username)
                st.success('User created successfully')

    # Account info and signout option for logged-in users
    if st.session_state.signout:
        st.title('Account')
        st.text(f"Name: {st.session_state.username}")
        st.text(f"Email: {st.session_state.email}")
        st.button('Sign out', on_click=signout)
