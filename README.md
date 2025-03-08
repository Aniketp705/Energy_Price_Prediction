# Energy_Price_Prediction

<img align="center" src="https://media.istockphoto.com/id/1338921291/photo/light-bulb-on-an-electricity-bill.jpg?s=612x612&w=0&k=20&c=GG_OnRegEIIdLZ98Bf_WyYVKpzNBSuOx3uliQ3eNbB8=" />

## Welcome to My Project!

This project utilizes **linear regression** to predict energy prices. It aligns with the **United Nations' 17 Sustainable Development Goals**, particularly:

> **Goal 7: Ensure access to affordable, reliable, sustainable, and modern energy for all.**

---

## Model Used

### Linear Regression
The model analyzes the relationship between various factors (demand, generation sources, and time-related data) to predict electricity prices based on historical trends.

---

## Dataset Overview

The dataset contains features related to energy generation, demand, and pricing:
- **Generation Sources**: Biomass, fossil fuels, solar, wind, nuclear, etc.
- **Forecasts**: Day-ahead solar, wind, and total load predictions.
- **Energy Prices**: Day-ahead and actual market prices.

The dataset spans a full year, capturing hourly price fluctuations.

---

## Model Performance

- **Mean Squared Error (MSE)**: Measures the average squared difference between predicted and actual prices. An MSE of **82** indicates reasonable accuracy.
- **R-squared**: Explains how well independent variables account for price variations. A score of **0.55** means the model explains 55% of the variability.

---

## Running the Application

1. Clone the repository:
   ```sh
   git clone https://github.com/Aniketp705/Energy_Price_Prediction.git
   ```
2. Navigate to the project directory:
   ```sh
   cd Energy_Price_Prediction
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the Streamlit application:
   ```sh
   streamlit run main.py
   ```
5. Upload a CSV file to generate predictions.

---

## Features

### 1. Prediction Model
- Uses **Linear Regression** for price predictions.
- Provides hourly forecasts for an entire year.

### 2. User Interface
- Built with **Streamlit** for an intuitive experience.
- Users can:
  - Upload CSV files with historical energy data.
  - View processed data and predictions.
  - Visualize actual vs. predicted prices through interactive plots.

### 3. Database Integration
- Uses **Firestore** to store:
  - Predicted values for future reference.
  - Model performance metrics.
  - User-specific data linked to login credentials.

---

## Firebase Setup

To use authentication and database storage, Firebase must be configured. **Firebase credentials are not included in this repository** for security reasons.

### Steps:

1. **Create a Firebase Project**
   - Visit [Firebase Console](https://console.firebase.google.com/) and create a project.

2. **Enable Authentication**
   - Go to **Authentication > Sign-in method** and enable **Email/Password Authentication**.

3. **Set Up Firestore Database**
   - Navigate to **Firestore Database** and create a new database.
   - Choose **production mode** or **test mode**.
   - Add a `predictions` collection to store user data.

4. **Generate Service Account Key**
   - Go to **Project Settings > Service Accounts**.
   - Click **Generate new private key**, download the JSON file, and rename it `firebase_key.json`.
   - Place it in the project’s root directory.

5. **Replace API Key**
   - In `app.py`, replace the Firebase API key with your project's key (found in **Project Settings > General > Web API Key**).

6. **Update Firestore Rules**
   - Go to **Firestore Database > Rules** and update them:
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
   ```sh
   pip install firebase-admin
   ```

---

## Contributing

Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a feature branch:
   ```sh
   git checkout -b feature/your-feature-name
   ```
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
