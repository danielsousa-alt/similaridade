#!/usr/bin/env python3
"""
Aplicação Streamlit para Classificação Manual
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
from pathlib import Path
import json

# Configuração da página
st.set_page_config(
    page_title="Classificador Manual",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Verificar se arquivo de dados existe
if not Path("dados_embbeding.csv").exists():
    st.error("❌ Arquivo 'dados_embbeding.csv' não encontrado!")
    st.stop()

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🎯 Classificador Manual</h1>
    <p>Sistema para classificação de formulários</p>
</div>
""", unsafe_allow_html=True)

# Teste básico
st.success("✅ Aplicação carregada com sucesso!")

# Carregar dados
try:
    df = pd.read_csv("dados_embbeding.csv")
    st.info(f"📊 {len(df)} formulários carregados")
    
    # Mostrar amostra
    if st.button("Ver amostra dos dados"):
        st.dataframe(df.head())
        
except Exception as e:
    st.error(f"❌ Erro ao carregar dados: {e}")
