# --- garantir import do pacote src ---
import os, sys, time
from pathlib import Path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
# -------------------------------------

import pandas as pd
from glob import glob

RAW = Path("data/raw")
SPLITS_DIR = Path("data/splits"); SPLITS_DIR.mkdir(parents=True, exist_ok=True)

def find_metadata_path():
    candidates = glob(str(RAW / "**" / "*HAM10000_metadata*"), recursive=True)
    if not candidates:
        raise FileNotFoundError("Não encontrei 'HAM10000_metadata' em data/raw/.")
    candidates = sorted(candidates, key=lambda p: (not p.lower().endswith(".csv"), p))
    return candidates[0]

def read_metadata(meta_path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(meta_path)
    except Exception:
        return pd.read_csv(meta_path, sep=",", engine="python")

def build_image_index() -> dict:
    """Faz UMA varredura e cria um dicionário {image_id: caminho}."""
    t0 = time.time()
    jpgs = list(RAW.rglob("*.jpg"))
    index = {}
    for p in jpgs:
        stem = p.stem  # nome do arquivo sem extensão
        # mantém a 1ª ocorrência (HAM10000 não tem duplicados de stem)
        if stem not in index:
            index[stem] = str(p)
    print(f"[index] {len(jpgs)} arquivos .jpg varridos; {len(index)} indexados em {time.time()-t0:.2f}s")
    return index

def main(test_size=0.2, random_state=42):
    from sklearn.model_selection import StratifiedShuffleSplit

    print("[info] procurando metadados…")
    meta_path = find_metadata_path()
    print(f"[info] usando: {meta_path}")

    print("[info] lendo CSV…")
    df = read_metadata(meta_path)

    needed = {"image_id", "dx"}
    if not needed.issubset(set(df.columns)):
        raise ValueError(f"Metadados precisam conter {needed}. Colunas atuais: {df.columns.tolist()}")

    print("[info] indexando imagens (.jpg)…")
    idx = build_image_index()

    print("[info] mapeando image_id -> path…")
    df["image_id"] = df["image_id"].astype(str)
    df["path"] = df["image_id"].map(idx)

    missing = int(df["path"].isna().sum())
    if missing:
        print(f"[warn] {missing} imagens dos metadados não foram encontradas no disco (serão descartadas).")

    df = df.dropna(subset=["path"]).reset_index(drop=True)

    # bloqueio por lesão (se existir)
    group_col = "lesion_id" if "lesion_id" in df.columns else None
    print(f"[info] coluna de bloqueio por lesão: {group_col if group_col else 'não disponível'}")

    if group_col:
        g = (df.groupby(group_col)
               .agg(dx=("dx", "first"), n=("dx", "size"))
               .reset_index())
        Xg, yg = g[group_col].values, g["dx"].values
        sss = StratifiedShuffleSplit(n_splits=1, test_size=test_size, random_state=random_state)
        train_idx, val_idx = next(sss.split(Xg, yg))
        train_groups = set(Xg[train_idx]); val_groups = set(Xg[val_idx])
        df_train = df[df[group_col].isin(train_groups)].copy()
        df_val   = df[df[group_col].isin(val_groups)].copy()
    else:
        X, y = df["image_id"].values, df["dx"].values
        sss = StratifiedShuffleSplit(n_splits=1, test_size=test_size, random_state=random_state)
        train_idx, val_idx = next(sss.split(X, y))
        df_train = df.iloc[train_idx].copy()
        df_val   = df.iloc[val_idx].copy()

    # ordena e salva
    cols = ["image_id", "dx", "path"] + ([group_col] if group_col else [])
    df_train = df_train[cols].sort_values(["dx", "image_id"]).reset_index(drop=True)
    df_val   = df_val[cols].sort_values(["dx", "image_id"]).reset_index(drop=True)

    df_train.to_csv(SPLITS_DIR / "train.csv", index=False)
    df_val.to_csv(SPLITS_DIR / "val.csv", index=False)

    def summarize(d):
        return d.groupby("dx")["image_id"].count().sort_values(ascending=False)

    print("Arquivos salvos:")
    print(" -", SPLITS_DIR / "train.csv")
    print(" -", SPLITS_DIR / "val.csv")
    print("\nDistribuição (train):\n", summarize(df_train))
    print("\nDistribuição (val):\n", summarize(df_val))

if __name__ == "__main__":
    main()
