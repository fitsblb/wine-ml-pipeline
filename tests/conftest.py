# tests/conftest.py
import sys, pathlib, pytest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from datascience.config_manager import load_config
from datascience.params_loader import load_params
from datascience.components.data_ingestion import DataIngestion
from datascience.components.data_validation import DataValidation
from datascience.components.data_transformation import DataTransformation
from datascience.components.model_trainer import ModelTrainer
from datascience.components.model_evaluation import ModelEvaluation

@pytest.fixture(scope="session", autouse=True)
def build_artifacts_once():
    cfg = load_config("config/config.yaml")
    params = load_params("params.yaml")
    df = DataIngestion(cfg).load()
    DataValidation({"target": cfg["features"]["target"], "required": []}, cfg).check_required(df)
    DataTransformation(params, cfg).split_and_transform(df)
    ModelTrainer(params, cfg).train()
    ModelEvaluation(params, cfg).evaluate()
