# Importações
from flask import Flask, render_template, request, redirect, url_for
import json

# Carregar dados do arquivo JSON
with open('dados.json', 'r') as f:
    dados = json.load(f)

# Instanciar Flask
app = Flask(__name__)

# Rotas

# Página inicial
@app.route('/')
def index():
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
            "endereço": request.form['endereço'],
            "cep": request.form['cep'],
            "nascimento": request.form['nascimento'],
        }
        dados.append(nova_pessoa)
        _salvar_dados()
        return redirect(url_for('index'))
    return render_template('criar.html')

# Ler Pessoa
@app.route('/ler/<int:id>')
def ler(id):
    pessoa = dados[id]
    return render_template('ler.html', pessoa=pessoa)

# Atualizar Pessoa
@app.route('/atualizar/<int:id>', methods=['GET', 'POST'])
def atualizar(id):
    pessoa = dados[id]
    if request.method == 'POST':
        pessoa['nome'] = request.form['nome']
        pessoa['cpf'] = request.form['cpf']
        pessoa['telefone'] = request.form['telefone']
        pessoa['email'] = request.form['email']
        pessoa['endereço'] = request.form['endereço']
        pessoa['cep'] = request.form['cep']
        pessoa['nascimento'] = request.form['nascimento']
        _salvar_dados()
        return redirect(url_for('index'))
    return render_template('atualizar.html', pessoa=pessoa)

# Excluir Pessoa
@app.route('/excluir/<int:id>')
def excluir(id):
    del dados[id]
    _salvar_dados()
    return redirect(url_for('index'))

# Salvar dados no arquivo JSON
def _salvar_dados():
    with open('dados.json', 'w') as f:
        json.dump(dados, f)

# Iniciar servidor
if __name__ == '__main__':
    app.run(debug=True)
