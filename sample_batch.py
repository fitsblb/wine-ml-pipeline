import json, pandas as pd
from datascience.config_manager import load_config
CFG = load_config("config/config.yaml")
df = pd.read_csv(CFG["paths"]["data_raw"], sep=CFG.get("io",{}).get("csv_sep",";"))
X = df.drop(columns=[CFG["features"]["target"]]).head(3).to_dict(orient="records")
print(json.dumps({"data": X}))
