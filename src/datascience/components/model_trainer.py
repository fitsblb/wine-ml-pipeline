from pathlib import Path
import json, joblib, pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

class ModelTrainer:
    def __init__(self, params: dict, cfg: dict):
        self.params = params
        self.cfg = cfg
        self.proc = Path(cfg["paths"]["data_processed_dir"])
        self.out = Path(cfg["paths"]["model_dir"])
        self.out.mkdir(parents=True, exist_ok=True)

    def _build_model(self):
        m = self.params.get("model", {})
        mtype = (m.get("type") or "random_forest").lower()
        if mtype == "linear":
            return LinearRegression()
        return RandomForestRegressor(
            n_estimators=m.get("n_estimators", 200),
            max_depth=m.get("max_depth", None),
            random_state=self.params.get("seed", 42),
            n_jobs=m.get("n_jobs", -1),
        )

    def train(self) -> str:
        Xtr = pd.read_csv(self.proc / "X_train.csv")
        ytr = pd.read_csv(self.proc / "y_train.csv").squeeze("columns")
        if isinstance(ytr, pd.DataFrame):
             ytr = ytr.iloc[:, 0]
        ytr = pd.to_numeric(ytr, errors="coerce")
        model = self._build_model()
        model.fit(Xtr, ytr)
        (self.out / "features.json").write_text(json.dumps(list(Xtr.columns)))
        path = self.out / "model.joblib"
        joblib.dump(model, path)
        return str(path)
