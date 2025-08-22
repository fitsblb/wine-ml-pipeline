from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS
from datascience.config_manager import load_config

def _load_artifacts(cfg):
    model_dir = Path(cfg["paths"]["model_dir"])
    features = json.loads((model_dir / "features.json").read_text())
    model = joblib.load(model_dir / "model.joblib")

    scaler = None
    scaler_path = Path(cfg["paths"]["data_processed_dir"]) / "scaler.joblib"
    if scaler_path.exists():
        scaler = joblib.load(scaler_path)
    return features, model, scaler

def _validate_and_frame(payload, feature_order):
    # Accept {"data": {...}} or {"data": [{...}, {...}]}
    if not isinstance(payload, dict) or "data" not in payload:
        raise ValueError("Body must be JSON with a 'data' key.")

    data = payload["data"]
    if isinstance(data, dict):
        rows = [data]
    elif isinstance(data, list) and all(isinstance(r, dict) for r in data):
        rows = data
    else:
        raise ValueError("'data' must be an object or a list of objects.")

    # Check keys
    missing = [f for f in feature_order if f not in rows[0]]
    extra = [k for k in rows[0].keys() if k not in feature_order]
    if missing:
        raise ValueError(f"Missing keys: {missing}")
    if extra:
        raise ValueError(f"Unexpected keys: {extra}")

    # Build DataFrame in the right column order
    X = pd.DataFrame(rows, columns=feature_order)

    # Coerce to numeric
    for c in feature_order:
        X[c] = pd.to_numeric(X[c], errors="raise")

    return X

def create_app(config_path: str = "config/config.yaml") -> Flask:
    cfg = load_config(config_path)
    features, model, scaler = _load_artifacts(cfg)

    app = Flask(__name__)
    CORS(app)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "model_dir": cfg["paths"]["model_dir"]})

    @app.post("/predict")
    def predict():
        try:
            payload = request.get_json(force=True, silent=False)
            X = _validate_and_frame(payload, features)
            if scaler is not None:
                X = pd.DataFrame(scaler.transform(X), columns=X.columns, index=X.index)
            preds = model.predict(X)
            return jsonify({"predictions": [float(p) for p in np.ravel(preds)], "n": len(X)})
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=False)
