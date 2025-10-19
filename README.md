**Dashboard for Stock Forecasting**

 An interactive React dashboard driven by a Flask backend displays the results of a full-stack machine learning and data science project that uses LSTM deep learning models to forecast future stock values.

 🔷**Features**

 -Forecasts the future stock prices of leading corporations in **China, Japan, and India**.

 -Shows **Current vs. Forecasted** Price Trends

  -Produces short-term **predictions (1 to 100)**

 -**React and Chart** were used to create the interactive dashboard. J.S.

  -Indicates both **high and low probable** future prices.

 -Backend developed with **Scikit-learn, Flask, and TensorFlow**

 Project Structure
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
├── Procfile                 # For deployment (Render/Heroku)
└── README.md                # Project documentation
```
