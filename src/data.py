from __future__ import annotations
from pathlib import Path
import hashlib
import pandas as pd

def sha256_of_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def load_metadata(meta_path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(meta_path)
    expected_cols = {"image_id", "dx"}
    missing = expected_cols - set(df.columns)
    if missing:
        raise ValueError(f"Metadados não possuem colunas esperadas: {missing}")
    return df

def class_distribution(df: pd.DataFrame, label_col: str = "dx") -> pd.DataFrame:
    dist = df[label_col].value_counts().rename_axis(label_col).reset_index(name="count")
    dist["pct"] = (dist["count"] / dist["count"].sum()).round(4)
    return dist