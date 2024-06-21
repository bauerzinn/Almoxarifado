import os

# Classe base que utiliza encapsulamento para proteger métodos e atributos
class BaseView:
    def __init__(self):
        self._base_path = os.path.dirname(__file__)  # Atributo protegido

    def _render_file(self, filename):  # Método protegido
        """Renderiza o conteúdo de um arquivo HTML."""
        caminho_arquivo = os.path.join(self._base_path, filename)
        with open(caminho_arquivo, 'rb') as file:
            return file.read()

# Classe que herda de BaseView
class ProdutoView(BaseView):
    @staticmethod
    def renderpaginainicial():
        """Renderiza a página inicial."""
        return ProdutoView()._render_file('Home.html')
        
    @staticmethod
    def renderformulariocadastro():
        """Renderiza o formulário de cadastro."""
        return ProdutoView()._render_file('Cadprod.html')

    @staticmethod
    def render_lista_produtos(produtos):
        """Renderiza uma lista de produtos em formato HTML."""
        response = '''<html>
<head>
    <title>Lista de Produtos</title>
    <style>
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #476bb5, #1f304f); margin: 0; padding: 0; }
        .container { width: 80%; margin: 0 auto; padding-top: 50px; }
        h1 { text-align: center; color: #000000; }
        table { width: 100%; border-collapse: collapse; background-color: #ffffff; border-radius: 5px; overflow: hidden; }
        th, td { padding: 15px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #154a82; color: white; }
        tr:hover { background-color: #f1f1f1; }
        a { color: #ffffff;; text-decoration: none; margin-right: 20px; }
        a:hover { text-decoration: underline; }

    </style>
</head>
<body>
    <div class="container">
        <h1>Lista de Produtos</h1>
        <table>
            <thead>
                <tr>
                    <th>Nome</th>
                    <th>Categoria</th>
                    <th>Preço</th>
                    <th>Quantidade</th>
                    <th>Data</th>
                </tr>
            </thead>
            <tbody>
        </ul><a href="/">Voltar</a></div></body></html>

'''

        for produto in produtos:
            response += f'''
                <tr>
                    <td>{produto["nome"]}</td>
                    <td>{produto["categoria"]}</td>
                    <td>R$ {produto["preco"]}</td>
                    <td>{produto["quantidade"]}</td>
                    <td>{produto["data"]}</td>
                </tr>
            </tbody>
            '''
        return response.encode('utf-8')
