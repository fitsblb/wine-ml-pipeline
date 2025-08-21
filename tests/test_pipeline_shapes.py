import yaml, pandas as pd
from pathlib import Path
from datascience.components.data_ingestion import DataIngestion
from datascience.components.data_validation import DataValidation
from datascience.components.data_transformation import DataTransformation

def test_split_and_shapes():
    df = DataIngestion().load()
    DataValidation().check_required(df)
    X_train, X_test, y_train, y_test = DataTransformation().split_and_transform(df)

    assert len(X_train) > 0 and len(X_test) > 0
    assert len(y_train) == len(X_train) and len(y_test) == len(X_test)
    assert set(X_train.columns) == set(X_test.columns)
