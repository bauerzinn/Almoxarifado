from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
from model.model import ProdutoModel
from view.view import ProdutoView

class ProdutoController(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.model = ProdutoModel()
        self.view = ProdutoView()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.view.renderpaginainicial())
        elif self.path == '/cadastro':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.view.renderformulariocadastro())
        elif self.path == '/lista':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            produtos = self.model.obter_produtos()
            self.wfile.write(self.view.render_lista_produtos(produtos))

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
            self.model.inserir_prod(nome, categoria, preco, quantidade, data)
            self.send_response(302)
            self.send_header('Location', '/lista')
            self.end_headers()

    def finish(self):
        self.model.fechar_conexao()
        super().finish()