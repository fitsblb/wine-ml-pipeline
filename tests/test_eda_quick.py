from pathlib import Path
import pandas as pd
from datascience.config_manager import load_config

def test_target_range_and_duplicates():
    CFG = load_config("config/config.yaml")  # resolves paths to absolute
    RAW = Path(CFG["paths"]["data_raw"])
    sep = CFG.get("io", {}).get("csv_sep", ",")

    assert RAW.exists(), f"raw data file missing at {RAW}"
    df = pd.read_csv(RAW, sep=sep)

    target = CFG["features"]["target"]
    assert df[target].between(0, 10).all(), f"{target} out of expected 0–10 range"
    assert df.duplicated().sum() < len(df) * 0.2, "too many duplicates (>20%)"
