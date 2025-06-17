# =============================================
# IMPORTAÇÃO DE BIBLIOTECAS
# =============================================
from models import db  # Banco de dados
from app import create_app  # Função para criar a aplicação Flask

# =============================================
# CRIAÇÃO DO APP
# =============================================
app = create_app()  # Inicializa a aplicação

# =============================================
# CONTEXTO DA APLICAÇÃO
# =============================================
with app.app_context():
    db.create_all()  # Cria todas as tabelas no banco de dados
    print("Banco de dados criado com sucesso!")  # Mensagem de sucesso
