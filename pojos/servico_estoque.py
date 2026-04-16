from pojos.estoque import Estoque

class ServicoEstoque:
    def __init__(self):
        self.estoque = Estoque()

    def adicionar(self, nome_produto, quantidade):
        self.estoque.adicionar_produto(nome_produto, quantidade)

    def remover(self, nome_produto, quantidade):
        return self.estoque.remover_produto(nome_produto, quantidade)

    def listar(self):
        return self.estoque.listar()
