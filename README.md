**Dashboard for Stock Forecasting**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=flat&logo=tensorflow&logoColor=white)
![Scikit--learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=flat&logo=scikitlearn&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=flat&logo=chartdotjs&logoColor=white)

 An interactive React dashboard driven by a Flask backend displays the results of a full-stack machine learning and data science project that uses LSTM deep learning models to forecast future stock values.

 🔷**Features**

 -Forecasts the future stock prices of leading corporations in **China, Japan, and India**.

 -Shows **Current vs. Forecasted** Price Trends

  -Produces short-term **predictions (1 to 100)**

 -**React and Chart** were used to create the interactive dashboard. J.S.

  -Indicates both **high and low probable** future prices.

 -Backend developed with **Scikit-learn, Flask, and TensorFlow**

 **Project Structure**
 ```
stock-forecasting-app/
│
├── backend/
│   ├── models/              # Trained LSTM models (.h5)
│   ├── scalers/             # Data scaling objects (.pkl)
│   ├── scaled_data/         # Preprocessed data
│   ├── plots/               # Generated stock plots
│   ├── app.py               # Flask backend API
│   └── metrics.json         # Model RMSE values
│
├── frontend/
│   ├── src/
│   │   ├── App.js           # React dashboard UI
│   │   ├── components/      # UI components
│   │   └── assets/          # Icons / images
│   └── package.json
│
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```
**Setup Instructions**

🔹 **Backend Setup**
```
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # (Windows)
# source venv/bin/activate  # (macOS/Linux)

# Install dependencies
pip install -r requirements.txt

# Run Flask app
python backend/app.py
```
🔹 **Frontend Setup**
```
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run React app
npm start
```
**Tech Stack**

| Layer         | Technologies Used                     |
| ------------- | ------------------------------------- |
| Frontend      | React.js, Chart.js, Axios             |
| Backend       | Flask, TensorFlow/Keras, Scikit-Learn |
| Data Handling | NumPy, Pandas, Pickle                 |
| Visualization | Matplotlib                            |
| Deployment    | Render / Heroku                       |


**Devansh Prasad**

 devanshprasad798@gmail.com

 GitHub: 2PDevansh

