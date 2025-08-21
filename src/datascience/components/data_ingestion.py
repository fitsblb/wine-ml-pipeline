from pathlib import Path
import pandas as pd

class DataIngestion:
    def __init__(self, cfg: dict):
        self.raw = Path(cfg["paths"]["data_raw"])
        self.sep = cfg.get("io", {}).get("csv_sep", ",")

    def load(self) -> pd.DataFrame:
        assert self.raw.exists(), f"Missing file: {self.raw}"
        return pd.read_csv(self.raw, sep=self.sep)
