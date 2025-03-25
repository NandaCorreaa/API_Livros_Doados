# Importamos a classe Flask do módulo flask para criar nossa aplicação web
from flask import Flask, request , jsonify

import sqlite3

# Criamos uma instância do Flask e armazenamos na variável "app"
# O parâmetro _name_ indica que este arquivo será reconhecido como a aplicação principal
app = Flask(__name__)

# Criamos uma rota para o endpoint "/pague"
# Quando acessarmos http://127.0.0.1:5000/pague, a função abaixo será executada


@app.route("/")
def exiba_mensagem():
    # Retorna um texto formatado em HTML que será exibido no navegador ao acessar a rota "/pague"
    return "<h2>CRIANDO A API DO LIVROS VAI NA WEB</h2>"

def init_db():
    # sqlite3 crie o arquivo database.db e se conecte com a variável conn(connection)
    # a variável conn é responsavel pela comunicação do nosso código python com o banco de dados
    with sqlite3.connect("database.db") as conn:
        # IF NOT EXISTS - Crie a tabela livros se a tabela não existir. Pois toda hora que rodarmos o nosso código, ia dar um erro pois ele ia querer criar uma tabela que já existe
        conn.execute(""" 
            CREATE TABLE IF NOT EXISTS LIVROS( 
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     titulo TEXT NOT NULL,
                     categoria TEXT NOT NULL,
                     autor TEXT NOT NULL,
                     imagem_url TEXT NOT NULL
                     )
        """)

init_db()

# Quando apertarmos para enviar lá no form do site, precisamos ter um lugar para guardar. Esse lugar será a rota '/doar'
# O método post serve para enviar os dados pelo lado do cliente.
@app.route("/doar", methods = ['POST'])
def doar():
    # request é uma funcionalidade do flask própria para receber os dados do lado do cliente.
    # .get_json() é uma funcionalidade para receber os dados no formato json e guardar na variável dados
    dados = request.get_json()

#   a variável está puxando da varíavel 'dados' a informação que recebeu
    titulo = dados.get('titulo')
    categoria = dados.get('categoria')
    autor = dados.get('autor')
    imagem_url = dados.get('imagem_url')

    if not titulo or not categoria or not autor or not imagem_url:
        return jsonify({'erro':'Todos os campos são obrigatórios'}), 400

    with sqlite3.connect('database.db') as conn:
        conn.execute(f'''
        INSERT INTO LIVROS (titulo, categoria, autor, imagem_url) 
        VALUES("{titulo}","{categoria}","{autor}","{imagem_url}")
''')
        conn.commit()

        return jsonify({'mensagem':'Livro Cadastrado com Sucesso'}), 201
    
# Rota para 'puxar' os livros - methods=[GET] método para puxar os dados
@app.route('/livros', methods=['GET'])
def listar_livros():
    with sqlite3.connect('database.db') as conn:
        livros = conn.execute('SELECT * FROM LIVROS').fetchall()
        # Guarde todos os livros na variável 'livros' e traduza para python usando o fetchall(). Estamos traduzindo pois o python não entende o SQL.
        livros_formatados = []

        for item in livros:
            dicionario_livros = {
                'id': item[0],
                'titulo': item[1],
                'categoria': item[2],
                'autor': item[3],
                'imagem_url': item[4]
            }
        
            livros_formatados.append(dicionario_livros)

    return jsonify(livros_formatados)

# Aqui verificamos se o script está sendo executado diretamente e não importado como módulo
if __name__ == "__main__":
    # Inicia o servidor Flask no modo de depuração
    # O modo debug permite que mudanças no código sejam aplicadas automaticamente sem reiniciar o servidor manualmente
    app.run(debug=True)