import json
from flask import Flask, render_template, request, redirect, url_for

ARQUIVO_DADOS = 'dados/dados.json'

# Carregar dados do arquivo JSON
def carregar_dados():
    with open(ARQUIVO_DADOS, 'r') as f:
        dados = json.load(f)
    return dados 

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

# Atualizar Pessoa
@app.route('/atualizar/<cpf>', methods=['GET', 'POST'])
def atualizar(cpf):
    dados = carregar_dados()
    pessoa = dados.get(cpf)
    if pessoa is None:
        pessoa = "Dados não encontrados."
    else:
        for p in dados:
            if dados[p] == cpf:
                pessoa = dados[p]
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
    if cpf in dados:
        del dados[cpf]
        salvar_dados(dados)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
    
# Buscar Pessoa por CPF
@app.route('/buscar', methods=['GET'])
def buscar():
    cpf = request.args.get('cpf', '')
    dados = carregar_dados()
    pessoa = dados.get(cpf)
    if pessoa is not None:
        dados = {cpf: pessoa}
    return render_template('index.html', pessoas=dados)

# Iniciar servidor
if __name__ == '__main__':
    app.run(debug=True)
