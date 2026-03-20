import os
import pickle
import logging
import traceback

import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# ===================== APP SETUP =====================
app = Flask(__name__)
CORS(app)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

BASE_DIR = os.getcwd()
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
PLOTS_DIR = os.path.join(BASE_DIR, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

SEQ_LENGTH = 60

# ===================== MODEL / SCALER / DATA =====================
MODELS = {
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

SCALERS = {
    "HDFC": "scalers/hdfc_scaler.pkl",
    "Reliance": "scalers/nse_scaler.pkl",
    "Adani": "scalers/adani_scaler.pkl",
    "TCS": "scalers/tcs_scaler.pkl",
    "Honda": "scalers/honda_scaler.pkl",
    "Sony": "scalers/sony_scaler.pkl",
    "Nintendo": "scalers/nintendo_scaler.pkl",
    "Alibaba": "scalers/alibaba_scaler.pkl",
    "Xiaomi": "scalers/xiaomi_scaler.pkl",
    "Tencent": "scalers/tencent_scaler.pkl",
    "Toyota": "scalers/toyota_scaler.pkl",
    "JD.com Inc": "scalers/jdhk_scaler.pkl",
}

DATASETS = {
    "HDFC": "scaled_data/hdfc_scaled_data.pkl",
    "Reliance": "scaled_data/nse_scaled_data.pkl",
    "Adani": "scaled_data/adani_scaled_data.pkl",
    "TCS": "scaled_data/tcs_scaled_data.pkl",
    "Honda": "scaled_data/honda_scaled_data.pkl",
    "Sony": "scaled_data/sony_scaled_data.pkl",
    "Nintendo": "scaled_data/nintendo_scaled_data.pkl",
    "Alibaba": "scaled_data/alibaba_scaled_data.pkl",
    "Xiaomi": "scaled_data/xiaomi_scaled_data.pkl",
    "Tencent": "scaled_data/tencent_scaled_data.pkl",
    "Toyota": "scaled_data/toyota_scaled_data.pkl",
    "JD.com Inc": "scaled_data/jdhk_scaled_data.pkl",
}

# ===================== LOAD CSV DATA =====================
def load_csv(path):
    try:
        df = pd.read_csv(path)
        df.columns = df.columns.str.strip().str.lower()
        return df
    except Exception as e:
        logging.error(f"CSV load failed: {path} | {e}")
        return pd.DataFrame()

company_risk_df = load_csv(os.path.join(DATASET_DIR, "company_risk.csv"))
country_grsi_df = load_csv(os.path.join(DATASET_DIR, "country_GRSI.csv"))

# ===================== HELPERS =====================
def find_company(company: str):
    if company_risk_df.empty:
        return None

    name = company.strip().lower()
    exact = company_risk_df[company_risk_df["company"].str.lower() == name]
    if not exact.empty:
        return exact.iloc[0]

    contains = company_risk_df[company_risk_df["company"].str.lower().str.contains(name)]
    if not contains.empty:
        return contains.iloc[0]

    return None

def ensure_file(path):
    if not os.path.exists(path):
        raise FileNotFoundError(path)

# ===================== ROUTES =====================
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend running"})


# ---------- GRSI ----------
@app.route("/grsi", methods=["GET"])
def get_grsi():
    try:
        company = request.args.get("company")
        if not company:
            return jsonify({"error": "Company parameter missing"}), 400

        row = find_company(company)
        if row is None:
            return jsonify({"error": "Company not found"}), 404

        if "grsi" not in row or pd.isna(row["grsi"]):
            return jsonify({"error": "GRSI not available"}), 404

        return jsonify({
            "company": row["company"],
            "GRSI": float(row["grsi"])
        }), 200

    except Exception:
        logging.error(traceback.format_exc())
        return jsonify({"error": "Failed to fetch GRSI"}), 500


# ---------- PREDICT ----------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        payload = request.get_json(force=True)
        company = payload.get("company")
        days = int(payload.get("days", 5))

        if not company or company not in MODELS:
            return jsonify({"error": "Invalid company"}), 400

        model_path = MODELS[company]
        scaler_path = SCALERS[company]
        data_path = DATASETS[company]

        ensure_file(model_path)
        ensure_file(scaler_path)
        ensure_file(data_path)

        model = tf.keras.models.load_model(model_path, compile=False)
        scaler = pickle.load(open(scaler_path, "rb"))
        data_scaled = np.array(pickle.load(open(data_path, "rb")))

        if data_scaled.ndim == 1:
            data_scaled = data_scaled.reshape(-1, 1)

        if len(data_scaled) <= SEQ_LENGTH:
            return jsonify({"error": "Insufficient data"}), 400

        X, y = [], []
        for i in range(SEQ_LENGTH, len(data_scaled)):
            X.append(data_scaled[i - SEQ_LENGTH:i])
            y.append(data_scaled[i, 0])

        X = np.array(X)
        y = np.array(y)

        preds = model.predict(X, verbose=0).reshape(-1, 1)
        features = data_scaled.shape[1]

        preds_pad = np.hstack([preds, np.zeros((len(preds), features - 1))])
        y_pad = np.hstack([y.reshape(-1, 1), np.zeros((len(y), features - 1))])

        preds_real = scaler.inverse_transform(preds_pad)[:, 0]
        y_real = scaler.inverse_transform(y_pad)[:, 0]

        # ---------- SAVE PLOT ----------
        plot_url = None
        try:
            plt.figure(figsize=(10, 6))
            plt.plot(y_real[-100:], label="Actual Prices", linewidth=2)
            plt.plot(preds_real[-100:], label="Predicted Prices", linestyle="--", linewidth=2)
            plt.title(f"Actual vs Predicted Stock Prices ({company})")
            plt.xlabel("Days")
            plt.ylabel("Stock Price")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()

            plot_name = f"{company}_actual_vs_predicted.png"
            plot_path = os.path.join(PLOTS_DIR, plot_name)
            plt.savefig(plot_path)
            plt.close()

            if os.path.exists(plot_path):
                plot_url = f"http://127.0.0.1:5000/plots/{plot_name}"

        except Exception:
            logging.error("Plot generation failed:\n" + traceback.format_exc())

        # ---------- FORECAST ----------
        last_seq = data_scaled[-SEQ_LENGTH:]
        current = last_seq.reshape(1, SEQ_LENGTH, features)
        forecast = []

        for _ in range(days):
            p = model.predict(current, verbose=0)[0][0]
            forecast.append(p)
            new_row = np.array([[p] + [0] * (features - 1)])
            current = np.append(current[:, 1:, :], new_row.reshape(1, 1, features), axis=1)

        forecast_pad = np.hstack([
            np.array(forecast).reshape(-1, 1),
            np.zeros((days, features - 1))
        ])
        forecast_real = scaler.inverse_transform(forecast_pad)[:, 0]

        return jsonify({
            "company": company,
            "low_likely": float(forecast_real.min()),
            "high_likely": float(forecast_real.max()),
            "forecast": forecast_real.tolist(),
            "plot_url": plot_url
        })

    except Exception:
        logging.error("Predict error:\n" + traceback.format_exc())
        return jsonify({"error": "Prediction failed"}), 500


# ---------- SERVE PLOTS ----------
@app.route("/plots/<filename>")
def serve_plot(filename):
    return send_from_directory(PLOTS_DIR, filename)


# ===================== RUN =====================
if __name__ == "__main__":
    logging.info("Backend running at http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
