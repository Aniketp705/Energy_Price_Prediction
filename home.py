import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import account
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import firebase_admin
from firebase_admin import credentials, auth, firestore

# Initialize Firestore client for database interactions
db = firestore.client()

# Retrieve the username from session state to use in data storage
username = account.st.session_state.username

# Set up Firebase credentials (commented out initialization line for clarity)
cred = credentials.Certificate('energy-price-prediction.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://energy-price-prediction-1679b-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Preprocesses the input data by handling missing values, dropping unnecessary columns
def preprocess_data(data):
    # Fill missing values with forward fill method and remove duplicate rows
    data.fillna(method='ffill', inplace=True)
    data = data.drop_duplicates()
    
    # Drop specific columns that are not needed for analysis
    data = data.drop(['generation hydro pumped storage aggregated', 'forecast wind offshore eday ahead'], axis=1)
    data = data.drop(['time'], axis=1)
    
    # Calculate percentages of NaN values and drop columns with high null values
    nan_percentages = round(data.isna().sum() / len(data) * 100, 2)
    null_values = ['generation marine', 'generation geothermal', 'generation fossil peat',
                   'generation wind offshore', 'generation fossil oil shale', 'generation fossil coal-derived gas']
    data = data.drop(null_values, axis=1)

    return data

# Function to predict energy price based on the processed data
def predict_price(data):
    # Separate features (x) and target variable (y)
    x = data.drop(['price actual'], axis=1)
    y = data['price actual']
    
    # Scale features for better performance in linear regression
    scaler = MinMaxScaler()
    x = scaler.fit_transform(x)
    
    # Split data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    
    # Train linear regression model and make predictions
    model = LinearRegression()
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    
    # Calculate mean squared error to evaluate model performance
    mse = mean_squared_error(y_test, y_pred)

    return y_pred, mse

# Function to store prediction data in Firestore database
def store_data(username, prediction, accuracy):
    # Reference user's predictions document in Firestore
    references = db.collection('predictions').document(username)
    
    # Store accuracy and prediction values in Firestore with merging option
    references.set({
        'accuracy(MSE)': accuracy,
        'predicted values': prediction.tolist()
    }, merge=True)

# Main Streamlit app
def app():
    st.title('Home')

    st.title('Welcome to the Energy Price Prediction App!')
    # Display a welcome message for signed-in users
    if st.session_state.signout:
        # Display a welcome message for signed-in users
        st.markdown("""
        <style>
            .big-font {
                font-size:20px !important;
            }
        </style>""", unsafe_allow_html=True)
        st.markdown('<p class="big-font">Welcome back, {}</p>'.format(username), unsafe_allow_html=True)

        # Radio button for selecting options between making a prediction or viewing past predictions
        choice = st.radio('Select an option', ['Predict', 'View Prediction'])

        if choice == 'Predict':
            # Prompt user to upload a CSV file for prediction
            st.write('Please enter the CSV file to predict the energy price')
            uploaded_file = st.file_uploader("Choose a file")
            
            if st.button('Predict'):
                # Process the file and display predictions if a file is uploaded
                if uploaded_file is not None:
                    sample_data = pd.read_csv(uploaded_file)
                    
                    # Take a sample of the data for faster processing
                    data = sample_data.sample(frac=0.1, random_state=42)
                    
                    # Preprocess the sampled data
                    processed_data = preprocess_data(data)
                    st.write(processed_data)
                    
                    # Display a histogram of the target variable for distribution insights
                    plt.figure(figsize=(15, 10))
                    sns.histplot(processed_data, x='price actual')
                    st.pyplot(plt)
                    
                    # Make predictions and display results
                    prediction, accuracy = predict_price(processed_data)
                    st.write('The predicted prices are:', prediction)
                    st.write('The mean squared error is:', accuracy)
                    
                    # Store prediction data in the Firestore database
                    store_data(username, prediction, accuracy)
                    st.success('Data stored successfully')
                else:
                    # Show error if file is not uploaded
                    st.error('Please upload a file')

        elif choice == 'View Prediction':
            # Retrieve and display user's previous predictions from Firestore
            references = db.collection('predictions').document(username).get()
            
            # Check if predictions exist for the user and display, otherwise show error
            if references.exists:
                data = references.to_dict()
                st.write('The accuracy was:', data['accuracy(MSE)'])
                st.write('The predicted values are:', data['predicted values'])
            else:
                st.error('No predictions found')

    else:
        # Display a message for signed-out users
        st.write('Please sign in to access the prediction features')
    
    
    

