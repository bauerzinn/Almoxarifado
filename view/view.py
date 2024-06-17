import os
class ProdutoView:
    @staticmethod
    def renderpaginainicial():
        caminho_arquivo = os.path.join(os.path.dirname(__file__), 'Home.html')
        with open(caminho_arquivo, 'rb') as file:
            return file.read()
        
    @staticmethod
    def renderformulariocadastro():
        caminho_arquivo = os.path.join(os.path.dirname(__file__), 'Cadprod.html')
        with open(caminho_arquivo, 'rb') as file:
            return file.read()
    @staticmethod
    def render_lista_produtos(produtos):
        response = '''<html>
<head>
    <title>Lista de Produtos</title>
    <style>
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #476bb5, #1f304f); margin: 0; padding: 0; }
        .container { width: 80%; margin: 0 auto; padding-top: 50px; }
        h1 { text-align: center; color: #000000; }
        ul { list-style-type: none; padding: 0; }
        .produto { background-color: #ffffff; padding: 20px; margin-bottom: 10px; border-radius: 5px; }
        .produto li { margin-bottom: 5px; }
        .produto span { font-weight: bold; }
        a { color: #154a82; text-decoration: none; margin-right: 20px; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Lista de Produtos</h1>
        <ul>
'''
        for produto in produtos:
            response += f'<li>{produto["nome"]} - {produto["categoria"]} - R$ {produto["preco"]} - Quantidade: {produto["quantidade"]} - Data: {produto["data"]}</li>'
        response += '''
        </ul><a href="/">Voltar</a></div></body></html>'''
        return response.encode('utf-8')