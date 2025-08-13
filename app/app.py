import streamlit as st

st.title("Dermato AI – Protótipo (Dia 1)")
st.write("Setup ok. Este app será usado para demo do classificador e Grad-CAM nas próximas etapas.")
st.info("Coloque o dataset em data/raw/HAM10000 e rode os scripts de verificação.")
st.code("streamlit run app/app.py", language="bash")