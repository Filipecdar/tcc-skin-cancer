# Definition of Done – Semana 1 (Setup)

- [ ] **Repositório criado** com estrutura: `data/`, `notebooks/`, `src/`, `outputs/figures/`, `outputs/models/`, `reports/`, `scripts/`, `app/`.
- [ ] **Ambiente replicável** (conda/venv) funcionando; `notebooks/00_check_environment.ipynb` roda sem erro.
- [ ] **Dataset baixado e verificado**: contagem = 10.015 imagens e `HAM10000_metadata.csv` presente.
- [ ] **Script de verificação** rodou e gerou: `reports/ham10000_summary.json`, `reports/ham10000_manifest.csv`, `reports/ham10000_hashes.txt`.
- [ ] **Padrão de figuras** aplicado via `src/viz.py` (PNG 300 DPI, fonte legível).
- [ ] **Protótipo Streamlit** abre (`streamlit run app/app.py`) com placeholder do pipeline.
- [ ] **Decisão de dataset** registrada em `reports/dataset_decision.md` e anotada no documento do TCC.

> Critério de aceite: qualquer pessoa que clone o repo e siga o HOWTO_6passos deve conseguir reproduzir o ambiente e validar o dataset sem erros.