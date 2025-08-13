from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt

_DEFAULT_SIZES_IN = {
    "S": (5.5, 3.5),
    "M": (7.0, 4.5),
    "L": (9.0, 5.5),
}

def configure():
    """Aplica o estilo base para o TCC (padrão de figuras)."""
    plt.rcParams.update({
        "figure.dpi": 100,          # DPI de exibição
        "savefig.dpi": 300,         # garante 300 DPI no arquivo
        "figure.autolayout": True,  # evita cortes
        "font.size": 12,
        "font.family": "sans-serif",
        "axes.titlesize": 13,
        "axes.labelsize": 12,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
    })

def fig_ax(size: str = "M", **kwargs):
    """Cria figura e eixo no tamanho padrão especificado (S, M, L)."""
    if size not in _DEFAULT_SIZES_IN:
        raise ValueError(f"Tamanho inválido: {size}. Opções: {list(_DEFAULT_SIZES_IN.keys())}")
    w, h = _DEFAULT_SIZES_IN[size]
    fig, ax = plt.subplots(figsize=(w, h), **kwargs)
    return fig, ax

def save_fig(fig, path, tight=True, dpi=300):
    from pathlib import Path
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if tight:
        fig.tight_layout()
    # Garante aparência consistente (sem transparência)
    fig.savefig(path, format="png", dpi=dpi, facecolor="white", transparent=False)

# Helpers opcionais
def beautify_axes(ax, grid: bool = True):
    """Aplica pequenos ajustes de visual no eixo."""
    if grid:
        ax.grid(True, alpha=0.2)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    return ax
