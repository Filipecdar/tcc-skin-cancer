# Padrão de Figuras — Dia 1 (Step 6)

**Objetivo:** garantir consistência visual e reprodutibilidade das figuras usadas no TCC.

## Especificações
- **Formato do arquivo:** PNG
- **DPI (arquivo salvo):** 300
- **Fonte:** sans-serif (padrão do Matplotlib) com tamanho base **12 pt**
- **Títulos e rótulos:**
  - Título do gráfico: 13 pt
  - Rótulos de eixos: 12 pt
  - Ticks: 11 pt
- **Tamanho de figura (padrões):**
  - `S` (report): **5.5 x 3.5 in** (ideal para 1 coluna)
  - `M` (report): **7.0 x 4.5 in**
  - `L` (slides): **9.0 x 5.5 in**
- **Layout:** `tight_layout()` para evitar cortes de labels
- **Fundo:** branco (default)
- **Grade:** opcional, linhas leves (usar `ax.grid(True, alpha=0.2)` quando fizer sentido)
- **Nomeação de arquivos:**
  - `outputs/figures/<capitulo>_<tema>_<detalhe>.png`
  - Ex.: `outputs/figures/dados_ham10000_class_dist.png`

## Como aplicar
1. Use o módulo `src/viz.py`:
   - `viz.configure()` para aplicar o estilo base nas `rcParams`;
   - `viz.fig_ax(size="M")` para criar figura com tamanho padrão;
   - `viz.save_fig(fig, "outputs/figures/...", dpi=300)` para salvar com DPI correto.
2. Em notebooks, sempre chame `viz.configure()` no topo.

## Checklist de Qualidade (QA)
- [ ] Tamanho de fonte ≥ 11 pt em ticks e ≥ 12 pt em labels
- [ ] Legendas e rótulos não cortados (usar `tight_layout()`)
- [ ] PNG salvo em 300 DPI
- [ ] Eixos/grades legíveis, sem poluição visual
- [ ] Nome do arquivo informativo
