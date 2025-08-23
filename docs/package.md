
# 📦 datascience — Internal ML Pipeline Package

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

<b>Modular, config-driven ML pipeline for wine quality prediction.</b>

</div>

---

## 🚀 What’s Inside

- **config_manager:**
	- `load_config(path)` — Loads YAML config, resolves all paths to absolute
	- `load_schema(path)` — Loads schema YAML
	- `make_dirs(cfg)` — Creates output directories

- **params_loader:**
	- `load_params(path)` — Loads pipeline parameters

- **components/**
	- `DataIngestion` — Loads CSV data
	- `DataValidation` — Checks required columns/schema
	- `DataTransformation` — Splits, scales, and saves data
	- `ModelTrainer` — Trains model, saves artifacts
	- `ModelEvaluation` — Evaluates model, writes metrics
	- `ModelDiagnostics` — Generates plots and reports

---

## ⚡ Quick Start

```python
from datascience.config_manager import load_config, load_schema
from datascience.params_loader import load_params
from datascience.components.data_ingestion import DataIngestion
from datascience.components.data_validation import DataValidation
from datascience.components.data_transformation import DataTransformation
from datascience.components.model_trainer import ModelTrainer
from datascience.components.model_evaluation import ModelEvaluation

CFG = load_config("config/config.yaml")
SCHEMA = load_schema(CFG["paths"]["schema_file"])
PARAMS = load_params("params.yaml")

df = DataIngestion(CFG).load()
DataValidation(SCHEMA, CFG).check_required(df)
DataTransformation(PARAMS, CFG).split_and_transform(df)
ModelTrainer(PARAMS, CFG).train()
metrics_path = ModelEvaluation(PARAMS, CFG).evaluate()
print(metrics_path)
```

---

## 🛠️ Conventions

- Paths in `config/config.yaml` are relative to the config folder and resolved to absolute by the loader.
- `params.yaml` controls split, scaling, model, and metrics.
- Inference feature order comes from `artifacts/model_trainer/features.json`.

---

## 🧪 Testing

Run all tests:
```bash
pytest -q
```

---

## 📚 More Info

See the main [README](../../README.md) for project overview, API, and deployment details.