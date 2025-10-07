import os
import json
import pickle
import numpy as np
import tensorflow as tf
from sklearn.metrics import mean_squared_error
from math import sqrt

# Always resolve relative to backend/
BASE_DIR = os.path.dirname(__file__)

models = {
    "HDFC": os.path.join(BASE_DIR, "models/hdfc_model.h5"),
    "Honda": os.path.join(BASE_DIR, "models/honda_model.h5"),
    "Sony": os.path.join(BASE_DIR, "models/sony_model.h5"),
    "Nintendo": os.path.join(BASE_DIR, "models/nintendo_model.h5"),
    "Alibaba": os.path.join(BASE_DIR, "models/alibaba_model.h5"),
    "Reliance": os.path.join(BASE_DIR, "models/stock_price_model.h5"),
    "Adani": os.path.join(BASE_DIR, "models/adani_model.h5"),
    "TCS": os.path.join(BASE_DIR, "models/tcs_model.h5"),
    "Xiaomi": os.path.join(BASE_DIR, "models/xiaomi_model.h5"),
    "Tencent": os.path.join(BASE_DIR, "models/tencent_stock_price_model.h5"),
    "JD.com Inc": os.path.join(BASE_DIR, "models/jdhk_model.h5"),
    "Toyota": os.path.join(BASE_DIR, "models/toyota_stock_price_model.h5"),
}

scalers = {
    "HDFC": os.path.join(BASE_DIR, "scalers/hdfc_scaler.pkl"),
    "Honda": os.path.join(BASE_DIR, "scalers/honda_scaler.pkl"),
    "Sony": os.path.join(BASE_DIR, "scalers/sony_scaler.pkl"),
    "Nintendo": os.path.join(BASE_DIR, "scalers/nintendo_scaler.pkl"),
    "Alibaba": os.path.join(BASE_DIR, "scalers/alibaba_scaler.pkl"),
    "Reliance": os.path.join(BASE_DIR, "scalers/nse_scaler.pkl"),
    "Adani": os.path.join(BASE_DIR, "scalers/adani_scaler.pkl"),
    "TCS": os.path.join(BASE_DIR, "scalers/tcs_scaler.pkl"),
    "Xiaomi": os.path.join(BASE_DIR, "scalers/xiaomi_scaler.pkl"),
    "Tencent": os.path.join(BASE_DIR, "scalers/tencent_scaler.pkl"),
    "JD.com Inc": os.path.join(BASE_DIR, "scalers/jdhk_scaler.pkl"),
    "Toyota": os.path.join(BASE_DIR, "scalers/toyota_scaler.pkl"),
}

datasets = {
    "HDFC": os.path.join(BASE_DIR, "scaled_data/hdfc_scaled_data.pkl"),
    "Honda": os.path.join(BASE_DIR, "scaled_data/honda_scaled_data.pkl"),
    "Sony": os.path.join(BASE_DIR, "scaled_data/sony_scaled_data.pkl"),
    "Nintendo": os.path.join(BASE_DIR, "scaled_data/nintendo_scaled_data.pkl"),
    "Alibaba": os.path.join(BASE_DIR, "scaled_data/alibaba_scaled_data.pkl"),
    "Reliance": os.path.join(BASE_DIR, "scaled_data/nse_scaled_data.pkl"),
    "Adani": os.path.join(BASE_DIR, "scaled_data/adani_scaled_data.pkl"),
    "TCS": os.path.join(BASE_DIR, "scaled_data/tcs_scaled_data.pkl"),
    "Xiaomi": os.path.join(BASE_DIR, "scaled_data/xiaomi_scaled_data.pkl"),
    "Tencent": os.path.join(BASE_DIR, "scaled_data/tencent_scaled_data.pkl"),
    "JD.com Inc": os.path.join(BASE_DIR, "scaled_data/jdhk_scaled_data.pkl"),
    "Toyota": os.path.join(BASE_DIR, "scaled_data/toyota_scaled_data.pkl"),
}

results = {}

for name, model_path in models.items():
    print(f"Computing RMSE for {name}...")

    if not os.path.exists(model_path):
        print(f" Model file not found: {model_path}")
        continue

    model = tf.keras.models.load_model(model_path, compile=False)
    scaler = pickle.load(open(scalers[name], "rb"))
    data = pickle.load(open(datasets[name], "rb"))

    seq_length = 60
    X, y = [], []
    for i in range(seq_length, len(data)):
        X.append(data[i - seq_length:i])
        y.append(data[i, 0])
    X, y = np.array(X), np.array(y)

    preds = model.predict(X, verbose=0)
    preds_rescaled = scaler.inverse_transform(
        np.concatenate((preds, np.zeros((preds.shape[0], 3))), axis=1)
    )[:, 0]
    y_rescaled = scaler.inverse_transform(
        np.concatenate((y.reshape(-1, 1), np.zeros((len(y), 3))), axis=1)
    )[:, 0]

    rmse = sqrt(mean_squared_error(y_rescaled, preds_rescaled))
    results[name] = rmse

# Save metrics inside backend/
metrics_file = os.path.join(BASE_DIR, "metrics.json")
with open(metrics_file, "w") as f:
    json.dump(results, f, indent=2)

print(f" Metrics updated in {metrics_file}")
