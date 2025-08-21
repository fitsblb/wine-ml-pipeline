from pathlib import Path
import pandas as pd, joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler

class DataTransformation:
    def __init__(self, params: dict, cfg: dict):
        self.params = params
        self.cfg = cfg
        self.outdir = Path(cfg["paths"]["data_processed_dir"])
        self.outdir.mkdir(parents=True, exist_ok=True)
        self.target = cfg["features"]["target"]

    def _scaler(self):
        name = (self.params.get("preprocessing", {}) or {}).get("scaler", "none")
        return {"standard": StandardScaler, "minmax": MinMaxScaler}.get(name, lambda: None)()

    def split_and_transform(self, df: pd.DataFrame):
        X = df.drop(columns=[self.target])
        y = df[self.target]

        Xtr, Xte, ytr, yte = train_test_split(
            X, y,
            test_size=self.params["split"]["test_size"],
            shuffle=self.params["split"]["shuffle"],
            random_state=self.params["seed"],
        )

        scaler = self._scaler()
        if scaler is not None:
            Xtr = pd.DataFrame(scaler.fit_transform(Xtr), columns=X.columns, index=Xtr.index)
            Xte = pd.DataFrame(scaler.transform(Xte), columns=X.columns, index=Xte.index)
            joblib.dump(scaler, self.outdir / "scaler.joblib")

        Xtr.to_csv(self.outdir / "X_train.csv", index=False)
        Xte.to_csv(self.outdir / "X_test.csv", index=False)
        ytr.to_csv(self.outdir / "y_train.csv", index=False)
        yte.to_csv(self.outdir / "y_test.csv", index=False)
        return Xtr, Xte, ytr, yte
