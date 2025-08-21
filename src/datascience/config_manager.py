from pathlib import Path
import yaml, os

def _abs(base: Path, p: str | Path) -> str:
    p = Path(p)
    return str(p if p.is_absolute() else (base / p).resolve())

def load_config(config_path: str | Path = "config/config.yaml") -> dict:
    cp = Path(config_path)
    if not cp.is_absolute():
        cp = (Path.cwd() / cp).resolve()
    cfg = yaml.safe_load(open(cp, "r"))
    base = cp.parent
    # normalize relative paths to absolute
    if "paths" in cfg:
        cfg["paths"] = {k: _abs(base, v) for k, v in cfg["paths"].items()}
    cfg["_config_path"] = str(cp)
    return cfg

def load_schema(schema_path: str | Path = "schema.yaml") -> dict:
    sp = Path(schema_path)
    if not sp.is_absolute():
        sp = (Path.cwd() / sp).resolve()
    return yaml.safe_load(open(sp, "r"))

def make_dirs(cfg: dict, keys=("data_processed_dir","model_dir","reports_dir")) -> None:
    for k in keys:
        p = Path(cfg["paths"].get(k, ""))
        if p:
            p.mkdir(parents=True, exist_ok=True)
