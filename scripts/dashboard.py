import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Dashboard - Inspeção Autônoma", layout="wide")

st.title("🏭 Dashboard de Qualidade: Esteira de Envase")
st.markdown("Monitoramento em tempo real das predições do modelo de Visão Computacional.")

st.header("📊 Métricas de Performance da IA")
col1, col2, col3 = st.columns(3)
col1.metric(label="Acurácia do Modelo", value="54.0%", delta="Underfitting detectado")
col2.metric(label="F1-Score (Contaminação)", value="0.55", delta="+0.55 vs Baseline")
col3.metric(label="Recall (Garrafas Boas)", value="62.0%", delta="Redução de Desperdício")

st.divider()

st.header("📉 Probabilidade de Falha e Distribuição")
col_grafico1, col_grafico2 = st.columns(2)

with col_grafico1:
    st.subheader("Distribuição de Defeitos Detectados")
    dados_defeitos = pd.DataFrame({
        'Classe': ['good', 'broken_small', 'broken_large', 'contamination'],
        'Quantidade': [8, 6, 4, 6]
    })
    st.bar_chart(dados_defeitos.set_index('Classe'))

with col_grafico2:
    st.subheader("Simulador de Inferência (Tempo Real)")
    arquivo_upload = st.file_uploader("Faça o upload de uma garrafa da esteira", type=["png", "jpg"])

    if arquivo_upload is not None:
        st.image(arquivo_upload, caption="Imagem da Esteira Capturada", width=250)
        st.success("Análise Concluída!")
        st.warning("Diagnóstico da IA: Possível anomalia detectada. Encaminhando para verificação.")
