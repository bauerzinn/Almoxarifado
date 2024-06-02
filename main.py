import pyodbc
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse

# A classe ProdutoModel é responsável pela interação com o banco de dados
class ProdutoModel:
    @staticmethod
    def conectar_bd():
        dados_conexao = (
            "Driver={SQL Server};"
            "Server=Bauer;"
            "Database=CP;"
        )
        conexao = pyodbc.connect(dados_conexao)
        return conexao

    @staticmethod
    def inserir_prod(nome_prod, categ_prod, preco_prod, quant_prod, data_prod):
        conexao = ProdutoModel.conectar_bd()
        cursor = conexao.cursor()
        comando = """
        INSERT INTO produtos (nome_prod, categ_prod, preco_prod, quant_prod, data_prod)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(comando, (nome_prod, categ_prod, preco_prod, quant_prod, data_prod))
        cursor.commit()
        cursor.close()
        conexao.close()

    @staticmethod
    def obter_produtos():
        conexao = ProdutoModel.conectar_bd()
        cursor = conexao.cursor()
        comando = "SELECT nome_prod, categ_prod, preco_prod, quant_prod, data_prod FROM produtos"
        cursor.execute(comando)
        rows = cursor.fetchall()
        cursor.close()
        conexao.close()
        produtos = [{'nome': row[0], 'categoria': row[1], 'preco': row[2], 'quantidade': row[3], 'data': row[4]} for row in rows]
        return produtos


# A classe ProdutoView é responsável por gerar o HTML das páginas web
class ProdutoView:
    @staticmethod
    # render_pagina_inicial: Retorna o HTML da página inicial.
    def render_pagina_inicial():
        return b'''
            <html>
            <head>
            <title>Almoxarifado</title>
            <style>
                body {
                background: linear-gradient(135deg, #476bb5, #1f304f);
                display: flex;
                font-family: Poppins;
                align-items: center;
                justify-content: center;
                min-height: 100vh;

                border: 0;
                }

                h1 {
                    text-align: center;
                    color: #000000;
                }
                a {
                    margin-top: 3px;
                    color: #2886eb;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }
                .container {
                background-color: #ffffff;
                border-radius: 10px;
                border: 2px solid #3E445B;
                width: 450px;
                max-width: 100%;
                box-shadow: 5px 5px 8px rgba(0, 0, 0, 0.336);
                padding: 0px 0px 20px;

                display: flex;
                flex-direction: column; /* Para garantir que os links fiquem empilhados verticalmente */
                align-items: center; /* Centralizar os links verticalmente */
                }
            </style>
            </head>
            <body>
            <div class="container">
            <h1>Almoxarifado</h1>
            <a href="/cadastro">Cadastrar Novo Produto</a><br>
            <a href="/lista">Lista de Produtos</a>
            </div>
            </body>
            </html>
        '''
    @staticmethod
    # HTML do formulário de cadastro de produto.
    def render_formulario_cadastro():
        return '''
            <html>
            <head>
            <title>Cadastro de Produto</title>
            <style>
            body {
                background: linear-gradient(135deg, #476bb5, #1f304f);
                font-family: Poppins;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                margin: 0;
                padding: 0;
            }
            .container {
                background-color: #ffffff;
                border-radius: 10px;
                border: 2px solid #3E445B;
                width: 80%;
                max-width: 450px;
                box-shadow: 5px 5px 8px rgba(0, 0, 0, 0.336);
                padding: 20px;
            }
            h1 {
                text-align: center;
                color: #000000;
                margin-bottom: 20px;
            }
            form {
                background-color: #ffffff;
                padding: 20px;
                border-radius: 5px;
            }
            input[type="text"] {
                width: 100%;
                padding: 10px;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            input[type="submit"] {
                width: 100%;
                padding: 10px;
                border: none;
                border-radius: 5px;
                background-color: #007bff;
                color: #fff;
                cursor: pointer;
            }
            input[type="submit"]:hover {
                background-color: #0056b3;
            }
            a {
                color: #154a82;
                text-decoration: none;
                margin-right: 20px;
            }
            a:hover {
                text-decoration: underline;
            }
            </style>
            </head>
            <body>
            <div class="container">
            <h1>Cadastro de Produto</h1>
            <form action="/cadastro" method="post">
                Nome: <input type="text" name="nome"><br>
                Categoria: <input type="text" name="categoria"><br>
                Valor: <input type="text" name="preco"><br>
                Quantidade: <input type="text" name="quantidade"><br>
                Data: <input type="text" name="data"><br>
                <input type="submit" value="Cadastrar">
            </form>
            <a href="/">Voltar</a>
            </div>
            </body>
            </html>

        '''.encode('utf-8')

    @staticmethod
    # Gera a lista de produtos em HTML.
    def render_lista_produtos(produtos):
        response = '''<html>
    <head>
        <title>Lista de Produtos</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #476bb5, #1f304f);
                margin: 0;
                padding: 0;
            }

            .container {
                width: 80%;
                margin: 0 auto;
                padding-top: 50px;

            }

            h1 {
                text-align: center;
                color: #000000;
            }

            ul {
                list-style-type: none;
                padding: 0;
                
                
            }

            .produto {
                background-color: #ffffff;
                padding: 20px;
                margin-bottom: 10px;
                border-radius: 5px;
            }

            .produto li {
                margin-bottom: 5px;
            }

            .produto span {
                font-weight: bold;
            }
        </style>
    </head>

<body>
    <div class="container">
        <h1>Lista de Produtos</h1>
        <ul>
'''
        for produto in produtos:
            response += f'<li>{produto["nome"]} - {produto["categoria"]} - R$ {produto["preco"]} - Quantidade: {produto["quantidade"]} - Data: {produto["data"]}</li>'
        response += '</ul><a href="/">Voltar</a></div></body></html>'
        return response.encode('utf-8')


# A classe ProdutoController herda de BaseHTTPRequestHandler, que é uma classe base da biblioteca http.server de Python para tratar requisições HTTP.

class ProdutoController(BaseHTTPRequestHandler):
    # O método do_GET é invocado sempre que o servidor recebe uma requisição GET.
    # O código verifica o caminho (self.path) para determinar qual conteúdo deve ser retornado ao usuário.
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(ProdutoView.render_pagina_inicial())
        elif self.path == '/cadastro':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(ProdutoView.render_formulario_cadastro())
        elif self.path == '/lista':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            produtos = ProdutoModel.obter_produtos()
            self.wfile.write(ProdutoView.render_lista_produtos(produtos))
        

    #O método do_POST é invocado quando o servidor recebe uma requisição POST, geralmente enviada quando um formulário é submetido.
    def do_POST(self):
        if self.path == '/cadastro':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = urlparse.parse_qs(post_data.decode())
            nome = post_data['nome'][0]
            categoria = post_data['categoria'][0]
            preco = float(post_data['preco'][0])
            quantidade = int(post_data['quantidade'][0])
            data = post_data['data'][0]
            ProdutoModel.inserir_prod(nome, categoria, preco, quantidade, data)
            self.send_response(302)
            self.send_header('Location', '/lista')
            self.end_headers()



def run(server_class=HTTPServer, handler_class=ProdutoController, port=8001):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Servindo na porta {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
    
#http://127.0.0.1:8001
