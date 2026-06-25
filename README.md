#  Stock Forecasting Dashboard

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=flat&logo=tensorflow&logoColor=white)
![Scikit--learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=flat&logo=scikitlearn&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=flat&logo=chartdotjs&logoColor=white)

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


Tech Stack
           Layer	Technologies Used
           
  Frontend    	React.js, Chart.js, Axios
                
  Backend	      Flask, TensorFlow/Keras, Scikit-Learn
                
  Data	        NumPy, Pandas, Pickle
                
 Visualization	Matplotlib
                
  Deployment	  Render 

### Dashboard Preview()

<img width="884" height="418" alt="image" src="https://github.com/user-attachments/assets/9a7c6236-beac-4ee9-925f-0f01d8f450bf" />




