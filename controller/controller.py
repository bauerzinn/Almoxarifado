from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
from model.model import ProdutoModel
from view.view import ProdutoView

#Cada vez que o servidor HTTP recebe uma nova requisição, ele cria uma nova instância da classe ProdutoController
class ProdutoController(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.model = ProdutoModel()  #produto controller usa instancias de ProdutoModel e ProdutoView
        self.view = ProdutoView()  # assim eu posso usar métodos dessas classes
        super().__init__(*args, **kwargs)

    def do_GET(self):
        #com base nas rotas do path, dispara as funções de renderização das paginass
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
            #wfile é o canal de saída onde os dados da resposta são escritos.
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