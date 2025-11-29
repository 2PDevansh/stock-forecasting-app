import json
import pickle
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import pandas as pd
import traceback
import logging

# ------------------------
# App / Logging setup
# ------------------------
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

# ------------------------
# Paths: adjust if your tree differs
# ------------------------
DATASET_DIR = "dataset"
PLOTS_DIR = "plots"
os.makedirs(PLOTS_DIR, exist_ok=True)

# ------------------------
# Model / Scaler / Dataset Paths
# ------------------------
models = {
    "HDFC": "models/hdfc_model.h5",
    "Reliance": "models/stock_price_model.h5",
    "Adani": "models/adani_model.h5",
    "TCS": "models/tcs_model.h5",
    "Honda": "models/honda_model.h5",
    "Sony": "models/sony_model.h5",
    "Nintendo": "models/nintendo_model.h5",
    "Alibaba": "models/alibaba_model.h5",
    "Xiaomi": "models/xiaomi_model.h5",
    "Tencent": "models/tencent_stock_price_model.h5",
    "Toyota": "models/toyota_stock_price_model.h5",
    "JD.com Inc": "models/jdhk_model.h5",
}

scalers = {
    "HDFC": "scalers/hdfc_scaler.pkl",
    "Reliance": "scalers/nse_scaler.pkl",
    "TCS": "scalers/tcs_scaler.pkl",
    "Adani": "scalers/adani_scaler.pkl",
    "Honda": "scalers/honda_scaler.pkl",
    "Sony": "scalers/sony_scaler.pkl",
    "Nintendo": "scalers/nintendo_scaler.pkl",
    "Alibaba": "scalers/alibaba_scaler.pkl",
    "Xiaomi": "scalers/xiaomi_scaler.pkl",
    "Tencent": "scalers/tencent_scaler.pkl",
    "Toyota": "scalers/toyota_scaler.pkl",
    "JD.com Inc": "scalers/jdhk_scaler.pkl",
}

datasets = {
    "HDFC": "scaled_data/hdfc_scaled_data.pkl",
    "Reliance": "scaled_data/nse_scaled_data.pkl",
    "TCS": "scaled_data/tcs_scaled_data.pkl",
    "Adani": "scaled_data/adani_scaled_data.pkl",
    "Honda": "scaled_data/honda_scaled_data.pkl",
    "Sony": "scaled_data/sony_scaled_data.pkl",
    "Nintendo": "scaled_data/nintendo_scaled_data.pkl",
    "Alibaba": "scaled_data/alibaba_scaled_data.pkl",
    "Xiaomi": "scaled_data/xiaomi_scaled_data.pkl",
    "Tencent": "scaled_data/tencent_scaled_data.pkl",
    "Toyota": "scaled_data/toyota_scaled_data.pkl",
    "JD.com Inc": "scaled_data/jdhk_scaled_data.pkl",
}

# ------------------------
# Load CSV Data (robust)
# ------------------------
def load_csv(path):
    try:
        df = pd.read_csv(path)
        # normalize column names to lowercase & strip spaces
        df.columns = df.columns.str.strip().str.lower()
        return df
    except FileNotFoundError:
        logging.error(f"CSV file not found: {path}")
        return pd.DataFrame()
    except Exception:
        logging.error(f"Error loading CSV {path}:\n{traceback.format_exc()}")
        return pd.DataFrame()

company_risk_df = load_csv(os.path.join(DATASET_DIR, "company_risk.csv"))
country_grsi_df = load_csv(os.path.join(DATASET_DIR, "country_GRSI.csv"))

# ------------------------
# Helper: fuzzy match company name (exact, then contains)
# ------------------------
def find_company_row(company_name: str):
    if company_risk_df.empty:
        return pd.DataFrame()
    name = company_name.strip().lower()
    # exact (case-insensitive)
    exact = company_risk_df[company_risk_df["company"].str.lower() == name]
    if not exact.empty:
        return exact.iloc[[0]]
    # contains
    contains = company_risk_df[company_risk_df["company"].str.lower().str.contains(name)]
    if not contains.empty:
        return contains.iloc[[0]]
    # no match
    return pd.DataFrame()

# ------------------------
# Health check
# ------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend running. Use /predict and /grsi endpoints."})

# ------------------------
# Company risk list
# ------------------------
@app.route("/company_risk", methods=["GET"])
def get_company_risk():
    try:
        return jsonify(company_risk_df.to_dict(orient="records"))
    except Exception:
        logging.error(traceback.format_exc())
        return jsonify({"error": "Failed to return company risk data"}), 500

# ------------------------
# Country GRSI list
# ------------------------
@app.route("/country_GRSI", methods=["GET"])
def get_country_grsi():
    try:
        return jsonify(country_grsi_df.to_dict(orient="records"))
    except Exception:
        logging.error(traceback.format_exc())
        return jsonify({"error": "Failed to return country GRSI data"}), 500

# ------------------------
# GRSI lookup (company-specific or full country map)
# ------------------------
@app.route("/grsi", methods=["GET"])
def get_grsi():
    try:
        company = request.args.get("company")
        if company:
            row = find_company_row(company)
            if row.empty:
                return jsonify({"error": "Company not found"}), 404
            # column is 'grsi' after normalization
            score = row.iloc[0].get("grsi")
            if pd.isna(score):
                return jsonify({"error": "GRSI value missing for company"}), 404
            # return uppercase key 'GRSI' to match frontend expectation
            return jsonify({"company": row.iloc[0]["company"], "GRSI": float(score)}), 200

        # no company given -> return country-level map
        if country_grsi_df.empty:
            return jsonify({"GRSI": {}}), 200
        # country and grsi columns expected
        if "country" in country_grsi_df.columns and "grsi" in country_grsi_df.columns:
            country_scores = dict(zip(country_grsi_df["country"], country_grsi_df["grsi"].astype(float)))
            return jsonify({"GRSI": country_scores}), 200
        else:
            return jsonify({"GRSI": {}}), 200

    except Exception:
        logging.error(traceback.format_exc())
        return jsonify({"error": "Unexpected server error"}), 500

# ------------------------
# Safe helper: check file exists
# ------------------------
def file_exists(path):
    return os.path.exists(path) and os.path.isfile(path)

# ------------------------
# Predict endpoint
# ------------------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json() or {}
        company = data.get("company")
        days = int(data.get("days", 5))

        if not company:
            return jsonify({"error": "Company is required"}), 400

        if company not in models:
            # tolerate case-insensitive mapping: try to find a key equal ignoring case
            match_key = next((k for k in models.keys() if k.lower() == company.lower()), None)
            if match_key:
                company_key = match_key
            else:
                # continue but return an error listing available companies
                return jsonify({"error": f"Invalid company. Available: {list(models.keys())}"}), 400
        else:
            company_key = company

        model_path = models[company_key]
        scaler_path = scalers.get(company_key)
        dataset_path = datasets.get(company_key)

        # Check files exist
        missing = []
        if not file_exists(model_path):
            missing.append(model_path)
        if not file_exists(scaler_path):
            missing.append(scaler_path)
        if not file_exists(dataset_path):
            missing.append(dataset_path)
        if missing:
            msg = f"Missing files for {company_key}: {missing}"
            logging.error(msg)
            return jsonify({"error": msg}), 500

        # Load model, scaler, dataset
        try:
            model = tf.keras.models.load_model(model_path, compile=False)
        except Exception:
            logging.error(f"Failed to load model {model_path}:\n{traceback.format_exc()}")
            return jsonify({"error": f"Failed to load model for {company_key}"}), 500

        try:
            with open(scaler_path, "rb") as f:
                scaler = pickle.load(f)
        except Exception:
            logging.error(f"Failed to load scaler {scaler_path}:\n{traceback.format_exc()}")
            return jsonify({"error": f"Failed to load scaler for {company_key}"}), 500

        try:
            with open(dataset_path, "rb") as f:
                data_scaled = pickle.load(f)
        except Exception:
            logging.error(f"Failed to load dataset {dataset_path}:\n{traceback.format_exc()}")
            return jsonify({"error": f"Failed to load dataset for {company_key}"}), 500

        # Ensure data_scaled is a numpy array
        data_scaled = np.array(data_scaled)
        if data_scaled.ndim == 1:
            # make it 2D with single column
            data_scaled = data_scaled.reshape(-1, 1)

        seq_length = 60
        if len(data_scaled) < seq_length + 1:
            return jsonify({"error": f"Not enough historical data for {company_key} (need > {seq_length})"}), 500

        # Build X,y
        X, y = [], []
        for i in range(seq_length, len(data_scaled)):
            X.append(data_scaled[i - seq_length:i])
            y.append(data_scaled[i, 0])
        X = np.array(X)
        y = np.array(y)

        # Predictions
        preds = model.predict(X, verbose=0)

        # preds might be shape (n,1) or (n,)
        preds_arr = preds.reshape(-1, 1) if preds.ndim == 1 else preds

        # Prepare for inverse_transform: pad with zeros for remaining features
        n_features = data_scaled.shape[1]
        if n_features < 1:
            return jsonify({"error": "Dataset has no features"}), 500

        pad_width_pred = np.zeros((preds_arr.shape[0], max(0, n_features - preds_arr.shape[1])))
        preds_padded = np.concatenate([preds_arr, pad_width_pred], axis=1) if n_features > preds_arr.shape[1] else preds_arr[:, :n_features]

        try:
            preds_rescaled = scaler.inverse_transform(preds_padded)[:, 0]
        except Exception:
            logging.error("Scaler inverse_transform failed:\n" + traceback.format_exc())
            return jsonify({"error": "Scaler inverse_transform failed"}), 500

        # Rescale y (actual)
        y_arr = y.reshape(-1, 1)
        pad_y = np.zeros((y_arr.shape[0], max(0, n_features - 1)))
        y_padded = np.concatenate([y_arr, pad_y], axis=1)
        try:
            y_rescaled = scaler.inverse_transform(y_padded)[:, 0]
        except Exception:
            logging.error("Scaler inverse_transform failed for y:\n" + traceback.format_exc())
            return jsonify({"error": "Scaler inverse_transform failed"}), 500

        # Save plot
        try:
            plt.figure(figsize=(10, 6))
            plt.plot(y_rescaled[-100:], label="Actual Prices", linewidth=2)
            plt.plot(preds_rescaled[-100:], label="Predicted Prices", linestyle="--", linewidth=2)
            plt.title(f"Actual vs Predicted Stock Prices ({company_key})")
            plt.xlabel("Days")
            plt.ylabel("Stock Price")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plot_filename = f"{company_key}_actual_vs_predicted.png"
            plot_path = os.path.join(PLOTS_DIR, plot_filename)
            plt.savefig(plot_path)
            plt.close()
            plot_url = f"http://127.0.0.1:5000/plots/{plot_filename}"
        except Exception:
            logging.error("Failed to create/save plot:\n" + traceback.format_exc())
            plot_url = None

        # Forecast future days (iterative)
        last_seq = data_scaled[-seq_length:]
        current_input = last_seq.reshape(1, seq_length, -1)
        forecast = []
        for _ in range(days):
            pred = model.predict(current_input, verbose=0)
            val = float(pred[0][0]) if hasattr(pred, "shape") else float(pred[0])
            forecast.append(val)
            # create new input: drop first, append padded pred
            new_row = np.concatenate((np.array([[val]]), np.zeros((1, n_features - 1))), axis=1) if n_features > 1 else np.array([[val]])
            new_input = np.vstack([current_input[0][1:], new_row])
            current_input = new_input.reshape(1, seq_length, -1)

        # inverse transform forecast
        forecast_arr = np.array(forecast).reshape(-1, 1)
        pad_fore = np.zeros((forecast_arr.shape[0], max(0, n_features - 1)))
        forecast_padded = np.concatenate([forecast_arr, pad_fore], axis=1)
        try:
            forecast_rescaled = scaler.inverse_transform(forecast_padded)[:, 0]
        except Exception:
            logging.error("Scaler inverse_transform failed for forecast:\n" + traceback.format_exc())
            return jsonify({"error": "Scaler inverse_transform failed for forecast"}), 500

        # GeoRisk lookup (company risk and country GRSI)
        company_row = find_company_row(company_key)
        company_risk_value = None
        country_grsi_value = None
        if not company_row.empty:
            if "grsi" in company_row.columns:
                company_risk_value = float(company_row.iloc[0]["grsi"])
            if "country" in company_row.columns:
                comp_country = company_row.iloc[0]["country"]
                # find country GRSI
                if not country_grsi_df.empty and "country" in country_grsi_df.columns and "grsi" in country_grsi_df.columns:
                    country_row = country_grsi_df[country_grsi_df["country"].str.lower() == str(comp_country).lower()]
                    if not country_row.empty:
                        country_grsi_value = float(country_row.iloc[0]["grsi"])

        result = {
            "company": company_key,
            "low_likely": float(min(forecast_rescaled)),
            "high_likely": float(max(forecast_rescaled)),
            "forecast": forecast_rescaled.tolist(),
            "plot_url": plot_url,
            "company_risk": company_risk_value,
            "country_grsi": country_grsi_value,
        }

        return jsonify(result)

    except Exception:
        logging.error("Unhandled error in /predict:\n" + traceback.format_exc())
        return jsonify({"error": "Unexpected error occurred"}), 500

# ------------------------
# Serve plot images
# ------------------------
@app.route("/plots/<filename>")
def get_plot(filename):
    plot_dir = os.path.join(os.getcwd(), PLOTS_DIR)
    return send_from_directory(plot_dir, filename)

# ------------------------
# Run app
# ------------------------
if __name__ == "__main__":
    logging.info("Starting backend on http://127.0.0.1:5000")
    app.run(debug=True)
