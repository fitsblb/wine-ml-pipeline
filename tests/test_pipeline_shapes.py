from pathlib import Path
from datascience.config_manager import load_config, load_schema
from datascience.params_loader import load_params
from datascience.components.data_ingestion import DataIngestion
from datascience.components.data_validation import DataValidation
from datascience.components.data_transformation import DataTransformation

def test_split_and_shapes():
    # Load runtime config/params/schema
    CFG = load_config("config/config.yaml")
    PARAMS = load_params("params.yaml")
    SCHEMA = load_schema(CFG["paths"].get("schema_file", "config/schema.yaml"))

    # Ingestion
    df = DataIngestion(CFG).load()
    assert df.shape[0] > 0 and df.shape[1] > 0

    # Validation
    DataValidation(SCHEMA, CFG).check_required(df)

    # Transformation
    X_train, X_test, y_train, y_test = DataTransformation(PARAMS, CFG).split_and_transform(df)

    # Basic shape checks
    assert len(X_train) > 0 and len(X_test) > 0
    assert len(y_train) == len(X_train) and len(y_test) == len(X_test)
    assert set(X_train.columns) == set(X_test.columns)

    # If scaler is enabled, artifact should exist
    scaler_name = (PARAMS.get("preprocessing", {}) or {}).get("scaler", "none")
    if scaler_name != "none":
        assert (Path(CFG["paths"]["data_processed_dir"]) / "scaler.joblib").exists()
