import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


def preprocess_data(data):
    # data = data.dropna()
    data = data.drop_duplicates()
    data = data.drop(['generation hydro pumped storage aggregated','forecast wind offshore eday ahead'], axis=1)
    data = data.drop(['time'], axis=1)
    nan_percentages = round(data.isna().sum() / len(data) * 100, 2)
    null_values= ['generation marine',
                 'generation geothermal',
                 'generation fossil peat',
                 'generation wind offshore',
                 'generation fossil oil shale',
                 'generation fossil coal-derived gas']
    data = data.drop(null_values, axis=1)


    return data

def predict_price(data):
    x = data.drop(['price actual'], axis = 1)
    y = data['price actual']
    scaler = MinMaxScaler()
    x = scaler.fit_transform(x)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(x_train, y_train)



def app():
    st.title('Home')
    st.title('Welcome to the Energy Price Prediction App!')
    st.write('Please enter the CSV file to predict the energy price')

    uploaded_file = st.file_uploader("Choose a file")
    if st.button('Predict'):
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)
            processed_data = preprocess_data(data)
            st.write(processed_data)
            plt.figure(figsize=(15, 10))
            sns.histplot(processed_data, x='price actual')
            st.pyplot(plt)
        else:
            st.error('Please upload a file')