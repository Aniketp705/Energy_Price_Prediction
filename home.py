import streamlit as st



def app():
    st.title('Home')
    st.title('Welcome to the Energy Price Prediction App!')
    st.write('Please enter the following features to predict the price of energy')

    feature1 = st.text_input('Enter feature 1')
    feature2 = st.text_input('Enter feature 2')
    feature3 = st.text_input('Enter feature 3')
    feature4 = st.text_input('Enter feature 4')
    feature5 = st.text_input('Enter feature 5')

    st.button('Predict')