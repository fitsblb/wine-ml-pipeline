import json
import pandas as pd
from datascience.config_manager import load_config
from app import create_app

def test_health_ok():
    app = create_app()
    app.testing = True
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"

def test_predict_one_row():
    cfg = load_config("config/config.yaml")
    raw = cfg["paths"]["data_raw"]
    sep = cfg.get("io", {}).get("csv_sep", ",")

    df = pd.read_csv(raw, sep=sep)
    target = cfg["features"]["target"]
    sample = df.drop(columns=[target]).iloc[0].to_dict()

    app = create_app()
    app.testing = True
    client = app.test_client()

    resp = client.post(
        "/predict",
        data=json.dumps({"data": sample}),
        content_type="application/json"
    )
    assert resp.status_code == 200, resp.get_json()
    body = resp.get_json()
    assert "predictions" in body and isinstance(body["predictions"], list)
    assert len(body["predictions"]) == 1
    assert isinstance(body["predictions"][0], float)
