import pyodbc

class BaseModel:
    def __init__(self):
        self._conexao = self._conectar_bd()

    def _conectar_bd(self):
        """Método protegido para conectar ao banco de dados."""
        dados_conexao = (
            "Driver={SQL Server};"
            "Server=Bauer;"
            "Database=CP;"
        )
        return pyodbc.connect(dados_conexao)

    def _executar_comando(self, comando, parametros=None):
        """Método protegido para executar comandos SQL."""
        cursor = self._conexao.cursor()
        if parametros:
            cursor.execute(comando, parametros)
        else:
            cursor.execute(comando)
        return cursor

    def fechar_conexao(self):
        """Fecha a conexão com o banco de dados."""
        self._conexao.close()

class ProdutoModel(BaseModel):
    def inserir_prod(self, nome_prod, categ_prod, preco_prod, quant_prod, data_prod):
        """Insere um novo produto no banco de dados."""
        comando = """
        INSERT INTO produtos (nome_prod, categ_prod, preco_prod, quant_prod, data_prod)
        VALUES (?, ?, ?, ?, ?)
        """
        self._executar_comando(comando, (nome_prod, categ_prod, preco_prod, quant_prod, data_prod))
        self._conexao.commit()

    def obter_produtos(self):
        """Obtém todos os produtos do banco de dados."""
        comando = "SELECT nome_prod, categ_prod, preco_prod, quant_prod, data_prod FROM produtos"
        cursor = self._executar_comando(comando)
        rows = cursor.fetchall()
        cursor.close()
        produtos = [{'nome': row[0], 'categoria': row[1], 'preco': row[2], 'quantidade': row[3], 'data': row[4]} for row in rows]
        return produtos
