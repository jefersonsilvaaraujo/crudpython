import json
from flask import Flask, render_template, request, redirect, url_for

ARQUIVO_DADOS = 'dados/dados.json'

# Carregar dados do arquivo JSON
def carregar_dados():
    with open(ARQUIVO_DADOS, 'r') as f:
        return json.load(f)

# Salvar dados no arquivo JSON
def salvar_dados(dados):
    with open(ARQUIVO_DADOS, 'w') as f:
        json.dump(dados, f)

# Instanciar Flask
app = Flask(__name__)

# Rotas

# Página inicial
@app.route('/')
def index():
    dados = carregar_dados()
    return render_template('index.html', pessoas=dados)

# Criar Pessoa
@app.route('/criar', methods=['GET', 'POST'])
def criar():
    if request.method == 'POST':
        nova_pessoa = {
            "nome": request.form['nome'],
            "cpf": request.form['cpf'],
            "telefone": request.form['telefone'],
            "email": request.form['email'],
            "endereco": request.form['endereco'],
            "cep": request.form['cep'],
            "nascimento": request.form['nascimento'],
        }
        dados = carregar_dados()
        dados[nova_pessoa['cpf']] = nova_pessoa
        #dados.append(nova_pessoa)
        salvar_dados(dados)
        return redirect(url_for('index'))
    return render_template('criar.html')

# Buscar Pessoa por CPF
@app.route('/buscar/<cpf>')
def buscar(cpf):
    dados = carregar_dados()
    pessoa = None
    for p in dados:
        if p['cpf'] == cpf:
            pessoa = p
            break
    return render_template('ler.html', pessoa=pessoa)

# Atualizar Pessoa
@app.route('/atualizar/<cpf>', methods=['GET', 'POST'])
def atualizar(cpf):
    dados = carregar_dados()
    pessoa = None
    for p in dados:
        if p['cpf'] == cpf:
            pessoa = p
            break
    if request.method == 'POST':
        pessoa['nome'] = request.form['nome']
        pessoa['telefone'] = request.form['telefone']
        pessoa['email'] = request.form['email']
        pessoa['endereco'] = request.form['endereco']
        pessoa['cep'] = request.form['cep']
        pessoa['nascimento'] = request.form['nascimento']
        salvar_dados(dados)
        return redirect(url_for('index'))
    return render_template('atualizar.html', pessoa=pessoa)

# Excluir Pessoa
@app.route('/excluir/<cpf>')
def excluir(cpf):
    dados = carregar_dados()
    nova_lista = []
    for p in dados:
        if p['cpf'] != cpf:
            nova_lista.append(p)
    salvar_dados(nova_lista)
    return redirect(url_for('index'))

# Iniciar servidor
if __name__ == '__main__':
    app.run(debug=True)
