#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, csv
from pathlib import Path
from hashlib import sha256
import pandas as pd

def hash_file(path: Path) -> str:
    h = sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True, help="Pasta com imagens e HAM10000_metadata.csv")
    ap.add_argument("--out", type=Path, default=Path("reports"), help="Pasta de saída para relatórios")
    args = ap.parse_args()

    root = args.root
    out = args.out
    out.mkdir(parents=True, exist_ok=True)

    # Arquivos esperados
    meta_candidates = list(root.glob("**/HAM10000_metadata.csv"))
    if not meta_candidates:
        raise FileNotFoundError("HAM10000_metadata.csv não encontrado sob a pasta raiz fornecida.")
    meta_path = meta_candidates[0]

    # Carregar metadados
    df = pd.read_csv(meta_path)
    if "image_id" not in df.columns or "dx" not in df.columns:
        raise ValueError("Metadados não possuem colunas esperadas 'image_id' e 'dx'.")

    # Contagem de imagens .jpg
    jpgs = sorted([p for p in root.rglob("*.jpg")])
    n_jpg = len(jpgs)

    # Checar interseção metadata vs arquivos
    image_ids = set(df["image_id"].astype(str))
    jpg_ids = set([p.stem for p in jpgs])
    missing_files = sorted(list(image_ids - jpg_ids))
    extra_files = sorted(list(jpg_ids - image_ids))

    # Hash do CSV e manifest de amostra (ou completo, se desejar)
    csv_hash = hash_file(meta_path)
    manifest_path = out / "ham10000_manifest.csv"
    with open(manifest_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["image_id", "exists"])
        for iid in sorted(image_ids):
            w.writerow([iid, iid in jpg_ids])

    # Distribuição de classes
    dist = df["dx"].value_counts().rename_axis("dx").reset_index(name="count")
    dist["pct"] = (dist["count"] / dist["count"].sum()).round(4)
    dist.to_csv(out / "ham10000_class_dist.csv", index=False)

    # Resumo JSON
    summary = {
        "num_images_metadata": int(len(df)),
        "num_images_found": int(n_jpg),
        "csv_sha256": csv_hash,
        "missing_files_count": len(missing_files),
        "extra_files_count": len(extra_files),
        "expected_min_images": 10000,  # sanity
    }
    (out / "ham10000_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Hashes do CSV e lista de faltantes
    (out / "ham10000_hashes.txt").write_text(f"HAM10000_metadata.csv sha256: {csv_hash}\n", encoding="utf-8")
    if missing_files:
        (out / "ham10000_missing.txt").write_text("\n".join(missing_files), encoding="utf-8")
    if extra_files:
        (out / "ham10000_extra.txt").write_text("\n".join(extra_files), encoding="utf-8")

    print("OK! Relatórios em:", out)

if __name__ == "__main__":
    main()