# --- garantir import do pacote src ---
import os, sys
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
for p in (PROJECT_ROOT, SRC_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)
# -------------------------------------

# opcional: silenciar logs do TF
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from data.pipeline import load_and_preprocess, make_augmenter

RAW_DIR = Path("data/raw")
OUT = Path("outputs/figures/augmentation_demo.png")
OUT.parent.mkdir(parents=True, exist_ok=True)

def find_jpgs(n=6):
    imgs = sorted(RAW_DIR.glob("**/*.jpg"))
    if len(imgs) < n:
        raise FileNotFoundError(f"Encontrei apenas {len(imgs)} JPG(s) em {RAW_DIR}/**/*.jpg")
    return imgs[:n]

def to_img_np(x):
    x = tf.convert_to_tensor(x)
    if x.dtype.is_integer:
        x = tf.cast(x, tf.float32) / 255.0
    x = tf.clip_by_value(x, 0.0, 1.0)
    return x.numpy()

def main():
    paths = find_jpgs(6)
    aug = make_augmenter()

    originals = [load_and_preprocess(p) for p in paths]
    auged = [aug(x) for x in originals]

    n = len(originals)
    fig, axes = plt.subplots(2, n, figsize=(n*2.6, 5.2))

    for i in range(n):
        axes[0, i].imshow(to_img_np(originals[i])); axes[0, i].set_title("original"); axes[0, i].axis("off")
        axes[1, i].imshow(to_img_np(auged[i]));     axes[1, i].set_title("augment");  axes[1, i].axis("off")

    plt.tight_layout()
    plt.savefig(OUT, dpi=300)
    plt.close(fig)
    print(f"OK: {OUT}")

if __name__ == "__main__":
    main()
