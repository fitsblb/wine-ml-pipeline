from pathlib import Path
import json, math
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class ModelDiagnostics:
    def __init__(self, params: dict, cfg: dict):
        self.params = params
        self.cfg = cfg
        self.proc = Path(cfg["paths"]["data_processed_dir"])
        self.model_dir = Path(cfg["paths"]["model_dir"])
        self.reports = Path(cfg["paths"]["reports_dir"])
        self.reports.mkdir(parents=True, exist_ok=True)

    def _save_residuals_hist(self, residuals: np.ndarray, path: Path):
        plt.figure(figsize=(5,3))
        plt.hist(residuals, bins=30)
        plt.title("Residuals (y_true - y_pred)")
        plt.xlabel("residual"); plt.ylabel("count")
        plt.tight_layout(); plt.savefig(path, dpi=150, bbox_inches="tight"); plt.close()

    def _save_pred_vs_true(self, y_true: np.ndarray, y_pred: np.ndarray, path: Path):
        lo = float(min(y_true.min(), y_pred.min()))
        hi = float(max(y_true.max(), y_pred.max()))
        plt.figure(figsize=(5,5))
        plt.scatter(y_true, y_pred, s=8, alpha=0.6)
        plt.plot([lo, hi], [lo, hi])  # y=x
        plt.xlabel("y_true"); plt.ylabel("y_pred")
        plt.title("Predicted vs True")
        plt.tight_layout(); plt.savefig(path, dpi=150, bbox_inches="tight"); plt.close()

    def _save_error_by_target(self, y_true: np.ndarray, y_pred: np.ndarray, path: Path):
        df = pd.DataFrame({"y": y_true, "pred": y_pred})
        # bin by target; 6 equal-width bins by range
        bins = np.linspace(df["y"].min(), df["y"].max(), 7)
        df["bin"] = pd.cut(df["y"], bins, include_lowest=True)
        err = (
                        df.assign(abs_err=lambda x: (x["y"] - x["pred"]).abs())
                        .groupby("bin", observed=True)["abs_err"]   # was: .groupby("bin")["abs_err"]
                        .mean()
                    )

       
        plt.figure(figsize=(6,3))
        err.plot(kind="bar")
        plt.ylabel("mean |error|"); plt.title("Error by target bin")
        plt.tight_layout(); plt.savefig(path, dpi=150, bbox_inches="tight"); plt.close()

    def _save_feature_importance(self, model, feature_names: list[str]) -> tuple[str, str] | tuple[None, None]:
        imp_json = self.reports / "feature_importance.json"
        imp_png  = self.reports / "feature_importance.png"

        if hasattr(model, "feature_importances_"):
            vals = model.feature_importances_
            series = pd.Series(vals, index=feature_names).sort_values(ascending=False).head(10)
            imp_json.write_text(json.dumps(series.to_dict(), indent=2))
            plt.figure(figsize=(6,3))
            series[::-1].plot(kind="barh")  # small to large for nicer labels
            plt.title("Top feature importance")
            plt.tight_layout(); plt.savefig(imp_png, dpi=150, bbox_inches="tight"); plt.close()
            return str(imp_json), str(imp_png)

        if hasattr(model, "coef_"):
            vals = np.ravel(model.coef_)
            series = pd.Series(vals, index=feature_names).sort_values(key=lambda s: s.abs(), ascending=False).head(10)
            imp_json.write_text(json.dumps(series.to_dict(), indent=2))
            plt.figure(figsize=(6,3))
            series[::-1].plot(kind="barh")
            plt.title("Top coefficients (abs)")
            plt.tight_layout(); plt.savefig(imp_png, dpi=150, bbox_inches="tight"); plt.close()
            return str(imp_json), str(imp_png)

        return None, None

    def run(self) -> list[str]:
        Xte = pd.read_csv(self.proc / "X_test.csv")
        yte = pd.read_csv(self.proc / "y_test.csv").squeeze("columns")
        model = joblib.load(self.model_dir / "model.joblib")

        yhat = model.predict(Xte)
        residuals = yte.values - yhat

        # plots
        paths = []
        p1 = self.reports / "residuals_hist.png"; self._save_residuals_hist(residuals, p1); paths.append(str(p1))
        p2 = self.reports / "pred_vs_true.png";   self._save_pred_vs_true(yte.values, yhat, p2); paths.append(str(p2))
        p3 = self.reports / "error_by_target.png"; self._save_error_by_target(yte.values, yhat, p3); paths.append(str(p3))

        # feature importance / coefficients
        feats_path = self.model_dir / "features.json"
        feat_names = json.loads(feats_path.read_text()) if feats_path.exists() else list(Xte.columns)
        imp_json, imp_png = self._save_feature_importance(model, feat_names)
        if imp_json: paths.extend([imp_json, imp_png])

        # summary report
        metrics_path = Path(self.cfg["paths"]["reports_dir"]) / "metrics.json"
        metrics = json.loads(metrics_path.read_text()) if metrics_path.exists() else {}
        report = self.reports / "report.md"
        report.write_text(
            f"# Evaluation Report\n"
            f"- rows test: {len(yte)}\n"
            f"- baseline: {metrics.get('baseline', {})}\n"
            f"- model: {metrics.get('model', {})}\n"
            f"- artifacts: {[Path(p).name for p in paths]}\n"
        )
        paths.append(str(report))
        return paths
