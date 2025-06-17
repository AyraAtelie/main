# Guia de Deploy no PythonAnywhere

Este guia fornece instruções passo a passo para hospedar este projeto Flask no PythonAnywhere.

## Pré-requisitos

1. Uma conta no PythonAnywhere (https://www.pythonanywhere.com/)
2. Uma conta no GitHub (opcional, mas recomendado)
3. Seu projeto Flask configurado localmente

## Método 1: Deploy via GitHub

### 1. Preparação do Projeto

1. Certifique-se de que seu projeto está em um repositório GitHub
2. Adicione um arquivo `wsgi.py` na raiz do projeto com o seguinte conteúdo:

```python
from app import create_app

application = create_app()

if __name__ == '__main__':
    application.run()
```

### 2. Configuração para Repositório Privado

Se seu repositório for privado, você tem duas opções:

#### Opção A: Usando Chave SSH

1. No PythonAnywhere, abra um console Bash
2. Gere uma nova chave SSH:
```bash
ssh-keygen -t ed25519 -C "seu-email@exemplo.com"
```
3. Copie a chave pública:
```bash
cat ~/.ssh/id_ed25519.pub
```
4. No GitHub:
   - Vá para Settings > SSH and GPG keys
   - Clique em "New SSH key"
   - Cole a chave pública
   - Dê um título (ex: "PythonAnywhere")
   - Clique em "Add SSH key"

#### Opção B: Usando Token de Acesso Pessoal (PAT)

1. No GitHub:
   - Vá para Settings > Developer settings > Personal access tokens
   - Clique em "Generate new token"
   - Dê um nome ao token
   - Selecione os escopos: `repo` e `workflow`
   - Copie o token gerado

2. No PythonAnywhere:
   - Use o token na URL do clone:
   ```bash
   git clone https://SEU-TOKEN@github.com/seu-usuario/seu-repositorio.git
   ```

### 3. Configuração no PythonAnywhere

1. Faça login no PythonAnywhere
2. Vá para a seção "Web"
3. Clique em "Add a new web app"
4. Escolha "Flask" como framework
5. Selecione a versão do Python (recomendado Python 3.9 ou superior)

### 4. Configuração do Virtual Environment

1. No console do PythonAnywhere, execute:
```bash
mkvirtualenv --python=/usr/bin/python3.9 meu-projeto
pip install -r requirements.txt
```

### 5. Configuração do WSGI

1. No painel do PythonAnywhere, vá para a seção "Web"
2. Clique no link do arquivo WSGI
3. Substitua o conteúdo por:

```python
import sys
path = '/home/seu-usuario/meu-projeto'
if path not in sys.path:
    sys.path.append(path)

from app import create_app
application = create_app()
```

### 6. Configuração do Banco de Dados

1. No console do PythonAnywhere, execute:
```bash
cd meu-projeto
python3
>>> from app import create_app
>>> app = create_app()
>>> with app.app_context():
...     from models import db
...     db.create_all()
```

## Método 2: Deploy via Arquivo ZIP

### 1. Preparação do Projeto

1. Compacte seu projeto em um arquivo ZIP
2. Certifique-se de incluir todos os arquivos necessários:
   - app.py
   - models/
   - templates/
   - static/
   - requirements.txt
   - wsgi.py (criado conforme instruções acima)

### 2. Upload do Projeto

1. No PythonAnywhere, vá para a seção "Files"
2. Faça upload do arquivo ZIP
3. Extraia o arquivo ZIP no diretório desejado

### 3. Configuração do Ambiente

1. Siga os mesmos passos do Método 1, começando da seção "Configuração do Virtual Environment"

## Configurações Adicionais

### Configuração de Arquivos Estáticos

1. No painel do PythonAnywhere, vá para a seção "Web"
2. Em "Static files", adicione:
   - URL: /static/
   - Directory: /home/seu-usuario/meu-projeto/static

### Configuração de Variáveis de Ambiente

1. No arquivo WSGI, adicione:
```python
import os
os.environ['FLASK_ENV'] = 'production'
```

### Configuração de Segurança

1. Altere a chave secreta no arquivo app.py:
```python
app.secret_key = 'sua-nova-chave-secreta-segura'
```

## Solução de Problemas Comuns

1. **Erro 500**: Verifique os logs de erro no PythonAnywhere
2. **Problemas com banco de dados**: Certifique-se de que o banco de dados foi criado corretamente
3. **Arquivos estáticos não carregam**: Verifique as configurações de arquivos estáticos
4. **Problemas de permissão**: Verifique as permissões dos arquivos e diretórios
5. **Erro de acesso ao repositório privado**: 
   - Verifique se a chave SSH está corretamente configurada
   - Verifique se o token de acesso pessoal está válido
   - Certifique-se de que o usuário tem permissão para acessar o repositório

## Manutenção

1. Para atualizar o projeto via GitHub:
```bash
cd meu-projeto
git pull
pip install -r requirements.txt
```

2. Para reiniciar a aplicação:
   - Vá para a seção "Web" no PythonAnywhere
   - Clique em "Reload"

## Notas Importantes

1. O PythonAnywhere oferece um plano gratuito com limitações
2. Considere fazer backup regular do banco de dados
3. Mantenha suas dependências atualizadas
4. Monitore os logs regularmente
5. Para repositórios privados, mantenha suas chaves SSH e tokens de acesso seguros

## Suporte

Para mais ajuda, consulte:
- Documentação do PythonAnywhere: https://help.pythonanywhere.com/
- Documentação do Flask: https://flask.palletsprojects.com/
- Documentação do GitHub sobre SSH: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
- Documentação do GitHub sobre PAT: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token 