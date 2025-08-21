from pathlib import Path
import yaml

def load_params(path: str | Path = "params.yaml") -> dict:
    p = Path(path)
    if not p.is_absolute():
        p = (Path.cwd() / p).resolve()
    return yaml.safe_load(open(p, "r"))
