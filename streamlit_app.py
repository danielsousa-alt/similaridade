#!/usr/bin/env python3
"""
Arquivo principal para deploy no Streamlit Cloud
Este arquivo deve estar na raiz do repositório
"""

# Importar a aplicação principal
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.append(str(Path(__file__).parent / "src"))

# Importar e executar a aplicação
from src.web.classificador_simples import main

if __name__ == "__main__":
    main()
