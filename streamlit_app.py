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
    page_title="Sistema de Classificação Humana - ROPA/RAT",
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
        color: #484D50 !important;
    }
    
    /* HEADER ORIGINAL COM AJUSTES DE CONTRASTE */
    .header-container {
        background: linear-gradient(135deg, #004987 0%, #0056a3 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #ffffff;
    }
    
    .header-title {
        color: #ffffff !important;
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        text-rendering: optimizeLegibility;
    }
    
    .header-subtitle {
        color: #ffffff !important;
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 1;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        text-rendering: optimizeLegibility;
    }
    
    /* CARDS SIMPLES COM FUNDO CINZA PADRÃO COMENTÁRIOS */
    .card-white {
        background: #f8f9fa !important;
        border: 1px solid #ddd !important;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #212529 !important;
    }
    
    .card-white h3 {
        color: #212529 !important;
        margin: 0 0 1rem 0;
        font-weight: bold;
    }
    
    .card-white p {
        color: #212529 !important;
        margin: 0.5rem 0;
    }
    
    /* CARD DE USUÁRIO */
    .user-welcome {
        background: #f8f9fa !important;
        border: 1px solid #ddd !important;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #484D50 !important;
    }
    
    .user-welcome h3 {
        color: #212529 !important;
        margin: 0 0 0.5rem 0;
        font-weight: bold;
    }
    
    .user-welcome p {
        color: #212529 !important;
        margin: 0;
    }
    
    /* INPUTS COM MÁXIMO CONTRASTE */
    .stSelectbox > div > div {
        background: #ffffff !important;
        border: 1px solid #ddd !important;
        border-radius: 5px;
        color: #484D50 !important;
    }
    
    .stSelectbox > div > div > div {
        color: #484D50 !important;
        background: #ffffff !important;
    }
    
    .stTextInput > div > div {
        background: #ffffff !important;
        border: 1px solid #ddd !important;
        border-radius: 5px;
        color: #484D50 !important;
    }
    
    .stTextInput input {
        color: #484D50 !important;
        background: #ffffff !important;
    }
    
    .stTextInput input::placeholder {
        color: #90B1B1 !important;
        opacity: 1 !important;
    }
    
    .stTextArea > div > div {
        background: #ffffff !important;
        border: 1px solid #ddd !important;
        border-radius: 5px;
    }
    
    .stTextArea textarea {
        background: #ffffff !important;
        color: #000000 !important;
        font-size: 16px !important;
        font-weight: bold !important;
        line-height: 1.5 !important;
    }
    
    .stNumberInput > div > div {
        background: #ffffff !important;
        border: 1px solid #ddd !important;
        border-radius: 5px;
    }
    
    .stNumberInput input {
        color: #484D50 !important;
        background: #ffffff !important;
    }
    
    /* LABELS ESCUROS */
    .stSelectbox > label,
    .stTextInput > label,
    .stTextArea > label,
    .stSlider > label,
    .stNumberInput > label {
        color: #484D50 !important;
        font-weight: bold !important;
        font-size: 1rem !important;
    }
    
    /* BOTÕES COM CONTRASTE */
    .stButton > button {
        background: #ffffff !important;
        color: #484D50 !important;
        border: 1px solid #ddd !important;
        border-radius: 5px;
        padding: 0.5rem 1.5rem;
        font-weight: bold;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background: #f8f9fa !important;
        color: #484D50 !important;
    }
    
    .stButton > button[kind="primary"] {
        background: #3498db !important;
        color: #ffffff !important;
        border: 1px solid #3498db !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: #2980b9 !important;
        border: 1px solid #2980b9 !important;
    }
    
    /* BOTÕES ESPECIAIS COM TEXTO BRANCO E BOLD */
    .btn-pular {
        background: #6c757d !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border: 1px solid #6c757d !important;
    }
    
    .btn-trocar-usuario {
        background: #dc3545 !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border: 1px solid #dc3545 !important;
    }
    
    .btn-pular:hover {
        background: #5a6268 !important;
        border: 1px solid #5a6268 !important;
    }
    
    .btn-trocar-usuario:hover {
        background: #c82333 !important;
        border: 1px solid #c82333 !important;
    }
    
    /* MÉTRICAS CONTRASTADAS */
    [data-testid="metric-container"] {
        background: #ffffff !important;
        border: 1px solid #ddd !important;
        border-radius: 8px;
        padding: 1rem;
        color: #484D50 !important;
    }
    
    [data-testid="metric-container"] * {
        color: #484D50 !important;
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

# JavaScript para aplicar estilos específicos aos botões
st.markdown("""
<script>
function aplicarEstilosBotoes() {
    // Aguardar o DOM estar pronto
    setTimeout(function() {
        // Encontrar todos os botões
        const botoes = document.querySelectorAll('button');
        
        botoes.forEach(function(botao) {
            const texto = botao.textContent || botao.innerText;
            
            // Aplicar estilo ao botão "Pular"
            if (texto.includes('Pular')) {
                botao.classList.add('btn-pular');
            }
            
            // Aplicar estilo ao botão "Trocar Usuário"
            if (texto.includes('Trocar Usuário')) {
                botao.classList.add('btn-trocar-usuario');
            }
        });
    }, 100);
}

// Executar quando a página carrega
document.addEventListener('DOMContentLoaded', aplicarEstilosBotoes);

// Executar periodicamente para capturar botões criados dinamicamente
setInterval(aplicarEstilosBotoes, 500);
</script>
""", unsafe_allow_html=True)

# ========================================
# CONFIGURAÇÕES DE DADOS
# ========================================

DADOS_FILE = "dados_embbeding.csv"
CLASSIFICACOES_IA_FILE = "data/classified/level1_classifications.csv"

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

@st.cache_data
def carregar_classificacoes_ia():
    """Carrega classificações da IA"""
    try:
        df_classificacoes = pd.read_csv(CLASSIFICACOES_IA_FILE)
        return df_classificacoes
    except Exception as e:
        st.warning(f"Arquivo de classificações da IA não encontrado: {e}")
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
    """Salva contribuição no session state e em arquivo CSV"""
    # Salvar no session state (para exibição imediata)
    if 'contribuicoes' not in st.session_state:
        st.session_state.contribuicoes = []
    st.session_state.contribuicoes.append(dados_contribuicao)
    
    # Salvar em arquivo CSV estruturado para retreinamento
    salvar_contribuicao_csv(dados_contribuicao)

def salvar_contribuicao_csv(dados_contribuicao):
    """Salva contribuição em arquivo CSV estruturado para retreinamento"""
    try:
        # Diretório de destino
        output_dir = Path("data/human_labels")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Arquivo principal de classificações humanas
        csv_file = output_dir / "human_classifications.csv"
        
        # Estruturar dados para ML/retreinamento
        dados_ml = {
            # Identificação do formulário
            'forms_number': dados_contribuicao['forms_number'],
            'forms_text': dados_contribuicao['descricao_atividade'],
            'forms_title': dados_contribuicao['forms_name'],
            
            # Classificação humana (ground truth)
            'human_category': dados_contribuicao['categoria_usuario'],
            'human_subcategory': dados_contribuicao['subcategoria_usuario'],
            'confidence_human': dados_contribuicao['nivel_certeza'],
            
            # Metadados do classificador
            'classifier_name': dados_contribuicao['usuario'],
            'classification_timestamp': dados_contribuicao['timestamp'],
            'comments': dados_contribuicao.get('comentarios', ''),
            
            # Dados da IA (para comparação)
            'ai_category': dados_contribuicao.get('categoria_ia', ''),
            'ai_confidence': dados_contribuicao.get('confianca_ia', 0.0),
            'ai_threshold_met': dados_contribuicao.get('confianca_ia', 0) > 0.47 if dados_contribuicao.get('confianca_ia') else False,
            
            # Análise de concordância
            'approved_ai': dados_contribuicao.get('aprovou_ia', False),
            'classification_type': dados_contribuicao.get('tipo_classificacao', 'manual'),
            'disagreement_flag': dados_contribuicao.get('categoria_ia') != dados_contribuicao['categoria_usuario'] if dados_contribuicao.get('categoria_ia') else False,
            
            # Qualidade e confiabilidade
            'high_confidence': dados_contribuicao['nivel_certeza'] >= 0.8,
            'needs_review': dados_contribuicao['nivel_certeza'] < 0.6,
            'data_quality': 'high' if dados_contribuicao['nivel_certeza'] >= 0.8 else ('medium' if dados_contribuicao['nivel_certeza'] >= 0.6 else 'low')
        }
        
        # Converter para DataFrame
        df_novo = pd.DataFrame([dados_ml])
        
        # Salvar (append se arquivo já existe)
        if csv_file.exists():
            # Ler dados existentes
            df_existente = pd.read_csv(csv_file)
            
            # Verificar se já existe classificação para este formulário pelo mesmo usuário
            filtro = (df_existente['forms_number'] == dados_ml['forms_number']) & \
                    (df_existente['classifier_name'] == dados_ml['classifier_name'])
            
            if filtro.any():
                # Atualizar registro existente
                df_existente.loc[filtro, df_novo.columns] = df_novo.iloc[0]
                df_final = df_existente
            else:
                # Adicionar novo registro
                df_final = pd.concat([df_existente, df_novo], ignore_index=True)
        else:
            df_final = df_novo
        
        # Salvar CSV com cabeçalho
        df_final.to_csv(csv_file, index=False, encoding='utf-8')
        
        # Salvar também em formato Parquet para ML (mais eficiente)
        parquet_file = output_dir / "training_ready.parquet"
        df_final.to_parquet(parquet_file, index=False)
        
        # Log de auditoria
        salvar_log_auditoria(dados_contribuicao, output_dir)
        
    except Exception as e:
        st.error(f"Erro ao salvar classificação: {e}")
        # Não interromper o fluxo por erro de salvamento

def salvar_log_auditoria(dados_contribuicao, output_dir):
    """Salva log de auditoria das classificações"""
    try:
        log_file = output_dir / "classification_sessions.json"
        
        # Carregar logs existentes
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        else:
            logs = {"sessions": [], "statistics": {}}
        
        # Adicionar entrada de log
        log_entry = {
            "timestamp": dados_contribuicao['timestamp'],
            "user": dados_contribuicao['usuario'],
            "forms_number": dados_contribuicao['forms_number'],
            "action": "classification",
            "type": dados_contribuicao.get('tipo_classificacao', 'manual'),
            "ai_category": dados_contribuicao.get('categoria_ia'),
            "human_category": dados_contribuicao['categoria_usuario'],
            "confidence": dados_contribuicao['nivel_certeza'],
            "approved_ai": dados_contribuicao.get('aprovou_ia', False)
        }
        
        logs["sessions"].append(log_entry)
        
        # Atualizar estatísticas
        user = dados_contribuicao['usuario']
        if user not in logs["statistics"]:
            logs["statistics"][user] = {
                "total_classifications": 0,
                "ai_approvals": 0,
                "manual_classifications": 0,
                "avg_confidence": 0.0,
                "last_activity": None
            }
        
        stats = logs["statistics"][user]
        stats["total_classifications"] += 1
        stats["last_activity"] = dados_contribuicao['timestamp']
        
        if dados_contribuicao.get('aprovou_ia', False):
            stats["ai_approvals"] += 1
        else:
            stats["manual_classifications"] += 1
        
        # Calcular confiança média (simplificado)
        total = stats["total_classifications"]
        current_avg = stats["avg_confidence"]
        new_confidence = dados_contribuicao['nivel_certeza']
        stats["avg_confidence"] = ((current_avg * (total - 1)) + new_confidence) / total
        
        # Salvar logs
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        # Log de auditoria é opcional, não deve quebrar o fluxo
        pass

def contar_contribuicoes_csv(usuario):
    """Conta contribuições salvas no CSV para um usuário específico"""
    try:
        csv_file = Path("data/human_labels/human_classifications.csv")
        if csv_file.exists():
            df = pd.read_csv(csv_file)
            return len(df[df['classifier_name'] == usuario])
        return 0
    except Exception:
        return 0

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

def obter_classificacao_ia(forms_number, df_classificacoes):
    """Obtém a classificação da IA para um formulário específico"""
    if df_classificacoes.empty:
        return None, None, None
    
    # Buscar classificação da IA
    classificacao = df_classificacoes[df_classificacoes['forms_number'] == forms_number]
    
    if classificacao.empty:
        return None, None, None
    
    row = classificacao.iloc[0]
    categoria_ia = row.get('level1_category', None)
    confianca = row.get('level1_confidence', 0)
    threshold_met = row.get('level1_threshold_met', False)
    
    # Se a categoria começa com "Nova_Classe", significa que a IA não conseguiu classificar
    if categoria_ia and str(categoria_ia).startswith('Nova_Classe'):
        return None, None, None
    
    return categoria_ia, confianca, threshold_met

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
        <p class="header-subtitle">Sistema de classificação humana com o intuito de re treinar o modelo de IA feito para similaridade do ROPA/RAT, objetivando uma maior acurácia do modelo.</p>
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
            
            # Botão sempre ativo
            if st.button("Começar Classificação", type="primary", use_container_width=True):
                if usuario and len(usuario.strip()) >= 2:
                    st.session_state.usuario = usuario.strip().title()
                    st.session_state.usuario_autenticado = True
                    st.rerun()
                elif not usuario or len(usuario.strip()) < 2:
                    st.error("Por favor, insira um nome com pelo menos 2 caracteres antes de começar.")
        
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
    
    # Carregar classificações da IA
    df_classificacoes = carregar_classificacoes_ia()
    
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
        # Contar contribuições do arquivo CSV (dados persistentes)
        contribuicoes_csv = contar_contribuicoes_csv(usuario)
        st.metric("Contribuições Salvas", f"{contribuicoes_csv:,}", help="Dados salvos permanentemente para retreinamento")
    
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
        
        # Mostrar estatísticas de retreinamento
        mostrar_estatisticas_retreinamento()
        
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
            # Obter classificação da IA
            categoria_ia, confianca_ia, threshold_met = obter_classificacao_ia(forms_number, df_classificacoes)
            
            if categoria_ia:
                # Mostrar sugestão da IA
                confianca_pct = confianca_ia * 100 if confianca_ia else 0
                cor_confianca = "#28a745" if threshold_met else "#ffc107"
                
                st.markdown(f"""
                <div class="card-white">
                    <h3>🤖 Sugestão da IA</h3>
                    <p><strong>Categoria:</strong> {categoria_ia}</p>
                    <p><strong>Confiança:</strong> <span style="color: {cor_confianca}; font-weight: bold;">{confianca_pct:.1f}%</span></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Opção de aprovar ou modificar
                col_aprovar, col_modificar = st.columns(2)
                
                with col_aprovar:
                    if st.button("✅ Aprovar IA", type="primary", use_container_width=True, key=f"aprovar_{forms_number}"):
                        # Auto-preencher com a sugestão da IA
                        st.session_state[f"aprovado_ia_{forms_number}"] = True
                        st.session_state[f"categoria_escolhida_{forms_number}"] = categoria_ia
                        st.rerun()
                
                with col_modificar:
                    if st.button("✏️ Modificar", use_container_width=True, key=f"modificar_{forms_number}"):
                        # Permitir modificação manual
                        st.session_state[f"aprovado_ia_{forms_number}"] = False
                        st.rerun()
                
                # Verificar se foi aprovado ou se vai modificar
                aprovado = st.session_state.get(f"aprovado_ia_{forms_number}", None)
                
                if aprovado is True:
                    # Mostrar aprovação
                    st.success(f"✅ Aprovado: **{categoria_ia}** (Confiança: {confianca_pct:.1f}%)")
                    categoria_selecionada = categoria_ia
                    mostrar_selecao_manual = False
                else:
                    mostrar_selecao_manual = True
            else:
                # Não há sugestão da IA
                st.markdown("""
                <div class="card-white">
                    <h3>🧠 Sua Classificação</h3>
                    <p><em>A IA não conseguiu classificar este formulário. Sua análise é essencial!</em></p>
                </div>
                """, unsafe_allow_html=True)
                mostrar_selecao_manual = True
            
            # Seleção manual (quando necessário)
            if mostrar_selecao_manual:
                st.markdown("### 📝 Classificação Manual")
                
                # Pré-selecionar categoria da IA se disponível
                categoria_default = None
                if categoria_ia and categoria_ia in CATEGORIAS.keys():
                    categoria_default = list(CATEGORIAS.keys()).index(categoria_ia)
                
                categoria_selecionada = st.selectbox(
                    "Categoria Principal:",
                    list(CATEGORIAS.keys()),
                    index=categoria_default,
                    key=f"categoria_{forms_number}",
                    help="Selecione a categoria que melhor descreve esta atividade"
                )
            
            # Definir categoria e subcategoria
            if 'categoria_selecionada' not in locals():
                categoria_selecionada = None
            
            if categoria_selecionada:
                if mostrar_selecao_manual:
                    subcategoria_selecionada = st.selectbox(
                        "Subcategoria:",
                        CATEGORIAS[categoria_selecionada],
                        key=f"subcategoria_{forms_number}",
                        help="Selecione a subcategoria específica"
                    )
                else:
                    # Se aprovado da IA, usar primeira subcategoria como padrão
                    subcategorias = CATEGORIAS.get(categoria_selecionada, [])
                    subcategoria_selecionada = subcategorias[0] if subcategorias else "Outros"
            else:
                subcategoria_selecionada = None
            
            # Nível de certeza e comentários (sempre mostrar)
            if mostrar_selecao_manual or st.session_state.get(f"aprovado_ia_{forms_number}") is not None:
                st.markdown("---")
                
                # Nível de certeza
                valor_inicial = confianca_ia if categoria_ia and st.session_state.get(f"aprovado_ia_{forms_number}") else 0.8
                certeza = st.slider(
                    "Seu nível de certeza:",
                    0.0, 1.0, valor_inicial, 0.1,
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
            else:
                certeza = 0.8
                comentarios = ""
        
        # Botão de salvar
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if categoria_selecionada and subcategoria_selecionada:
                if st.button("Salvar Classificação e Continuar", type="primary", use_container_width=True):
                    # Verificar se foi aprovação da IA ou classificação manual
                    aprovou_ia = st.session_state.get(f"aprovado_ia_{forms_number}") is True
                    
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
                        'comentarios': comentarios,
                        'categoria_ia': categoria_ia,
                        'confianca_ia': confianca_ia,
                        'aprovou_ia': aprovou_ia,
                        'tipo_classificacao': 'aprovacao_ia' if aprovou_ia else 'manual'
                    }
                    
                    # Salvar
                    salvar_contribuicao(contribuicao)
                    salvar_formulario_analisado(forms_number, usuario)
                    
                    # Limpar estados específicos do formulário
                    keys_to_remove = [
                        f"aprovado_ia_{forms_number}",
                        f"categoria_escolhida_{forms_number}",
                        f"categoria_{forms_number}",
                        f"subcategoria_{forms_number}",
                        f"certeza_{forms_number}",
                        f"comentarios_{forms_number}"
                    ]
                    for key in keys_to_remove:
                        if key in st.session_state:
                            del st.session_state[key]
                    
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

def mostrar_estatisticas_retreinamento():
    """Mostra estatísticas dos dados coletados para retreinamento"""
    try:
        csv_file = Path("data/human_labels/human_classifications.csv")
        if csv_file.exists():
            df = pd.read_csv(csv_file)
            
            st.subheader("📊 Estatísticas para Retreinamento")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Classificações", len(df))
            
            with col2:
                aprovacoes_ia = len(df[df['approved_ai'] == True])
                st.metric("Aprovações IA", aprovacoes_ia)
            
            with col3:
                alta_confianca = len(df[df['high_confidence'] == True])
                st.metric("Alta Confiança", alta_confianca)
            
            with col4:
                discordancias = len(df[df['disagreement_flag'] == True])
                st.metric("Discordâncias", discordancias)
            
            # Mostrar distribuição por categoria
            st.markdown("**Distribuição por Categoria:**")
            dist_categoria = df['human_category'].value_counts()
            st.bar_chart(dist_categoria)
    
    except Exception as e:
        st.info("Ainda não há dados de retreinamento salvos")

if __name__ == "__main__":
    main()
