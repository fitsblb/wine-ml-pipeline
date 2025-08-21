import yaml
from pathlib import Path
import pandas as pd

def test_target_range_and_duplicates():
    project_root = Path(__file__).resolve().parent.parent
    config_path = project_root / "config" / "config.yaml"
    CFG = yaml.safe_load(open(config_path))
    RAW = project_root / CFG["paths"]["data_raw"]
    sep = CFG.get("io", {}).get("csv_sep", ",")
    df = pd.read_csv(RAW, sep=sep)

    assert df["quality"].between(0, 10).all(), "quality out of expected 0–10 range"
    assert df.duplicated().sum() < len(df) * 0.2, "too many duplicates (>20%)"
