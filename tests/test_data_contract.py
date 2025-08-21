import yaml
from pathlib import Path
import pandas as pd

def test_data_file_and_columns():
    CFG = yaml.safe_load(open("config/config.yaml"))
    RAW = Path(CFG["paths"]["data_raw"])
    SEP = CFG.get("io", {}).get("csv_sep", ",")
    assert RAW.exists(), "raw data file missing"

    df = pd.read_csv(RAW, sep=SEP)

    schema_path = Path(CFG["paths"]["schema_file"])  # <- use config path
    SCHEMA = yaml.safe_load(open(schema_path))
    required = set(SCHEMA.get("required", [])) | {SCHEMA.get("target", "quality")}
    assert required.issubset(df.columns), f"missing columns: {sorted(required - set(df.columns))}"
