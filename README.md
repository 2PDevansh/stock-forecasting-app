# 📈 Stock Forecasting Dashboard

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Backend-black.svg)
![React](https://img.shields.io/badge/React-Frontend-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-DeepLearning-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Project-Active-success.svg)

An **interactive full-stack stock forecasting dashboard** powered by **LSTM deep learning models**, featuring a **React-based UI** and **Flask backend API**.  
This project predicts future stock prices of major corporations across **China 🇨🇳, Japan 🇯🇵, and India 🇮🇳**.

---

## 🚀 Project Highlights

✨ **Full-Stack Machine Learning Application**  
✨ **Time-Series Forecasting using LSTM Networks**  
✨ **Interactive & Responsive Dashboard**  
✨ **Supports Multi-Country Stock Analysis**

---

## 🔥 Features

✔️ Forecasts future stock prices of leading corporations  
✔️ Displays **Current vs Forecasted Price Trends**  
✔️ Produces **short-term predictions (1–100 days)**  
✔️ Visualizes **High & Low probable future prices**  
✔️ Interactive charts using **React + Chart.js**  
✔️ Backend powered by **Flask, TensorFlow & Scikit-learn**  
✔️ Model evaluation using **RMSE metrics**

---

## 🧠 Machine Learning Details

- Model: **LSTM (Long Short-Term Memory)**
- Framework: **TensorFlow / Keras**
- Scaling: **MinMaxScaler**
- Evaluation Metric: **RMSE**
- Saved Artifacts:
  - Trained Models (`.h5`)
  - Scalers (`.pkl`)
  - Preprocessed Data

---

## 🗂️ Project Structure


stock-forecasting-app/
│

├── backend/

│ ├── models/ # Trained LSTM models (.h5)

│ ├── scalers/ # Data scaling objects (.pkl)
│ ├── scaled_data/ # Preprocessed data
│ ├── plots/ # Generated stock plots
│ ├── app.py # Flask backend API
│ └── metrics.json # Model RMSE values
│
├── frontend/
│ ├── src/
│ │ ├── App.js # React dashboard UI
│ │ ├── components/ # UI components
│ │ └── assets/ # Icons / images
│ └── package.json
│
├── frontend_nicegui/
│ └── app.py # NICEGUI dashboard UI
│
├── requirements.txt # Python dependencies
└── README.md # Project documentation

---

## ⚙️ Setup Instructions

### 🔹 Backend Setup (Flask API)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run Flask app
python backend/app.py
🔹 Frontend Setup (React Dashboard)
bash
Copy code
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start React app
npm start
```


 ### Tech Stack
Layer	Technologies Used
Frontend	React.js, Chart.js, Axios
Backend	Flask, TensorFlow/Keras, Scikit-Learn
Data	NumPy, Pandas, Pickle
Visualization	Matplotlib
Deployment	Render / Heroku

### Dashboard Preview
