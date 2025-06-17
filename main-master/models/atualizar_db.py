# =============================================
# IMPORTAÇÃO DE BIBLIOTECAS
# =============================================
import sys  # Biblioteca de sistema para manipulação de caminhos
import os  # Biblioteca OS para operações de sistema de arquivos

# =============================================
# AJUSTE DO PATH PARA IMPORTAÇÕES
# =============================================
# Adiciona o diretório pai ao sys.path para garantir que a importação funcione
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# =============================================
# IMPORTAÇÃO DA APLICAÇÃO E MODELOS
# =============================================
from app import create_app  # Função que cria a aplicação Flask
from models import db, Conteudo  # Banco de dados e modelo Conteudo

# =============================================
# CRIAÇÃO DO APP
# =============================================
app = create_app()  # Inicializa a aplicação

# =============================================
# CONTEXTO DA APLICAÇÃO
# =============================================
with app.app_context():
    db.create_all()  # Cria todas as tabelas no banco de dados

    # =============================================
    # VERIFICA SE JÁ EXISTE CONTEÚDO CADASTRADO
    # =============================================
    if not Conteudo.query.first():
        conteudo_inicial = Conteudo(
            titulo_menu="Bem-vindo ao site!",
            texto_sobre="Este é o conteúdo inicial da seção sobre."
        )
        db.session.add(conteudo_inicial)  # Adiciona o conteúdo inicial
        db.session.commit()  # Salva as alterações

    print("Banco de dados atualizado com sucesso.")  # Mensagem de sucesso
