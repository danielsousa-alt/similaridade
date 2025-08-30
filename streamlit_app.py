#!/usr/bin/env python3
"""
Classificador Manual para Re-treinamento - Versão com Contraste Corrigido
Sistema para classificação humana de formulários
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

# Configuração da página
st.set_page_config(
    page_title="Classificador Manual",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado com contraste melhorado
st.markdown("""
<style>
    /* Configurações gerais para melhor contraste */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Header principal */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        color: white !important;
        margin: 0;
        font-size: 2rem;
        font-weight: bold;
    }
    
    .main-header p {
        color: white !important;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Cards de informação com melhor contraste */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .info-card h3 {
        color: #2c3e50 !important;
        margin-top: 0;
        font-size: 1.2rem;
        font-weight: bold;
    }
    
    .info-card p {
        color: #34495e !important;
        margin: 0.5rem 0;
    }
    
    .info-card strong {
        color: #2c3e50 !important;
        font-weight: bold;
    }
    
    /* Card da IA */
    .ai-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #007bff;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .ai-card h4 {
        color: #007bff !important;
        margin-top: 0;
        font-weight: bold;
    }
    
    .ai-card p {
        color: #495057 !important;
    }
    
    /* Card do usuário */
    .user-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .user-card h3 {
        color: #28a745 !important;
        margin-top: 0;
        font-weight: bold;
    }
    
    .user-card h4 {
        color: #28a745 !important;
        margin-top: 0;
        font-weight: bold;
    }
    
    .user-card p {
        color: #495057 !important;
    }
    
    /* Alertas com melhor contraste */
    .success-alert {
        background: #d4edda;
        color: #155724 !important;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    .success-alert h3 {
        color: #155724 !important;
        margin-top: 0;
        font-weight: bold;
    }
    
    .warning-alert {
        background: #fff3cd;
        color: #856404 !important;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #ffeaa7;
        margin: 1rem 0;
    }
    
    /* Métricas com melhor contraste */
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        border: 1px solid #e0e0e0;
    }
    
    /* Botões melhorados */
    .stButton > button {
        border-radius: 25px;
        border: 2px solid #007bff;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
        background: white;
        color: #007bff;
    }
    
    .stButton > button:hover {
        background: #007bff;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 123, 255, 0.3);
    }
    
    /* Botão primário */
    .stButton > button[kind="primary"] {
        background: #007bff;
        color: white;
        border: 2px solid #007bff;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: #0056b3;
        border: 2px solid #0056b3;
    }
    
    /* Melhorar contraste dos inputs */
    .stSelectbox > div > div {
        background: white;
        border: 2px solid #ced4da;
        border-radius: 8px;
    }
    
    .stTextInput > div > div {
        background: white;
        border: 2px solid #ced4da;
        border-radius: 8px;
    }
    
    .stTextArea > div > div {
        background: white;
        border: 2px solid #ced4da;
        border-radius: 8px;
    }
    
    /* Labels mais visíveis */
    .stSelectbox > label,
    .stTextInput > label,
    .stTextArea > label,
    .stSlider > label {
        color: #2c3e50 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    /* Melhorar contraste do slider */
    .stSlider > div > div > div > div {
        background: #007bff;
    }
    
    /* Informações melhor visíveis */
    .stInfo {
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460 !important;
    }
    
    .stSuccess {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724 !important;
    }
    
    .stWarning {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404 !important;
    }
    
    .stError {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24 !important;
    }
    
    /* Melhorar métricas do Streamlit */
    [data-testid="metric-container"] {
        background: white;
        border: 1px solid #e0e0e0;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    [data-testid="metric-container"] > div {
        color: #2c3e50 !important;
    }
    
    /* Texto da descrição mais legível */
    .stTextArea textarea {
        color: #2c3e50 !important;
        background: white !important;
        border: 2px solid #ced4da !important;
    }
    
    /* Progress bar mais visível */
    .stProgress > div > div {
        background: #007bff;
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# CONFIGURAÇÕES DE DADOS
# ========================================

# Arquivo de dados
DADOS_FILE = "dados_embbeding.csv"
CONTRIBUTIONS_FILE = "contribuicoes_usuarios.csv"
ANALYZED_FILE = "formularios_analisados.json"

# Categorias organizadas para melhor UX
CATEGORIAS = {
    "🏢 Administração e RH": [
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
    "👥 Atendimento": [
        "Atendimento de solicitações de titulares de dados",
        "Atendimento colaboradores",
        "Atendimento ao Cliente",
        "Atendimento a Fornecedores",
        "Atendimento Ouvidoria",
        "Atendimento Presencial",
        "Atendimento Remoto",
        "Outros - Atendimento"
    ],
    "⚖️ Auditoria, Compliance e Jurídico": [
        "Auditoria Externa",
        "Auditoria Interna",
        "Compliance normativo",
        "Contencioso",
        "Contratos e parcerias",
        "Controle interno",
        "Outros - Auditoria e Compliance"
    ],
    "💻 Dados, TI e BI": [
        "Desenvolvimento de ETLs que contenham dados pessoais",
        "Painéis Data Sebrae",
        "Projetos Data Science",
        "Sistemas Transacionais que contenham dados pessoais",
        "Infraestrutura de TI",
        "Backup e recuperação",
        "Outros - Dados e TI"
    ],
    "📚 Educação e Consultoria": [
        "Capacitação interna",
        "Capacitação/treinamento",
        "Consultoria",
        "Educação empreendedora",
        "Outros - Educação"
    ],
    "📈 Gestão, Estratégia e Processos": [
        "Planejamento estratégico",
        "Gestão de processos",
        "Gestão de projetos",
        "Governança corporativa",
        "Outros - Gestão"
    ],
    "🔧 Outras Atividades": [
        "Atividades diversas",
        "Não classificado",
        "Outros"
    ]
}

# ========================================
# FUNÇÕES AUXILIARES
# ========================================

@st.cache_data
def carregar_formularios_analisados():
    """Carrega lista de formulários já analisados"""
    try:
        if hasattr(st.session_state, 'formularios_analisados'):
            return st.session_state.formularios_analisados
        return {}
    except:
        return {}

def salvar_formulario_analisado(forms_number, usuario):
    """Salva formulário como analisado"""
    if 'formularios_analisados' not in st.session_state:
        st.session_state.formularios_analisados = {}
    
    if str(forms_number) not in st.session_state.formularios_analisados:
        st.session_state.formularios_analisados[str(forms_number)] = []
    
    if usuario not in st.session_state.formularios_analisados[str(forms_number)]:
        st.session_state.formularios_analisados[str(forms_number)].append(usuario)

@st.cache_data
def carregar_dados():
    """Carrega dados dos formulários"""
    try:
        df = pd.read_csv(DADOS_FILE)
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
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

def extrair_nome_atividade(forms_text):
    """Extrai nome da atividade de forma inteligente"""
    if pd.isna(forms_text) or not forms_text:
        return "📋 Sem nome definido"
    
    partes = str(forms_text).split(';')
    nome = partes[0].strip().lstrip(' .,;-')
    
    if len(nome) > 80:
        nome = nome[:77] + "..."
    
    return f"📋 {nome}" if nome else "📋 Sem nome definido"

# ========================================
# COMPONENTES UI
# ========================================

def render_header():
    """Renderiza header principal"""
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Classificador Manual Inteligente</h1>
        <p>Sistema para classificação humana e re-treinamento do modelo</p>
    </div>
    """, unsafe_allow_html=True)

def render_user_welcome(usuario):
    """Renderiza boas-vindas do usuário"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"""
        <div class="user-card">
            <h3>👋 Bem-vindo, {usuario}!</h3>
            <p>Vamos classificar alguns formulários para melhorar o modelo de IA?</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🚪 Trocar Usuário", help="Clique para trocar de usuário"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()

def render_statistics(df_total, df_disponivel, usuario):
    """Renderiza estatísticas em cards visuais"""
    # Calcular estatísticas
    analisados = st.session_state.get('formularios_analisados', {})
    total_analisados = len([f for f, users in analisados.items() if usuario in users])
    
    contribuicoes_usuario = len([c for c in st.session_state.get('contribuicoes', []) if c.get('usuario') == usuario])
    
    # Layout em 4 colunas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Total de Formulários",
            value=f"{len(df_total):,}",
            help="Total de formulários no sistema"
        )
    
    with col2:
        st.metric(
            label="🎯 Disponíveis para Você",
            value=f"{len(df_disponivel):,}",
            help="Formulários que você ainda não analisou"
        )
    
    with col3:
        progresso = (total_analisados / len(df_total)) * 100 if len(df_total) > 0 else 0
        st.metric(
            label="✅ Você Analisou",
            value=f"{total_analisados:,}",
            delta=f"{progresso:.1f}% do total",
            help="Número de formulários que você já analisou"
        )
    
    with col4:
        st.metric(
            label="💾 Contribuições Salvas",
            value=f"{contribuicoes_usuario:,}",
            help="Suas classificações salvas no sistema"
        )

# ========================================
# FUNÇÃO PRINCIPAL
# ========================================

def main():
    # Verificar se arquivo de dados existe
    if not Path(DADOS_FILE).exists():
        st.error("❌ Arquivo 'dados_embbeding.csv' não encontrado!")
        st.info("📁 Certifique-se de que o arquivo está na raiz do repositório")
        st.stop()

    # Header
    render_header()
    
    # Autenticação do usuário
    if 'usuario_autenticado' not in st.session_state:
        st.session_state.usuario_autenticado = False
    
    if not st.session_state.usuario_autenticado:
        st.markdown("### 👤 Identificação do Usuário")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            usuario = st.text_input(
                "Digite seu primeiro nome:",
                placeholder="Ex: João, Maria, Pedro...",
                help="Seu nome será usado para rastrear suas contribuições"
            )
            
            if usuario and len(usuario.strip()) >= 2:
                if st.button("🚀 Começar Classificação", type="primary", use_container_width=True):
                    st.session_state.usuario = usuario.strip().title()
                    st.session_state.usuario_autenticado = True
                    st.rerun()
            elif usuario:
                st.warning("⚠️ Nome deve ter pelo menos 2 caracteres")
        
        return
    
    # Usuário autenticado
    usuario = st.session_state.usuario
    render_user_welcome(usuario)
    
    # Carregar dados
    df = carregar_dados()
    if df.empty:
        st.error("❌ Não foi possível carregar os dados do sistema")
        return
    
    # Filtrar formulários disponíveis
    df_disponivel = filtrar_formularios_nao_analisados(df, usuario)
    
    # Estatísticas
    render_statistics(df, df_disponivel, usuario)
    
    # Verificar se há formulários disponíveis
    if df_disponivel.empty:
        st.markdown("""
        <div class="success-alert">
            <h3>🎉 Parabéns!</h3>
            <p>Você já analisou todos os formulários disponíveis no sistema!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar contribuições
        contribuicoes = st.session_state.get('contribuicoes', [])
        suas_contrib = [c for c in contribuicoes if c.get('usuario') == usuario]
        
        if suas_contrib:
            st.subheader("📊 Suas Contribuições")
            df_contrib = pd.DataFrame(suas_contrib)
            st.dataframe(df_contrib, use_container_width=True)
            
            # Botão para baixar contribuições
            csv = df_contrib.to_csv(index=False)
            st.download_button(
                label="📥 Baixar Minhas Contribuições (CSV)",
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
        if st.button("⬅️ Anterior", disabled=st.session_state.indice_atual == 0):
            st.session_state.indice_atual = max(0, st.session_state.indice_atual - 1)
            st.rerun()
    
    with col2:
        if st.button("⏭️ Pular", help="Pular este formulário"):
            st.session_state.indice_atual = min(len(df_disponivel) - 1, st.session_state.indice_atual + 1)
            st.rerun()
    
    with col3:
        progresso = st.session_state.indice_atual + 1
        total = len(df_disponivel)
        st.info(f"📋 Formulário {progresso} de {total}")
    
    with col4:
        ir_para = st.number_input("Ir para:", min_value=1, max_value=len(df_disponivel), 
                                  value=st.session_state.indice_atual + 1, 
                                  key="nav_input")
        if ir_para != st.session_state.indice_atual + 1:
            st.session_state.indice_atual = ir_para - 1
            st.rerun()
    
    with col5:
        if st.button("➡️ Próximo", disabled=st.session_state.indice_atual >= len(df_disponivel) - 1):
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
            <div class="info-card">
                <h3>{extrair_nome_atividade(forms_text)}</h3>
                <p><strong>🆔 Formulário:</strong> {forms_number}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Descrição
            st.markdown("**📄 Descrição da Atividade:**")
            st.text_area("Conteúdo do formulário", value=forms_text, height=200, disabled=True, label_visibility="collapsed")
        
        with col_direita:
            st.markdown("""
            <div class="user-card">
                <h4>👤 Sua Classificação</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Seleção de categoria
            categoria_selecionada = st.selectbox(
                "🏷️ Categoria Principal:",
                list(CATEGORIAS.keys()),
                key=f"categoria_{forms_number}",
                help="Selecione a categoria que melhor descreve esta atividade"
            )
            
            if categoria_selecionada:
                subcategoria_selecionada = st.selectbox(
                    "🏷️ Subcategoria:",
                    CATEGORIAS[categoria_selecionada],
                    key=f"subcategoria_{forms_number}",
                    help="Selecione a subcategoria específica"
                )
            else:
                subcategoria_selecionada = None
            
            # Nível de certeza
            certeza = st.slider(
                "🎯 Seu nível de certeza:",
                0.0, 1.0, 0.8, 0.1,
                key=f"certeza_{forms_number}",
                format="%.0f%%",
                help="0% = Totalmente incerto, 100% = Totalmente certo"
            )
            
            # Comentários
            comentarios = st.text_area(
                "💭 Comentários (opcional):",
                placeholder="Ex: 'Categoria óbvia pelo contexto' ou 'Difícil de classificar'",
                key=f"comentarios_{forms_number}",
                help="Adicione observações que possam ajudar outros analistas"
            )
        
        # Botão de salvar
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if categoria_selecionada and subcategoria_selecionada:
                if st.button("💾 Salvar Classificação e Continuar", type="primary", use_container_width=True):
                    # Preparar dados
                    contribuicao = {
                        'forms_number': forms_number,
                        'forms_name': extrair_nome_atividade(forms_text).replace('📋 ', ''),
                        'descricao_atividade': forms_text,
                        'categoria_usuario': categoria_selecionada.replace('🏢 ', '').replace('👥 ', '').replace('⚖️ ', '').replace('💻 ', '').replace('📚 ', '').replace('📈 ', '').replace('🔧 ', ''),
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
                    st.success("✅ Classificação salva com sucesso!")
                    
                    # Avançar automaticamente
                    if st.session_state.indice_atual < len(df_disponivel) - 1:
                        st.session_state.indice_atual += 1
                        st.rerun()
                    else:
                        st.balloons()
                        st.success("🎉 Você concluiu todos os formulários disponíveis!")
                        st.rerun()
            else:
                st.warning("⚠️ Por favor, selecione categoria e subcategoria antes de salvar")

if __name__ == "__main__":
    main()
