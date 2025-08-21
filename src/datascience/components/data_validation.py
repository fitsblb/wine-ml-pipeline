class DataValidation:
    def __init__(self, schema: dict, cfg: dict):
        self.target = schema.get("target", cfg["features"]["target"])
        self.required = set(schema.get("required", [])) | {self.target}

    def check_required(self, df):
        missing = self.required - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")
        return True
