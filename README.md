# TCC – Aplicação de Deep Learning na Detecção de Cânceres de Pele (Dia 1)

Este repositório foi inicializado para o **Dia 1 – Alinhar escopo + setup reprodutível**.

## Estrutura
```
data/
  raw/                # Coloque aqui os dados brutos (ex.: HAM10000 *.jpg e CSV)
notebooks/            # Notebooks Jupyter
src/                  # Código Python (data loading, utils, viz)
scripts/              # Scripts de download/validação
outputs/
  figures/            # Figuras (padrão: PNG, 300 DPI)
  models/             # Modelos treinados
reports/              # Decisões, DoD, anotações
app/                  # Protótipo Streamlit
```

## Ambiente
Escolha **conda** ou **venv**:

### Conda
```bash
conda env create -f environment.yml
conda activate tcc-skin
python -m ipykernel install --user --name tcc-skin --display-name "tcc-skin"
```

### venv (pip)
```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m ipykernel install --user --name tcc-skin --display-name "tcc-skin"
```

## Dados (HAM10000)
1) **Baixe** as imagens e o `HAM10000_metadata.csv` (ver `reports/dataset_decision.md`).
2) **Coloque** tudo em `data/raw/HAM10000/` (pasta criada por você).
3) **Valide**:
```bash
python scripts/verify_ham10000.py --root data/raw/HAM10000 --out reports
```

## Padrão de figuras
- Formato: **PNG**
- DPI ao salvar: **300**
- Fonte base: **sans-serif**, tamanho 12+ (controlado em `src/viz.py`)
- Use `viz.save_fig(fig, "outputs/figures/minha_fig.png")`

## Protótipo Streamlit
```bash
streamlit run app/app.py
```

---

Veja `reports/week1_DoD.md` para a Definition of Done da semana.