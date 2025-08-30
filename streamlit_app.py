#!/usr/bin/env python3
"""
Classificador Manual - Versão Final com Tema Forçado
Sistema para classificação humana e re-treinamento do modelo
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
from pathlib import Path
import json

# ========================================
# CONFIGURAÇÃO E ESTILO
# ========================================

# Configuração da página com tema forçado
st.set_page_config(
    page_title="Classificador Manual - Sebrae",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS para forçar completamente tema claro
st.markdown("""
<style>
    /* RESET COMPLETO - FORÇA TEMA CLARO */
    * {
        color-scheme: light !important;
    }
    
    html, body {
        background-color: #ffffff !important;
        color: #000000 !important;
        color-scheme: light !important;
    }
    
    .stApp {
        background-color: #ffffff !important;
        color: #000000 !important;
        color-scheme: light !important;
    }
    
    .main .block-container {
        background-color: #ffffff !important;
        color: #000000 !important;
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* FORÇAR TODOS OS ELEMENTOS PARA TEMA CLARO */
    div, p, span, label, h1, h2, h3, h4, h5, h6, section, article {
        background-color: inherit !important;
        color: #000000 !important;
    }
    
    /* HEADER SIMPLES E LIMPO */
    .header-container {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .header-title {
        color: white !important;
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        color: #ecf0f1 !important;
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
    }
    
    /* CARDS SIMPLES */
    .card-white {
        background: #ffffff !important;
        border: 2px solid #34495e !important;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #000000 !important;
    }
    
    .card-white h3 {
        color: #2c3e50 !important;
        margin: 0 0 1rem 0;
        font-weight: bold;
    }
    
    .card-white p {
        color: #34495e !important;
        margin: 0.5rem 0;
    }
    
    /* CARD DE USUÁRIO */
    .user-welcome {
        background: #f8f9fa !important;
        border: 2px solid #27ae60 !important;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #000000 !important;
    }
    
    .user-welcome h3 {
        color: #27ae60 !important;
        margin: 0 0 0.5rem 0;
        font-weight: bold;
    }
    
    .user-welcome p {
        color: #2c3e50 !important;
        margin: 0;
    }
    
    /* INPUTS COM MÁXIMO CONTRASTE */
    .stSelectbox > div > div {
        background: #ffffff !important;
        border: 3px solid #000000 !important;
        border-radius: 5px;
        color: #000000 !important;
    }
    
    .stSelectbox > div > div > div {
        color: #000000 !important;
        background: #ffffff !important;
    }
    
    .stTextInput > div > div {
        background: #ffffff !important;
        border: 3px solid #000000 !important;
        border-radius: 5px;
        color: #000000 !important;
    }
    
    .stTextInput input {
        color: #000000 !important;
        background: #ffffff !important;
    }
    
    .stTextArea > div > div {
        background: #ffffff !important;
        border: 3px solid #000000 !important;
        border-radius: 5px;
    }
    
    .stTextArea textarea {
        background: #ffffff !important;
        color: #000000 !important;
        font-size: 14px;
    }
    
    .stNumberInput > div > div {
        background: #ffffff !important;
        border: 3px solid #000000 !important;
        border-radius: 5px;
    }
    
    .stNumberInput input {
        color: #000000 !important;
        background: #ffffff !important;
    }
    
    /* LABELS ESCUROS */
    .stSelectbox > label,
    .stTextInput > label,
    .stTextArea > label,
    .stSlider > label,
    .stNumberInput > label {
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 1rem !important;
    }
    
    /* BOTÕES COM CONTRASTE */
    .stButton > button {
        background: #ffffff !important;
        color: #2c3e50 !important;
        border: 3px solid #2c3e50 !important;
        border-radius: 5px;
        padding: 0.5rem 1.5rem;
        font-weight: bold;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background: #2c3e50 !important;
        color: #ffffff !important;
    }
    
    .stButton > button[kind="primary"] {
        background: #3498db !important;
        color: #ffffff !important;
        border: 3px solid #3498db !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: #2980b9 !important;
        border: 3px solid #2980b9 !important;
    }
    
    /* MÉTRICAS CONTRASTADAS */
    [data-testid="metric-container"] {
        background: #ffffff !important;
        border: 2px solid #000000 !important;
        border-radius: 8px;
        padding: 1rem;
        color: #000000 !important;
    }
    
    [data-testid="metric-container"] * {
        color: #000000 !important;
    }
    
    /* ALERTAS STREAMLIT */
    .stInfo {
        background: #e3f2fd !important;
        border: 2px solid #1976d2 !important;
        color: #0d47a1 !important;
        border-radius: 5px;
    }
    
    .stSuccess {
        background: #e8f5e8 !important;
        border: 2px solid #388e3c !important;
        color: #1b5e20 !important;
        border-radius: 5px;
    }
    
    .stWarning {
        background: #fff8e1 !important;
        border: 2px solid #f57c00 !important;
        color: #e65100 !important;
        border-radius: 5px;
    }
    
    .stError {
        background: #ffebee !important;
        border: 2px solid #d32f2f !important;
        color: #b71c1c !important;
        border-radius: 5px;
    }
    
    /* SLIDER */
    .stSlider > div > div > div > div {
        background: #3498db !important;
    }
    
    /* FORÇAR SIDEBAR CLARA */
    .css-1d391kg {
        background: #f8f9fa !important;
        color: #000000 !important;
    }
    
    /* SUCCESS ALERT CUSTOMIZADO */
    .success-box {
        background: #d4edda !important;
        border: 2px solid #28a745 !important;
        color: #155724 !important;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .success-box h3 {
        color: #155724 !important;
        margin: 0 0 0.5rem 0;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# CONFIGURAÇÕES DE DADOS
# ========================================

DADOS_FILE = "dados_embbeding.csv"

# Categorias sem emojis
CATEGORIAS = {
    "Administração e RH": [
        "Gestão de folha de pagamento",
        "Gestão de benefícios", 
        "Gestão de entrega de equipamentos",
        "Atualização cadastral de colaboradores",
        "Elaboração de contratos",
        "Gestão do Clima Organizacional",
        "Recrutamento e seleção",
        "Desligamento de colaboradores",
        "Gestão de exames ocupacionais",
        "Outros - Administração e RH"
    ],
    "Atendimento": [
        "Atendimento de solicitações de titulares de dados",
        "Atendimento colaboradores",
        "Atendimento ao Cliente",
        "Atendimento a Fornecedores",
        "Atendimento Ouvidoria",
        "Atendimento Presencial",
        "Atendimento Remoto",
        "Outros - Atendimento"
    ],
    "Auditoria, Compliance e Jurídico": [
        "Auditoria Externa",
        "Auditoria Interna",
        "Compliance normativo",
        "Contencioso",
        "Contratos e parcerias",
        "Controle interno",
        "Outros - Auditoria e Compliance"
    ],
    "Dados, TI e BI": [
        "Desenvolvimento de ETLs que contenham dados pessoais",
        "Painéis Data Sebrae",
        "Projetos Data Science",
        "Sistemas Transacionais que contenham dados pessoais",
        "Infraestrutura de TI",
        "Backup e recuperação",
        "Outros - Dados e TI"
    ],
    "Educação e Consultoria": [
        "Capacitação interna",
        "Capacitação/treinamento",
        "Consultoria",
        "Educação empreendedora",
        "Outros - Educação"
    ],
    "Gestão, Estratégia e Processos": [
        "Planejamento estratégico",
        "Gestão de processos",
        "Gestão de projetos",
        "Governança corporativa",
        "Outros - Gestão"
    ],
    "Outras Atividades": [
        "Atividades diversas",
        "Não classificado",
        "Outros"
    ]
}

# ========================================
# FUNÇÕES AUXILIARES
# ========================================

@st.cache_data
def carregar_dados():
    """Carrega dados dos formulários"""
    try:
        df = pd.read_csv(DADOS_FILE)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

def filtrar_formularios_nao_analisados(df, usuario):
    """Filtra formulários não analisados pelo usuário"""
    if 'formularios_analisados' not in st.session_state:
        return df.copy()
    
    analisados = st.session_state.formularios_analisados
    forms_analisados_usuario = []
    
    for forms_number, usuarios in analisados.items():
        if usuario in usuarios:
            forms_analisados_usuario.append(int(forms_number))
    
    if forms_analisados_usuario:
        return df[~df['forms_number'].isin(forms_analisados_usuario)]
    return df.copy()

def salvar_contribuicao(dados_contribuicao):
    """Salva contribuição no session state"""
    if 'contribuicoes' not in st.session_state:
        st.session_state.contribuicoes = []
    st.session_state.contribuicoes.append(dados_contribuicao)

def salvar_formulario_analisado(forms_number, usuario):
    """Salva formulário como analisado"""
    if 'formularios_analisados' not in st.session_state:
        st.session_state.formularios_analisados = {}
    
    if str(forms_number) not in st.session_state.formularios_analisados:
        st.session_state.formularios_analisados[str(forms_number)] = []
    
    if usuario not in st.session_state.formularios_analisados[str(forms_number)]:
        st.session_state.formularios_analisados[str(forms_number)].append(usuario)

def extrair_nome_atividade(forms_text):
    """Extrai nome da atividade"""
    if pd.isna(forms_text) or not forms_text:
        return "Sem nome definido"
    
    partes = str(forms_text).split(';')
    nome = partes[0].strip().lstrip(' .,;-')
    
    if len(nome) > 80:
        nome = nome[:77] + "..."
    
    return nome if nome else "Sem nome definido"

# ========================================
# FUNÇÃO PRINCIPAL
# ========================================

def main():
    # Verificar se arquivo de dados existe
    if not Path(DADOS_FILE).exists():
        st.error("Arquivo 'dados_embbeding.csv' não encontrado!")
        st.info("Certifique-se de que o arquivo está na raiz do repositório")
        st.stop()

    # Header simples sem HTML complexo
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">Classificador Manual Inteligente</h1>
        <p class="header-subtitle">Sistema para classificação humana e re-treinamento do modelo - SEBRAE</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Autenticação do usuário
    if 'usuario_autenticado' not in st.session_state:
        st.session_state.usuario_autenticado = False
    
    if not st.session_state.usuario_autenticado:
        st.markdown("### Identificação do Usuário")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            usuario = st.text_input(
                "Digite seu primeiro nome:",
                placeholder="Ex: João, Maria, Pedro...",
                help="Seu nome será usado para rastrear suas contribuições"
            )
            
            if usuario and len(usuario.strip()) >= 2:
                if st.button("Começar Classificação", type="primary", use_container_width=True):
                    st.session_state.usuario = usuario.strip().title()
                    st.session_state.usuario_autenticado = True
                    st.rerun()
            elif usuario:
                st.warning("Nome deve ter pelo menos 2 caracteres")
        
        return
    
    # Usuário autenticado
    usuario = st.session_state.usuario
    
    # Boas-vindas simples
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
        <div class="user-welcome">
            <h3>Bem-vindo, {usuario}!</h3>
            <p>Vamos classificar alguns formulários para melhorar o modelo de IA?</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("Trocar Usuário", help="Clique para trocar de usuário"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()
    
    # Carregar dados
    df = carregar_dados()
    if df.empty:
        st.error("Não foi possível carregar os dados do sistema")
        return
    
    # Filtrar formulários disponíveis
    df_disponivel = filtrar_formularios_nao_analisados(df, usuario)
    
    # Estatísticas
    analisados = st.session_state.get('formularios_analisados', {})
    total_analisados = len([f for f, users in analisados.items() if usuario in users])
    contribuicoes_usuario = len([c for c in st.session_state.get('contribuicoes', []) if c.get('usuario') == usuario])
    
    # Métricas simples
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Formulários", f"{len(df):,}")
    
    with col2:
        st.metric("Disponíveis para Você", f"{len(df_disponivel):,}")
    
    with col3:
        progresso = (total_analisados / len(df)) * 100 if len(df) > 0 else 0
        st.metric("Você Analisou", f"{total_analisados:,}", f"{progresso:.1f}% do total")
    
    with col4:
        st.metric("Contribuições Salvas", f"{contribuicoes_usuario:,}")
    
    # Verificar se há formulários disponíveis
    if df_disponivel.empty:
        st.markdown("""
        <div class="success-box">
            <h3>Parabéns!</h3>
            <p>Você já analisou todos os formulários disponíveis no sistema!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar contribuições
        contribuicoes = st.session_state.get('contribuicoes', [])
        suas_contrib = [c for c in contribuicoes if c.get('usuario') == usuario]
        
        if suas_contrib:
            st.subheader("Suas Contribuições")
            df_contrib = pd.DataFrame(suas_contrib)
            st.dataframe(df_contrib, use_container_width=True)
            
            csv = df_contrib.to_csv(index=False)
            st.download_button(
                label="Baixar Minhas Contribuições (CSV)",
                data=csv,
                file_name=f"contribuicoes_{usuario}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        return
    
    # Controle de navegação
    if 'indice_atual' not in st.session_state:
        st.session_state.indice_atual = 0
    
    # Navegação entre formulários
    st.markdown("---")
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
    
    with col1:
        if st.button("Anterior", disabled=st.session_state.indice_atual == 0):
            st.session_state.indice_atual = max(0, st.session_state.indice_atual - 1)
            st.rerun()
    
    with col2:
        if st.button("Pular", help="Pular este formulário"):
            st.session_state.indice_atual = min(len(df_disponivel) - 1, st.session_state.indice_atual + 1)
            st.rerun()
    
    with col3:
        progresso = st.session_state.indice_atual + 1
        total = len(df_disponivel)
        st.info(f"Formulário {progresso} de {total}")
    
    with col4:
        ir_para = st.number_input("Ir para:", min_value=1, max_value=len(df_disponivel), 
                                  value=st.session_state.indice_atual + 1, 
                                  key="nav_input")
        if ir_para != st.session_state.indice_atual + 1:
            st.session_state.indice_atual = ir_para - 1
            st.rerun()
    
    with col5:
        if st.button("Próximo", disabled=st.session_state.indice_atual >= len(df_disponivel) - 1):
            st.session_state.indice_atual = min(len(df_disponivel) - 1, st.session_state.indice_atual + 1)
            st.rerun()
    
    # Formulário atual
    if st.session_state.indice_atual < len(df_disponivel):
        row = df_disponivel.iloc[st.session_state.indice_atual]
        forms_text = row['forms_text']
        forms_number = row['forms_number']
        
        # Layout principal
        col_esquerda, col_direita = st.columns([1.2, 1])
        
        with col_esquerda:
            # Informações do formulário - simples
            st.markdown(f"""
            <div class="card-white">
                <h3>{extrair_nome_atividade(forms_text)}</h3>
                <p><strong>Formulário:</strong> {forms_number}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Descrição
            st.markdown("**Descrição da Atividade:**")
            st.text_area("Conteúdo do formulário", value=forms_text, height=200, disabled=True, label_visibility="collapsed")
        
        with col_direita:
            st.markdown("""
            <div class="card-white">
                <h3>Sua Classificação</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Seleção de categoria
            categoria_selecionada = st.selectbox(
                "Categoria Principal:",
                list(CATEGORIAS.keys()),
                key=f"categoria_{forms_number}",
                help="Selecione a categoria que melhor descreve esta atividade"
            )
            
            if categoria_selecionada:
                subcategoria_selecionada = st.selectbox(
                    "Subcategoria:",
                    CATEGORIAS[categoria_selecionada],
                    key=f"subcategoria_{forms_number}",
                    help="Selecione a subcategoria específica"
                )
            else:
                subcategoria_selecionada = None
            
            # Nível de certeza
            certeza = st.slider(
                "Seu nível de certeza:",
                0.0, 1.0, 0.8, 0.1,
                key=f"certeza_{forms_number}",
                format="%.0f%%",
                help="0% = Totalmente incerto, 100% = Totalmente certo"
            )
            
            # Comentários
            comentarios = st.text_area(
                "Comentários (opcional):",
                placeholder="Ex: 'Categoria óbvia pelo contexto' ou 'Difícil de classificar'",
                key=f"comentarios_{forms_number}",
                help="Adicione observações que possam ajudar outros analistas"
            )
        
        # Botão de salvar
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if categoria_selecionada and subcategoria_selecionada:
                if st.button("Salvar Classificação e Continuar", type="primary", use_container_width=True):
                    # Preparar dados
                    contribuicao = {
                        'forms_number': forms_number,
                        'forms_name': extrair_nome_atividade(forms_text),
                        'descricao_atividade': forms_text,
                        'categoria_usuario': categoria_selecionada,
                        'subcategoria_usuario': subcategoria_selecionada,
                        'nivel_certeza': certeza,
                        'usuario': usuario,
                        'timestamp': datetime.now().isoformat(),
                        'comentarios': comentarios
                    }
                    
                    # Salvar
                    salvar_contribuicao(contribuicao)
                    salvar_formulario_analisado(forms_number, usuario)
                    
                    # Feedback visual
                    st.success("Classificação salva com sucesso!")
                    
                    # Avançar automaticamente
                    if st.session_state.indice_atual < len(df_disponivel) - 1:
                        st.session_state.indice_atual += 1
                        st.rerun()
                    else:
                        st.balloons()
                        st.success("Você concluiu todos os formulários disponíveis!")
                        st.rerun()
            else:
                st.warning("Por favor, selecione categoria e subcategoria antes de salvar")

if __name__ == "__main__":
    main()
