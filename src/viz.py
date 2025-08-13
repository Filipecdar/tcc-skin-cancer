from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt

# Estilo base para figuras científicas (padrão Dia 1)
plt.rcParams.update({
    "figure.dpi": 100,          # DPI de tela (o save_fig usa 300 DPI no arquivo)
    "savefig.dpi": 300,         # garante 300 DPI no arquivo
    "figure.autolayout": True,
    "font.size": 12,
    "font.family": "sans-serif",
    "axes.titlesize": 13,
    "axes.labelsize": 12,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
})

def save_fig(fig: plt.Figure, path: str | Path, tight: bool = True):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if tight:
        fig.tight_layout()
    fig.savefig(path, format="png", dpi=300)