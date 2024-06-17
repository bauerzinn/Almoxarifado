import pyodbc

class ProdutoModel:
    def __init__(self):
        self.conexao = self.conectar_bd()

    def conectar_bd(self):
        dados_conexao = (
            "Driver={SQL Server};"
            "Server=Bauer;"
            "Database=CP;"
        )
        return pyodbc.connect(dados_conexao)

    def inserir_prod(self, nome_prod, categ_prod, preco_prod, quant_prod, data_prod):
        cursor = self.conexao.cursor()
        comando = """
        INSERT INTO produtos (nome_prod, categ_prod, preco_prod, quant_prod, data_prod)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(comando, (nome_prod, categ_prod, preco_prod, quant_prod, data_prod))
        self.conexao.commit()
        cursor.close()

    def obter_produtos(self):
        cursor = self.conexao.cursor()
        comando = "SELECT nome_prod, categ_prod, preco_prod, quant_prod, data_prod FROM produtos"
        cursor.execute(comando)
        rows = cursor.fetchall()
        cursor.close()
        produtos = [{'nome': row[0], 'categoria': row[1], 'preco': row[2], 'quantidade': row[3], 'data': row[4]} for row in rows]
        return produtos

    def fechar_conexao(self):
        self.conexao.close()