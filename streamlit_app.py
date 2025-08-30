#!/usr/bin/env python3
"""
Classificador Manual - Versão Clean e Profissional
Sistema para classificação humana e re-treinamento do modelo
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
from pathlib import Path
import json
import base64

# ========================================
# CONFIGURAÇÃO E ESTILO
# ========================================

# Configuração da página
st.set_page_config(
    page_title="Classificador Manual - Sebrae",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS clean com fundo branco e texto escuro
st.markdown("""
<style>
    /* RESET E BASE */
    .stApp {
        background-color: #ffffff !important;
        color: #2c3e50 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main .block-container {
        background-color: #ffffff !important;
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* HEADER PRINCIPAL */
    .main-header {
        background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
        padding: 2rem;
        border-radius: 8px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 2px 10px rgba(44, 62, 80, 0.1);
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .main-header h1 {
        color: white !important;
        margin: 0;
        font-size: 2.2rem;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    
    .main-header p {
        color: #ecf0f1 !important;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* CARDS LIMPOS */
    .card {
        background: #ffffff;
        border: 1px solid #e1e8ed;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .card h3 {
        color: #2c3e50 !important;
        margin: 0 0 1rem 0;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    .card p {
        color: #34495e !important;
        margin: 0.5rem 0;
        line-height: 1.5;
    }
    
    .card strong {
        color: #2c3e50 !important;
        font-weight: 600;
    }
    
    /* CARD DE USUÁRIO */
    .user-card {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-left: 4px solid #27ae60;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .user-card h3 {
        color: #27ae60 !important;
        margin: 0 0 0.5rem 0;
        font-weight: 600;
    }
    
    .user-card p {
        color: #34495e !important;
        margin: 0;
    }
    
    /* ALERTAS */
    .alert-success {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724 !important;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .alert-success h3 {
        color: #155724 !important;
        margin: 0 0 0.5rem 0;
        font-weight: 600;
    }
    
    /* INPUTS LIMPOS */
    .stSelectbox > div > div {
        background: #ffffff !important;
        border: 2px solid #34495e !important;
        border-radius: 6px;
        font-size: 1rem;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #3498db !important;
        box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
    }
    
    .stTextInput > div > div {
        background: #ffffff !important;
        border: 2px solid #34495e !important;
        border-radius: 6px;
    }
    
    .stTextInput > div > div:focus-within {
        border-color: #3498db !important;
        box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
    }
    
    .stTextArea > div > div {
        background: #ffffff !important;
        border: 2px solid #34495e !important;
        border-radius: 6px;
    }
    
    .stTextArea > div > div:focus-within {
        border-color: #3498db !important;
        box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
    }
    
    .stTextArea textarea {
        background: #ffffff !important;
        color: #2c3e50 !important;
        font-size: 14px;
        line-height: 1.5;
    }
    
    .stNumberInput > div > div {
        background: #ffffff !important;
        border: 2px solid #34495e !important;
        border-radius: 6px;
    }
    
    .stNumberInput input {
        color: #2c3e50 !important;
        background: #ffffff !important;
    }
    
    /* LABELS */
    .stSelectbox > label,
    .stTextInput > label,
    .stTextArea > label,
    .stSlider > label,
    .stNumberInput > label {
        color: #2c3e50 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* BOTÕES LIMPOS */
    .stButton > button {
        background: #ffffff !important;
        color: #34495e !important;
        border: 2px solid #34495e !important;
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        background: #34495e !important;
        color: #ffffff !important;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(52, 73, 94, 0.3);
    }
    
    .stButton > button[kind="primary"] {
        background: #3498db !important;
        color: #ffffff !important;
        border: 2px solid #3498db !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: #2980b9 !important;
        border: 2px solid #2980b9 !important;
        box-shadow: 0 2px 8px rgba(52, 152, 219, 0.3);
    }
    
    /* MÉTRICAS */
    [data-testid="metric-container"] {
        background: #ffffff;
        border: 1px solid #e1e8ed;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    [data-testid="metric-container"] > div {
        color: #2c3e50 !important;
    }
    
    /* SLIDER */
    .stSlider > div > div > div > div {
        background: #3498db !important;
    }
    
    /* ALERTAS DO STREAMLIT */
    .stInfo {
        background: #e3f2fd !important;
        border: 1px solid #bbdefb !important;
        color: #0d47a1 !important;
        border-radius: 6px;
    }
    
    .stSuccess {
        background: #e8f5e8 !important;
        border: 1px solid #c8e6c9 !important;
        color: #2e7d32 !important;
        border-radius: 6px;
    }
    
    .stWarning {
        background: #fff8e1 !important;
        border: 1px solid #ffecb3 !important;
        color: #f57f17 !important;
        border-radius: 6px;
    }
    
    .stError {
        background: #ffebee !important;
        border: 1px solid #ffcdd2 !important;
        color: #c62828 !important;
        border-radius: 6px;
    }
    
    /* NAVIGATION BAR */
    .nav-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* FORMULÁRIO ATUAL */
    .form-info {
        background: #ffffff;
        border: 1px solid #e1e8ed;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .form-info h3 {
        color: #2c3e50 !important;
        margin: 0 0 1rem 0;
        font-weight: 600;
        font-size: 1.2rem;
    }
    
    /* CLASSIFICAÇÃO SECTION */
    .classification-section {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .classification-section h4 {
        color: #2c3e50 !important;
        margin: 0 0 1rem 0;
        font-weight: 600;
    }
    
    /* RESPONSIVIDADE */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.8rem;
        }
        
        .main .block-container {
            padding: 1rem;
        }
        
        .card, .user-card, .form-info, .classification-section {
            padding: 1rem;
        }
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

def get_logo_svg():
    """Retorna SVG da logo como string"""
    return """
    <svg width="40" height="40" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M20 35c0-15 10-25 25-25s25 10 25 25c5-10 15-15 25-15 8 0 15 7 15 15 0 5-2 9-5 12 3 3 5 7 5 12 0 8-7 15-15 15-5 0-9-2-12-5-3 8-11 14-20 14-12 0-22-10-22-22 0-3 1-6 2-8-10-2-18-10-18-18z" fill="white" stroke="#ecf0f1" stroke-width="2"/>
      <circle cx="35" cy="45" r="3" fill="#3498db"/>
      <circle cx="55" cy="40" r="3" fill="#3498db"/>
      <circle cx="45" cy="55" r="3" fill="#3498db"/>
      <circle cx="65" cy="50" r="3" fill="#3498db"/>
      <line x1="35" y1="45" x2="45" y2="55" stroke="#3498db" stroke-width="2"/>
      <line x1="45" y1="55" x2="55" y2="40" stroke="#3498db" stroke-width="2"/>
      <line x1="55" y1="40" x2="65" y2="50" stroke="#3498db" stroke-width="2"/>
      <line x1="35" y1="45" x2="55" y2="40" stroke="#3498db" stroke-width="2"/>
    </svg>
    """

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

    # Header com logo
    logo_svg = get_logo_svg()
    st.markdown(f"""
    <div class="main-header">
        <div class="logo-container">
            {logo_svg}
            <div>
                <h1>Classificador Manual Inteligente</h1>
                <p>Sistema para classificação humana e re-treinamento do modelo - SEBRAE</p>
            </div>
        </div>
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
    
    # Boas-vindas
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
        <div class="user-card">
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
    
    # Métricas
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
        <div class="alert-success">
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
            # Informações do formulário
            st.markdown(f"""
            <div class="form-info">
                <h3>{extrair_nome_atividade(forms_text)}</h3>
                <p><strong>Formulário:</strong> {forms_number}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Descrição
            st.markdown("**Descrição da Atividade:**")
            st.text_area("Conteúdo do formulário", value=forms_text, height=200, disabled=True, label_visibility="collapsed")
        
        with col_direita:
            st.markdown("""
            <div class="classification-section">
                <h4>Sua Classificação</h4>
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
