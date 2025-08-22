from pathlib import Path
from datascience.config_manager import load_config
from datascience.params_loader import load_params
from datascience.components.data_ingestion import DataIngestion
from datascience.components.data_validation import DataValidation
from datascience.components.data_transformation import DataTransformation
from datascience.components.model_trainer import ModelTrainer
from datascience.components.model_evaluation import ModelEvaluation
from datascience.components.model_diagnostics import ModelDiagnostics

def test_eval_artifacts_exist():
    CFG = load_config("config/config.yaml")
    PARAMS = load_params("params.yaml")

    # prep + train + eval (idempotent)
    df = DataIngestion(CFG).load()
    DataValidation({"target": CFG["features"]["target"], "required": []}, CFG).check_required(df)
    DataTransformation(PARAMS, CFG).split_and_transform(df)
    ModelTrainer(PARAMS, CFG).train()
    ModelEvaluation(PARAMS, CFG).evaluate()
    paths = ModelDiagnostics(PARAMS, CFG).run()

    # required files
    must = [
        Path(CFG["paths"]["reports_dir"]) / "metrics.json",
        Path(CFG["paths"]["reports_dir"]) / "pred_vs_true.png",
        Path(CFG["paths"]["reports_dir"]) / "residuals_hist.png",
        Path(CFG["paths"]["reports_dir"]) / "report.md",
    ]
    for p in must:
        assert p.exists(), f"missing {p}"
