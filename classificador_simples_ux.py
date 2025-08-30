#!/usr/bin/env python3
"""
Interface Streamlit UX/UI Otimizada para Classificação Manual
Design moderno, intuitivo e focado na experiência do usuário
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

# CSS customizado para melhor UX
st.markdown("""
<style>
    /* Header principal */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Cards de informação */
    .info-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #007bff;
        margin: 0.5rem 0;
    }
    
    .ai-card {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
    }
    
    .user-card {
        background: #f3e5f5;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #9c27b0;
    }
    
    /* Botões personalizados */
    .stButton > button {
        border-radius: 20px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    /* Métricas */
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    /* Progress bar customizada */
    .progress-bar {
        background: #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
        height: 8px;
        margin: 0.5rem 0;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #4caf50, #8bc34a);
        height: 100%;
        transition: width 0.3s ease;
    }
    
    /* Container de formulário */
    .form-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    /* Alertas customizados */
    .success-alert {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    .warning-alert {
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# CONFIGURAÇÕES DE DADOS
# ========================================

DATA_DIR = Path("data")
ASSIGNMENTS_FILE = DATA_DIR / "assigned" / "final_assignments.csv"
CONTRIBUTIONS_FILE = DATA_DIR / "human_labels" / "contribuicoes_usuarios.csv"
ANALYZED_FILE = DATA_DIR / "human_labels" / "formularios_analisados.json"

# Criar diretórios se não existirem
(DATA_DIR / "human_labels").mkdir(exist_ok=True)

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
    if ANALYZED_FILE.exists():
        with open(ANALYZED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def salvar_formulario_analisado(forms_number, usuario):
    """Salva formulário como analisado"""
    analisados = carregar_formularios_analisados()
    if str(forms_number) not in analisados:
        analisados[str(forms_number)] = []
    if usuario not in analisados[str(forms_number)]:
        analisados[str(forms_number)].append(usuario)
    
    with open(ANALYZED_FILE, 'w', encoding='utf-8') as f:
        json.dump(analisados, f, ensure_ascii=False, indent=2)

@st.cache_data
def carregar_dados():
    """Carrega dados dos formulários"""
    try:
        df = pd.read_csv(ASSIGNMENTS_FILE)
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        return pd.DataFrame()

def filtrar_formularios_nao_analisados(df, usuario):
    """Filtra formulários não analisados pelo usuário"""
    analisados = carregar_formularios_analisados()
    
    forms_analisados_usuario = []
    for forms_number, usuarios in analisados.items():
        if usuario in usuarios:
            forms_analisados_usuario.append(int(forms_number))
    
    if forms_analisados_usuario:
        return df[~df['forms_number'].isin(forms_analisados_usuario)]
    return df.copy()

def salvar_contribuicao(dados_contribuicao):
    """Salva contribuição incrementalmente"""
    df_contribuicao = pd.DataFrame([dados_contribuicao])
    
    if CONTRIBUTIONS_FILE.exists():
        df_existente = pd.read_csv(CONTRIBUTIONS_FILE)
        df_final = pd.concat([df_existente, df_contribuicao], ignore_index=True)
    else:
        df_final = df_contribuicao
    
    df_final.to_csv(CONTRIBUTIONS_FILE, index=False, encoding='utf-8')

def extrair_nome_atividade(forms_text):
    """Extrai nome da atividade de forma inteligente"""
    if pd.isna(forms_text) or not forms_text:
        return "📋 Sem nome definido"
    
    partes = str(forms_text).split(';')
    nome = partes[0].strip().lstrip(' .,;-')
    
    if len(nome) > 80:
        nome = nome[:77] + "..."
    
    return f"📋 {nome}" if nome else "📋 Sem nome definido"

def obter_confianca_visual(confidence):
    """Retorna representação visual da confiança"""
    if confidence >= 0.7:
        return "🟢 Alta", "#4caf50"
    elif confidence >= 0.5:
        return "🟡 Média", "#ff9800"
    else:
        return "🔴 Baixa", "#f44336"

# ========================================
# COMPONENTES UI
# ========================================

def render_header():
    """Renderiza header principal"""
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Classificador Manual Inteligente</h1>
        <p>Sistema otimizado para análise e classificação de formulários</p>
    </div>
    """, unsafe_allow_html=True)

def render_user_welcome(usuario):
    """Renderiza boas-vindas do usuário"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"""
        <div class="user-card">
            <h3>👋 Bem-vindo, {usuario}!</h3>
            <p>Vamos analisar alguns formulários juntos?</p>
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
    analisados = carregar_formularios_analisados()
    total_analisados = len([f for f, users in analisados.items() if usuario in users])
    
    if CONTRIBUTIONS_FILE.exists():
        df_contrib = pd.read_csv(CONTRIBUTIONS_FILE)
        contribuicoes_usuario = len(df_contrib[df_contrib['usuario'] == usuario]) if not df_contrib.empty else 0
    else:
        contribuicoes_usuario = 0
    
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
            help="Suas análises salvas no sistema"
        )
    
    # Barra de progresso visual
    if len(df_total) > 0:
        progresso_pct = (total_analisados / len(df_total)) * 100
        st.markdown(f"""
        <div style="margin: 1rem 0;">
            <p><strong>Seu Progresso:</strong> {progresso_pct:.1f}%</p>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progresso_pct}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_form_info(row, forms_text):
    """Renderiza informações do formulário de forma visual"""
    st.markdown("""
    <div class="form-container">
    """, unsafe_allow_html=True)
    
    # Header do formulário
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"### {extrair_nome_atividade(forms_text)}")
        st.markdown(f"**🆔 Formulário:** `{row['forms_number']}`")
    
    with col2:
        # Confiança da IA se disponível
        if pd.notna(row.get('combined_confidence', 0)) and row.get('combined_confidence', 0) > 0:
            conf_label, conf_color = obter_confianca_visual(row['combined_confidence'])
            st.markdown(f"""
            <div style="text-align: center; padding: 0.5rem; background: {conf_color}20; 
                        border-radius: 8px; border: 2px solid {conf_color};">
                <strong>Confiança IA</strong><br>
                {conf_label}<br>
                <span style="font-size: 1.2em; font-weight: bold;">{row['combined_confidence']:.1%}</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Descrição do formulário
    st.markdown("**📄 Descrição da Atividade:**")
    if forms_text:
        # Container scrollável para textos longos
        st.markdown(f"""
        <div style="max-height: 200px; overflow-y: auto; padding: 1rem; 
                    background: #f8f9fa; border-radius: 8px; border: 1px solid #dee2e6;">
            {forms_text.replace('\n', '<br>')}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Descrição não disponível")
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_ai_classification(row):
    """Renderiza classificação da IA de forma visual"""
    if pd.notna(row['final_category']) and row['final_category'] != 'Não Classificado':
        st.markdown("""
        <div class="ai-card">
            <h4>🤖 Classificação da Inteligência Artificial</h4>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Categoria:** {row['final_category']}")
        with col2:
            if pd.notna(row['final_subcategory']):
                st.write(f"**Subcategoria:** {row['final_subcategory']}")
        
        st.markdown("</div>", unsafe_allow_html=True)
        return True
    else:
        st.markdown("""
        <div class="warning-alert">
            <strong>⚠️ Formulário não classificado pela IA</strong><br>
            Este formulário precisa de classificação manual.
        </div>
        """, unsafe_allow_html=True)
        return False

def render_user_classification(row, forms_number):
    """Renderiza painel de classificação do usuário"""
    st.markdown("""
    <div class="user-card">
        <h4>👤 Sua Análise</h4>
    </div>
    """, unsafe_allow_html=True)
    
    tem_classificacao_ia = pd.notna(row['final_category']) and row['final_category'] != 'Não Classificado'
    
    # Decisão sobre a classificação IA
    if tem_classificacao_ia:
        st.markdown("**🤔 A classificação da IA está correta?**")
        aprovacao = st.radio(
            "Escolha uma opção:",
            ["✅ Aprovar classificação da IA", "❌ Classificar manualmente"],
            key=f"aprovacao_{forms_number}",
            horizontal=True
        )
        aprovacao_simplificada = "Aprovar" if "Aprovar" in aprovacao else "Reprovar"
    else:
        aprovacao_simplificada = "Reprovar"
        st.info("🔍 **Classificação manual obrigatória** - IA não conseguiu classificar")
    
    # Seleção de categoria
    categoria_selecionada = row['final_category'] if aprovacao_simplificada == "Aprovar" else None
    subcategoria_selecionada = row['final_subcategory'] if aprovacao_simplificada == "Aprovar" else None
    
    if aprovacao_simplificada == "Reprovar":
        st.markdown("**🏷️ Selecione a classificação correta:**")
        
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
    
    # Nível de certeza com visual melhorado
    st.markdown("**🎯 Qual seu nível de certeza nesta classificação?**")
    certeza = st.slider(
        "Nível de certeza",
        0.0, 1.0, 0.8, 0.1,
        key=f"certeza_{forms_number}",
        format="%.0f%%",
        help="0% = Totalmente incerto, 100% = Totalmente certo",
        label_visibility="collapsed"
    )
    
    # Visualização da certeza
    if certeza >= 0.8:
        certeza_cor = "#4caf50"
        certeza_texto = "🟢 Alta confiança"
    elif certeza >= 0.6:
        certeza_cor = "#ff9800"
        certeza_texto = "🟡 Confiança moderada"
    else:
        certeza_cor = "#f44336"
        certeza_texto = "🔴 Baixa confiança"
    
    st.markdown(f"""
    <div style="padding: 0.5rem; background: {certeza_cor}20; border-radius: 8px; 
                border-left: 4px solid {certeza_cor}; margin: 0.5rem 0;">
        <strong>{certeza_texto}</strong> - {certeza:.0%}
    </div>
    """, unsafe_allow_html=True)
    
    # Comentários opcionais
    comentarios = st.text_area(
        "💭 Comentários ou observações (opcional):",
        placeholder="Ex: 'Categoria óbvia pelo contexto' ou 'Difícil de classificar, poderia ser X ou Y'",
        key=f"comentarios_{forms_number}",
        help="Adicione observações que possam ajudar outros analistas"
    )
    
    return aprovacao_simplificada, categoria_selecionada, subcategoria_selecionada, certeza, comentarios

# ========================================
# FUNÇÃO PRINCIPAL
# ========================================

def main():
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
                if st.button("🚀 Começar Análise", type="primary", use_container_width=True):
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
        
        # Botão para carregar contribuições
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📤 Carregar Todas as Minhas Contribuições", type="primary", use_container_width=True):
                if CONTRIBUTIONS_FILE.exists():
                    df_contrib = pd.read_csv(CONTRIBUTIONS_FILE)
                    suas_contrib = df_contrib[df_contrib['usuario'] == usuario]
                    if not suas_contrib.empty:
                        st.success(f"✅ {len(suas_contrib)} contribuições carregadas com sucesso!")
                        st.dataframe(suas_contrib, use_container_width=True)
                    else:
                        st.info("ℹ️ Nenhuma contribuição encontrada")
                else:
                    st.info("ℹ️ Ainda não há contribuições no sistema")
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
        st.markdown(f"""
        <div style="text-align: center; padding: 0.5rem;">
            <strong>Formulário {progresso} de {total}</strong><br>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {(progresso/total)*100}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        ir_para = st.number_input("Navegar para formulário", min_value=1, max_value=len(df_disponivel), 
                                  value=st.session_state.indice_atual + 1, 
                                  key="nav_input", label_visibility="collapsed")
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
        
        # Obter texto completo
        forms_text = ""
        try:
            dados_raw = pd.read_csv(DATA_DIR / "raw" / "dados_embbeding.csv")
            match = dados_raw[dados_raw['forms_number'] == row['forms_number']]
            if not match.empty:
                forms_text = match.iloc[0]['forms_text']
        except Exception as e:
            st.warning(f"⚠️ Erro ao carregar texto do formulário: {e}")
        
        # Layout principal
        col_esquerda, col_direita = st.columns([1.2, 1])
        
        with col_esquerda:
            render_form_info(row, forms_text)
            render_ai_classification(row)
        
        with col_direita:
            aprovacao, categoria, subcategoria, certeza, comentarios = render_user_classification(row, row['forms_number'])
        
        # Botão de salvar
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if categoria and subcategoria:
                if st.button("💾 Salvar Análise e Continuar", type="primary", use_container_width=True):
                    # Preparar dados
                    contribuicao = {
                        'forms_number': row['forms_number'],
                        'forms_name': extrair_nome_atividade(forms_text).replace('📋 ', ''),
                        'descricao_atividade': forms_text,
                        'categoria_ia': row['final_category'] if pd.notna(row['final_category']) else 'Não Classificado',
                        'subcategoria_ia': row['final_subcategory'] if pd.notna(row['final_subcategory']) else 'Não Classificado',
                        'aprovacao_usuario': aprovacao,
                        'categoria_usuario': categoria.replace('🏢 ', '').replace('👥 ', '').replace('⚖️ ', '').replace('💻 ', '').replace('📚 ', '').replace('📈 ', '').replace('🔧 ', ''),
                        'subcategoria_usuario': subcategoria,
                        'nivel_certeza': certeza,
                        'usuario': usuario,
                        'timestamp': datetime.now().isoformat(),
                        'comentarios': comentarios
                    }
                    
                    # Salvar
                    salvar_contribuicao(contribuicao)
                    salvar_formulario_analisado(row['forms_number'], usuario)
                    
                    # Feedback visual
                    st.success("✅ Análise salva com sucesso!")
                    
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
