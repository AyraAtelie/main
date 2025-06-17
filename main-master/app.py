# teste
# =============================================
# IMPORTAÇÃO DE BIBLIOTECAS
# =============================================
from flask import Flask, redirect, url_for, render_template, request, session, flash  # Flask e funções para web
from models import db, Admin, Conteudo, Loja  # Modelos para banco de dados
import os  # Módulo do sistema operacional
from werkzeug.utils import secure_filename  # Utilitário para nomes de arquivos seguros

# =============================================
# CONFIGURAÇÕES GLOBAIS
# =============================================
UPLOAD_FOLDER = 'static/img'  # Pasta para upload de imagens

# =============================================
# FUNÇÃO PRINCIPAL DA APLICAÇÃO
# =============================================
def create_app():
    app = Flask(__name__)  # Inicializa a aplicação Flask

    # =============================================
    # CONFIGURAÇÃO DO BANCO DE DADOS
    # =============================================
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Diretório base do projeto
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "instance", "admin.db")}'  # Caminho do banco SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desativa rastreamento para melhor desempenho
    app.secret_key = 'minha-chave-secreta'  # Chave secreta para sessões

    db.init_app(app)  # Inicializa a extensão SQLAlchemy

    # =============================================
    # ROTAS PÚBLICAS
    # =============================================
    @app.route('/')
    def menu():
        produtos_destaque = Loja.query.filter_by(flagdestaque=True).all()  # Busca produtos em destaque
        conteudo = Conteudo.query.first()  # Busca conteúdo principal
        return render_template('index.html', produtos_destaque=produtos_destaque, conteudo=conteudo)  # Renderiza página inicial

    @app.route('/admin/editar_produto/<int:id>', methods=['GET', 'POST'])
    def editar_produtoDoMenu(id):
        produto = Loja.query.get_or_404(id)  # Busca produto por ID ou erro 404
        if request.method == 'POST':
            produto.nome = request.form['nome']  # Atualiza nome
            produto.descricao = request.form['descricao']  # Atualiza descrição
            produto.preco = float(request.form['preco'])  # Atualiza preço
            db.session.commit()  # Salva alterações
            flash('Produto atualizado com sucesso!')  # Mensagem de sucesso
            return redirect(url_for('menu_admin'))  # Redireciona para menu admin
        return render_template('editar_produto.html', produto=produto)  # Renderiza página de edição

    @app.route('/loja')
    def loja():
        produtos = Loja.query.all()  # Busca todos os produtos
        return render_template('loja.html', produtos=produtos)  # Renderiza página da loja

    @app.route('/contato')
    def contato():
        return render_template('contato.html')  # Renderiza página de contato

    @app.route('/cadastro')
    def cadastro():
        return render_template('cadastro.html')  # Renderiza página de cadastro

    @app.route('/login')
    def login():
        return render_template('login.html')  # Renderiza página de login

    @app.route('/sucesso-cadastro')
    def sucesso_cadastro():
        return render_template('sucesso-cadastro.html')  # Renderiza página de sucesso cadastro

    @app.route('/sucesso')
    def sucesso():
        return render_template('sucesso.html')  # Renderiza página de sucesso

    # =============================================
    # ROTAS ADMINISTRATIVAS
    # =============================================
    @app.route('/menu_admin', methods=['GET', 'POST'])
    def menu_admin():
        if not session.get('logado'):
            flash("Usuário não encontrado na área administrativa!")  # Mensagem de erro
            return redirect(url_for('login'))  # Redireciona para login
        
        produtos = Loja.query.all()  # Busca produtos
        conteudo = Conteudo.query.first()  # Busca conteúdo

        if conteudo is None:
            conteudo = Conteudo(titulo_menu="", texto_sobre="", sobre_mim="", religiao="", trabalho="")  # Conteúdo padrão
            db.session.add(conteudo)
            db.session.commit()

        if request.method == 'POST':
            conteudo.titulo_menu = request.form['titulo_menu']
            conteudo.texto_sobre = request.form['texto_sobre']
            conteudo.sobre_mim = request.form['sobre_mim']          
            conteudo.religiao = request.form['religiao']            
            conteudo.trabalho = request.form['trabalho']            
            db.session.commit()
            flash("Conteúdo atualizado com sucesso!")  # Mensagem de sucesso
            return redirect(url_for('menu_admin'))

        return render_template('menu_admin.html', produtos=produtos, conteudo=conteudo)  # Renderiza admin menu

    @app.route('/loja_admin', methods=['GET', 'POST'])
    def loja_admin():
        if not session.get('logado'):
            flash("Acesso restrito. Faça login.")  # Mensagem de erro
            return redirect(url_for('login'))

        if request.method == 'POST':
            nome = request.form.get('nome')  # Nome do produto
            preco = request.form.get('preco')  # Preço
            descricao = request.form.get('descricao_do_produto')  # Descrição
            imagem = request.files.get('img')  # Imagem
            flagdestaque = True if 'dest' in request.form else False  # Destaque

            if imagem and imagem.filename != '':
                filename = secure_filename(imagem.filename)  # Nome seguro
                caminho_imagem = os.path.join(UPLOAD_FOLDER, filename)  # Caminho
                imagem.save(caminho_imagem)  # Salva a imagem
                caminho_para_salvar = f'img/{filename}'
            else:
                caminho_para_salvar = 'img/produto_padrao.jpg'  # Imagem padrão

            novo_produto = Loja(nome=nome, preco=preco, descricao=descricao, imagem=caminho_para_salvar, flagdestaque=flagdestaque)
            db.session.add(novo_produto)
            db.session.commit()
            flash("Produto adicionado com sucesso!")
            return redirect(url_for('loja_admin'))

        produtos = Loja.query.all()  # Busca produtos
        return render_template('loja_admin.html', produtos=produtos)  # Renderiza loja admin

    @app.route('/admin')
    def admin():
        if not session.get('logado'):
            flash("Usuário não encontrado na área administrativa!")
            return redirect(url_for('login'))
        return render_template('admin.html')  # Renderiza página admin

    @app.route('/logout')
    def logout():
        session.clear()  # Limpa sessão
        return redirect(url_for('menu'))  # Redireciona para menu

    @app.route('/index_tab')
    def indextab():
        return render_template('index_tabs.html')  # Renderiza index tabs

    @app.route('/enviar-contato', methods=['POST'])
    def enviar_contato():
        nome = request.form.get('nome')  # Nome do usuário
        return redirect(url_for('sucesso', nome=nome))  # Redireciona

    @app.route('/enviar-cadastro', methods=['POST'])
    def enviar_cadastro():
        email = request.form['email']
        senha = request.form['senha']
        novo_admin = Admin(email=email, senha=senha)
        db.session.add(novo_admin)
        db.session.commit()
        return redirect(url_for('sucesso_cadastro'))  # Redireciona para sucesso cadastro

    @app.route('/enviar-login', methods=['POST'])
    def enviar_login():
        email = request.form['email-login']
        senha = request.form['senha']
        usuario = Admin.query.filter_by(email=email, senha=senha).first()
        if usuario:
            session['logado'] = True  # Usuário logado
            return redirect(url_for('admin'))
        else:
            flash('Login inválido.')  # Mensagem de erro
            return redirect(url_for('login'))

    @app.route('/editar-produto/<int:id>', methods=['POST'])
    def editar_produto(id):
        if not session.get('logado'):
            flash("Acesso restrito.")
            return redirect(url_for('login'))
        produto = Loja.query.get_or_404(id)
        produto.nome = request.form['nome']
        produto.preco = float(request.form['preco'])
        produto.descricao = request.form['descricao']
        db.session.commit()
        flash('Produto atualizado com sucesso!')
        return redirect(url_for('loja_admin'))

    @app.route('/deletar-produto/<int:id>', methods=['POST'])
    def deletar_produto(id):
        if not session.get('logado'):
            flash("Acesso restrito.")
            return redirect(url_for('login'))
        produto = Loja.query.get_or_404(id)
        db.session.delete(produto)
        db.session.commit()
        flash(f"Produto '{produto.nome}' excluído com sucesso!")
        return redirect(url_for('loja_admin'))

    return app  # Retorna a app

if __name__ == '__main__':
    app = create_app()  # Cria app
    with app.app_context():
        db.create_all()  # Cria tabelas
    app.run(debug=True, port=3000)  # Executa app
