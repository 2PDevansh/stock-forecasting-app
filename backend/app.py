import json
import pickle
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify
from flask_cors import CORS

# ------------------------
# Flask app
# ------------------------
app = Flask(__name__)
CORS(app)

# ------------------------
# Model / Scaler / Data paths
# ------------------------
models = {
    "HDFC": "backend/models/hdfc_model.h5",
    "Reliance": "backend/models/stock_price_model.h5",
    "Adani": "backend/models/adani_model.h5",
    "TCS": "backend/models/tcs_model.h5",
    "Honda": "backend/models/honda_model.h5",
    "Sony": "backend/models/sony_model.h5",
    "Nintendo": "backend/models/nintendo_model.h5",
    "Alibaba": "backend/models/alibaba_model.h5",
    "Xiaomi": "backend/models/xiaomi_model.h5",    
    "Tencent": "backend/models/tencent_stock_price_model.h5",
    "Toyota": "backend/models/toyota_stock_price_model.h5",
    "JD.com Inc": "backend/models/jdhk_model.h5",
}

scalers = {
    "HDFC": "backend/scalers/hdfc_scaler.pkl",
    "Reliance": "backend/scalers/nse_scaler.pkl",
    "TCS": "backend/scalers/tcs_scaler.pkl",
    "Adani": "backend/scalers/adani_scaler.pkl",
    "Honda": "backend/scalers/honda_scaler.pkl",
    "Sony": "backend/scalers/sony_scaler.pkl",
    "Nintendo": "backend/scalers/nintendo_scaler.pkl",
    "Alibaba": "backend/scalers/alibaba_scaler.pkl",
    "Xiaomi": "backend/scalers/xiaomi_scaler.pkl",
    "Tencent": "backend/scalers/tencent_scaler.pkl",
    "Toyota": "backend/scalers/toyota_scaler.pkl",
    "JD.com Inc": "backend/scalers/jdhk_scaler.pkl",
}

datasets = {
    "HDFC": "backend/scaled_data/hdfc_scaled_data.pkl",
    "Reliance": "backend/scaled_data/nse_scaled_data.pkl",
    "TCS": "backend/scaled_data/tcs_scaled_data.pkl",
    "Adani": "backend/scaled_data/adani_scaled_data.pkl",
    "Honda": "backend/scaled_data/honda_scaled_data.pkl",
    "Sony": "backend/scaled_data/sony_scaled_data.pkl",
    "Nintendo": "backend/scaled_data/nintendo_scaled_data.pkl",
    "Alibaba": "backend/scaled_data/alibaba_scaled_data.pkl",
    "Xiaomi": "backend/scaled_data/xiaomi_scaled_data.pkl",
    "Tencent": "backend/scaled_data/tencent_scaled_data.pkl",
    "Toyota": "backend/scaled_data/toyota_scaled_data.pkl",
    "JD.com Inc": "backend/scaled_data/jdhk_scaled_data.pkl",
}


# ------------------------
# Health check
# ------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend is running! Use /metrics or /predict."})

# ------------------------
# Return RMSE values
# ------------------------
@app.route("/metrics", methods=["GET"])
def get_metrics():
    try:
        with open("backend/metrics.json", "r") as f:
            metrics = json.load(f)
        return jsonify(metrics)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------------
# Predict next stock price
# ------------------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        company = data.get("company")
        days = int(data.get("days", 5))  # default 5 days forecast

        if company not in models:
            return jsonify({"error": "Invalid company"}), 400

        # Load model, scaler, dataset
        model = tf.keras.models.load_model(models[company], compile=False)
        scaler = pickle.load(open(scalers[company], "rb"))
        data_scaled = pickle.load(open(datasets[company], "rb"))

        # Prepare input sequence
        seq_length = 60
        last_seq = data_scaled[-seq_length:]
        X_input = np.array(last_seq).reshape(1, seq_length, -1)

        forecast = []
        current_input = X_input.copy()

        for _ in range(days):
            pred = model.predict(current_input, verbose=0)
            forecast.append(pred[0][0])

            # slide window: drop first row, add new pred
            new_row = np.concatenate(
                (pred, np.zeros((1, data_scaled.shape[1] - 1))), axis=1
            )
            new_input = np.vstack([current_input[0][1:], new_row])
            current_input = new_input.reshape(1, seq_length, -1)

        # Convert forecast into original scale
        forecast = np.array(forecast).reshape(-1, 1)
        forecast_padded = np.concatenate(
            (forecast, np.zeros((forecast.shape[0], data_scaled.shape[1] - 1))),
            axis=1
        )
        forecast_rescaled = scaler.inverse_transform(forecast_padded)[:, 0]

        result = {
            "company": company,
            "low_likely": float(min(forecast_rescaled)),
            "high_likely": float(max(forecast_rescaled)),
            "forecast": forecast_rescaled.tolist()
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


# ------------------------
# Run app
# ------------------------
if __name__ == "__main__":
    app.run(debug=True)
