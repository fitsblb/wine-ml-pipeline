from pathlib import Path
import json, math, joblib, pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

class ModelEvaluation:
    def __init__(self, params: dict, cfg: dict):
        self.params = params
        self.cfg = cfg
        self.proc = Path(cfg["paths"]["data_processed_dir"])
        self.model_dir = Path(cfg["paths"]["model_dir"])
        self.reports = Path(cfg["paths"]["reports_dir"])
        self.reports.mkdir(parents=True, exist_ok=True)

    def _metrics(self, y_true, y_pred):
        return {
            "rmse": math.sqrt(mean_squared_error(y_true, y_pred)),
            "mae": mean_absolute_error(y_true, y_pred),
            "r2": r2_score(y_true, y_pred),
        }

    def evaluate(self) -> str:
        Xte = pd.read_csv(self.proc / "X_test.csv")
        yte = pd.read_csv(self.proc / "y_test.csv").squeeze("columns")
        ytr = pd.read_csv(self.proc / "y_train.csv").squeeze("columns")

        baseline_pred = [float(ytr.mean())] * len(yte)
        baseline = self._metrics(yte, baseline_pred)

        model = joblib.load(self.model_dir / "model.joblib")
        yhat = model.predict(Xte)
        model_m = self._metrics(yte, yhat)

        out = {"target": self.cfg["features"]["target"], "baseline": baseline, "model": model_m}
        path = self.reports / "metrics.json"
        path.write_text(json.dumps(out, indent=2))
        return str(path)
