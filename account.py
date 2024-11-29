import streamlit as st
import re
import requests
import firebase_admin
from firebase_admin import credentials, firestore
from config import API_KEY
import home
import json

# Initialize Firebase Admin SDK for database interactions
cred = credentials.Certificate('energy-price-prediction.json')
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://energy-price-prediction-1679b-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

# Initialize Firestore client
db = firestore.client()


def firebase_login(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()  # Returns user info including ID token
    else:
        st.error("Invalid email or password.")
        return None

def firebase_register(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()  # Returns user info including ID token
    else:
        st.error("Failed to create user.")
        return None

def app():
    # Initialize session state variables if not already set
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'email' not in st.session_state:
        st.session_state.email = ''
    if 'signout' not in st.session_state:
        st.session_state.signout = False
    if 'signedout' not in st.session_state:
        st.session_state.signedout = False

    # Function to handle user sign-in
    def Login(email, password):
        user = firebase_login(email, password)
        if user:
            st.session_state.username = user['localId']
            st.session_state.email = user['email']
            st.session_state.signout = True
            st.session_state.signedout = True
            st.success('Login successful!')

    # Function to handle user registration
    def Register(email, password):
        user = firebase_register(email, password)
        if user:
            st.success("User created successfully!")

    # Function to handle user signout
    def signout():
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ''

    # Display login or registration options if user is not signed in
    if not st.session_state['signedout']:
        st.title('Login / Register')

        choice = st.radio('Select an option', ['Login', 'Register'])

        # Login form
        if choice == 'Login':
            st.write('Login')
            email = st.text_input('Email')
            password = st.text_input('Password', type='password')

            # Basic email validation
            if email:
                if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    st.error('Invalid email')

            # Login button
            if st.button('Login'):
                Login(email, password)

        # Registration form
        elif choice == 'Register':
            st.write('Register')
            email = st.text_input('Email')
            password = st.text_input('Password', type='password')
            confirm_pass = st.text_input('Confirm Password', type='password')

            # Ensure password and confirm password match
            if password != confirm_pass:
                st.error('Passwords do not match')

            # Register the new user if all conditions are met
            if st.button('Register'):
                Register(email, password)

    # Account info and signout option for logged-in users
    if st.session_state.signout:
        st.title('Account')
        st.text(f"Email: {st.session_state.email}")
        st.button('Sign out', on_click=signout)
