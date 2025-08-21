from datascience.config_manager import load_config, load_schema, make_dirs
from datascience.params_loader import load_params
from datascience.components.data_ingestion import DataIngestion
from datascience.components.data_validation import DataValidation
from datascience.components.data_transformation import DataTransformation

CFG = load_config("config/config.yaml")
SCHEMA = load_schema(CFG["paths"].get("schema_file", "schema.yaml"))
PARAMS = load_params("params.yaml")

make_dirs(CFG)

df = DataIngestion(CFG).load()
DataValidation(SCHEMA, CFG).check_required(df)
DataTransformation(PARAMS, CFG).split_and_transform(df)
print("Data pipeline complete.")
