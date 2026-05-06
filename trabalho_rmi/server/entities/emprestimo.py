from datetime import datetime

class Emprestimo:
    """Entidade de empréstimo (agregação com Usuario e Livro)"""
    def __init__(self, id: int, usuario, livro):
        self.id = id
        self.usuario = usuario  # Agregação: Emprestimo TEM-UM Usuario
        self.livro = livro      # Agregação: Emprestimo TEM-UM Livro
        self.data_emprestimo = datetime.now().isoformat()
        self.data_devolucao = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "usuario_id": self.usuario.id,
            "livro_id": self.livro.id,
            "data_emprestimo": self.data_emprestimo,
            "data_devolucao": self.data_devolucao
        }
