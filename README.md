# Energy_Price_Prediction

<img align="center" src="https://media.istockphoto.com/id/1338921291/photo/light-bulb-on-an-electricity-bill.jpg?s=612x612&w=0&k=20&c=GG_OnRegEIIdLZ98Bf_WyYVKpzNBSuOx3uliQ3eNbB8=" />

## Welcome to My Project!

This project is based on using **linear regression** to predict energy prices. The project is aligned with the **17 Sustainable Development Goals** by the United Nations, specifically focusing on Goal 7:  
**"Ensure access to affordable, reliable, sustainable, and modern energy for all."**

---

## Model Used

### Linear Regression
Linear regression is employed to analyze relationships between energy prices and various factors like demand, generation sources, and time-related data. The model predicts electricity prices based on historical trends and the variables.

---

## Dataset Overview

The dataset includes features related to energy generation, demand, and pricing:
- **Generation Sources**: Biomass, fossil fuels, solar, wind, nuclear, etc.
- **Forecasts**: Day-ahead solar, wind, and total load predictions.
- **Energy Prices**: Day-ahead and actual market prices.

The data spans an entire year, allowing the model to capture hourly fluctuations in electricity prices.

---

## Results

- **Mean-Squared-Error (MSE)**:  
   Indicates the average squared difference between predicted and actual prices. An MSE of **82** suggests reasonable prediction accuracy.  
- **R-squared**:  
   Explains how well the independent variables account for price variations. A value of **0.55** suggests 55% of variability is explained by the model.

---

## Steps to Run the App on Your Machine

1. Clone the repository:
   ```sh
   git clone https://github.com/Aniketp705/Energy_Price_Prediction.git
   ```
2. Navigate to the project directory:
    ```sh
    cd Energy_Price_Prediction
    ```
3. Install all the required modules and libraries mentioned in the requirements.txt file:
    ```sh
    pip install -r requirements.txt
    ```
4. Run the Streamlit App:
    ```sh
    streamlit run main.py
    ```
5. Upload the data in csv format to get predictions.

## Features

1. **Prediction Model**  
   The application uses a **Linear Regression** model to predict electricity prices based on historical data. Predictions are made for the entire year on an hourly basis, capturing price variations.

2. **User Interface**  
   The app is built using **Streamlit**, providing a simple and intuitive interface. Users can:
   - Upload a CSV file containing historical energy data.
   - View processed data and predictions.
   - Visualize actual vs. predicted prices through interactive plots.

3. **Database Integration**  
   The application uses **Firestore** to store:
   - Predicted values for future reference.
   - Model performance metrics such as accuracy (R-squared).
   - User-specific data tied to their login credentials.


---

## Important Note

This application requires Firebase integration for authentication and database storage. **The Firebase credentials (key) are not included in this repository** for security reasons. You must set up your own Firebase project and generate the required configuration file to run the app successfully.

---

## Steps to Set Up Firebase

1. **Create a Firebase Project**  
   - Go to [Firebase Console](https://console.firebase.google.com/) and create a new project.  
   - Name your project and follow the steps to complete the setup.

2. **Enable Authentication**  
   - Navigate to the **Authentication** section.  
   - Click on the **Sign-in method** tab and enable **Email/Password Authentication**.

3. **Set Up Firestore Database**  
   - Go to the **Firestore Database** section and create a database.  
   - Choose **Start in production mode** or **test mode** as per your requirements.  
   - Add a `predictions` collection for storing user-specific data.  

4. **Generate Service Account Key**  
   - Go to **Project Settings** > **Service Accounts**.  
   - Click **Generate new private key** and download the JSON file.  
   - Rename this file as `firebase_key.json` and place it in the root directory of the project.

5. **Replace API Key**  
   - In the `app.py` file (or your main script), replace the placeholder for the API key with your Firebase API key, found in **Project Settings** > **General** > **Web API Key**.

6. **Update Database Rules**  
   - Navigate to **Firestore Database** > **Rules**, and update them as required:
     ```json
     rules_version = '2';
     service cloud.firestore {
       match /databases/{database}/documents {
         match /{document=**} {
           allow read, write: if request.auth != null;
         }
       }
     }
     ```

7. **Install Firebase Admin SDK**  
   Install the Firebase Admin SDK using the following command:
   ```sh
   pip install firebase-admin
   ```

## Contributions

Contributions are welcome! To contribute:
1. Fork this repository.
2. Create a feature branch:
   ```sh
   git checkout -b feature/your-feature-name
3. Commit your changes:
    ```sh
    git commit -m "Add your message"
    ```
4. Push the branch:
    ```sh
    git push origin feature/your-feature-name
    ```
5. Open a pull request.

---