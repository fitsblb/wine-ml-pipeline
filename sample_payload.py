import pandas as pd, json 
from datascience.config_manager import load_config 

CFG = load_config("config/config.yaml") 
df = pd.read_csv(CFG["paths"]["data_raw"], sep=CFG.get("io", {}).get("csv_sep", ";")) 
sample = df.drop(columns=[CFG["features"]["target"]]).iloc[0].to_dict() 
print(json.dumps({"data": sample}))