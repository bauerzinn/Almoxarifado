from http.server import HTTPServer
from controller.controller import ProdutoController

def run(server_class=HTTPServer, handler_class=ProdutoController, port=8001):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Servindo na porta {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
#http://127.0.0.1:8001