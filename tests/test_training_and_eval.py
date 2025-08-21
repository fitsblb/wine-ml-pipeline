from pathlib import Path
import json
from datascience.config_manager import load_config
from datascience.params_loader import load_params
from datascience.components.data_ingestion import DataIngestion
from datascience.components.data_validation import DataValidation
from datascience.components.data_transformation import DataTransformation
from datascience.components.model_trainer import ModelTrainer
from datascience.components.model_evaluation import ModelEvaluation

def test_train_and_evaluate():
    CFG = load_config("config/config.yaml")
    PARAMS = load_params("params.yaml")

    df = DataIngestion(CFG).load()
    DataValidation({"target": CFG["features"]["target"], "required": []}, CFG).check_required(df)
    DataTransformation(PARAMS, CFG).split_and_transform(df)

    ModelTrainer(PARAMS, CFG).train()
    metrics_file = Path(ModelEvaluation(PARAMS, CFG).evaluate())
    assert metrics_file.exists()

    metrics = json.loads(metrics_file.read_text())
    assert "baseline" in metrics and "model" in metrics
    assert metrics["model"]["rmse"] <= metrics["baseline"]["rmse"] + 1e-9
