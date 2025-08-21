from pathlib import Path
import pandas as pd
from datascience.config_manager import load_config, load_schema

def test_data_file_and_columns():
    CFG = load_config("config/config.yaml")                 # normalizes paths -> absolute
    RAW = Path(CFG["paths"]["data_raw"])
    SEP = CFG.get("io", {}).get("csv_sep", ",")

    assert RAW.exists(), f"raw data file missing at {RAW}"
    df = pd.read_csv(RAW, sep=SEP)

    SCHEMA = load_schema(CFG["paths"]["schema_file"])       # absolute or normalized
    required = set(SCHEMA.get("required", [])) | {SCHEMA.get("target", "quality")}
    missing = required - set(df.columns)
    assert not missing, f"missing columns: {sorted(missing)}"
