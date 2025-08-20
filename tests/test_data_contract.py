import pandas as pd 
import yaml
from pathlib import Path
import os

# Testing Data pipeline
def test_data_file_and_columns():
    project_root = Path(__file__).resolve().parent.parent
    config_path = project_root / "config" / "config.yaml"
    CFG = yaml.safe_load(open(config_path))
    RAW = project_root / CFG["paths"]["data_raw"]
    SEP = CFG.get("io", {}).get("csv_sep", ",")
    assert RAW.exists(), "raw data file is missing"

    df = pd.read_csv(RAW, sep=SEP)
    SCHEMA = yaml.safe_load(open(project_root / "schema.yaml"))
    required = set(SCHEMA.get("required", [])) | {SCHEMA.get("target", "quality")}
    assert required.issubset(df.columns), f"missing columns: {sorted(required - set(df.columns))}"
