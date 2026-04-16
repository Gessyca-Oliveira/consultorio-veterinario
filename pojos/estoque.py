class Estoque:
    def __init__(self):
        self.produtos = {}

    def adicionar_produto(self, nome_produto, quantidade):
        if nome_produto not in self.produtos:
            self.produtos[nome_produto] = 0
        self.produtos[nome_produto] += quantidade

    def remover_produto(self, nome_produto, quantidade):
        if nome_produto not in self.produtos:
            return False
        if self.produtos[nome_produto] < quantidade:
            return False
        self.produtos[nome_produto] -= quantidade
        return True

    def listar(self):
        return self.produtos
