#  Stock Forecasting Dashboard

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Backend-black.svg)
![React](https://img.shields.io/badge/React-Frontend-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-DeepLearning-orange.svg)
![Status](https://img.shields.io/badge/Project-Completed-success.svg)

An **interactive full-stack stock forecasting dashboard** powered by **LSTM deep learning models**, featuring a **React-based UI** and **Flask backend API**.  
This project predicts future stock prices of major corporations across **China 🇨🇳, Japan 🇯🇵, and India 🇮🇳**.

---

##  Project Highlights

- **Full-Stack Machine Learning Application**  
- **Time-Series Forecasting using LSTM Networks**  
- **Interactive & Responsive Dashboard**  
- **Supports Multi-Country Stock Analysis**

---

##  Features

- Forecasts future stock prices of leading corporations  
- Displays **Current vs Forecasted Price Trends**  
- Produces **short-term predictions (1–100 days)**  
- Visualizes **High & Low probable future prices**  
- Interactive charts using **React + Chart.js**  
- Backend powered by **Flask, TensorFlow & Scikit-learn**  
- Model evaluation using **RMSE metrics**

---

##  Machine Learning Details

- Model: **LSTM (Long Short-Term Memory)**
- Framework: **TensorFlow / Keras**
- Scaling: **MinMaxScaler**
- Evaluation Metric: **RMSE**
- Saved Artifacts:
  - Trained Models (`.h5`)
  - Scalers (`.pkl`)
  - Preprocessed Data

---

##  Project Structure
```
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
```

##  Setup Instructions

### 🔹 Backend Setup (Flask API)

```
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run Flask app
python backend/app.py
```

### 🔹 Frontend Setup (React Dashboard)
```
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
<img width="857" height="303" alt="image" src="https://github.com/user-attachments/assets/f2a3f5ca-24e8-4aee-b14f-e5d1568cc771" />
<img width="848" height="379" alt="image" src="https://github.com/user-attachments/assets/fd4cce39-0f71-41a3-a584-861d71b60f06" />
<img width="1250" height="777" alt="Screenshot 2025-12-25 143725" src="https://github.com/user-attachments/assets/11d0e188-0a35-49c5-9c6c-104d5f653f95" />
<img width="1312" height="660" alt="Screenshot 2025-12-25 143730" src="https://github.com/user-attachments/assets/3938a2eb-306f-4957-b451-e7b6d63d743e" />
<img width="1390" height="370" alt="Screenshot 2025-12-25 143738" src="https://github.com/user-attachments/assets/56258856-50e5-49dc-bce9-55d50985a126" />



