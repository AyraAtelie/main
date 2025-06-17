# teste
# =============================================
# IMPORTAÇÃO DE BIBLIOTECAS E EXTENSÕES
# =============================================
from flask_sqlalchemy import SQLAlchemy  # Extensão para integração com banco de dados SQLAlchemy

# =============================================
# INSTÂNCIA DO BANCO DE DADOS
# =============================================
db = SQLAlchemy()  # Cria a instância do banco de dados para ser usada nos modelos

# =============================================
# DEFINIÇÃO DE MODELOS DO BANCO DE DADOS
# =============================================

# =============================================
# MODELO ADMINISTRADOR
# =============================================
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    email = db.Column(db.String(120), nullable=False, unique=True)  # Email único
    senha = db.Column(db.String(120), nullable=False)  # Senha

# =============================================
# MODELO DE CONTEÚDO DA PÁGINA
# =============================================
class Conteudo(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    titulo_menu = db.Column(db.String(120))  # Título do menu
    texto_sobre = db.Column(db.Text)  # Texto "Sobre"
    sobre_mim = db.Column(db.Text)  # Seção "Sobre mim"
    religiao = db.Column(db.Text)  # Seção "Religião"
    trabalho = db.Column(db.Text)  # Seção "Trabalho"

# =============================================
# MODELO DA LOJA
# =============================================
class Loja(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    nome = db.Column(db.String(120), nullable=False)  # Nome do produto
    preco = db.Column(db.Float, nullable=False)  # Preço do produto
    descricao = db.Column(db.Text)  # Descrição do produto
    imagem = db.Column(db.String(255))  # Caminho da imagem do produto
    flagdestaque = db.Column(db.Boolean, default=False)  # Destaque do produto
