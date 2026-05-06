class Livro:
    """Entidade de livro da biblioteca"""
    def __init__(self, id: int, titulo: str, autor: str, isbn: str):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponivel = True

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "titulo": self.titulo,
            "autor": self.autor,
            "isbn": self.isbn,
            "disponivel": self.disponivel
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Livro":
        livro = cls(data["id"], data["titulo"], data["autor"], data["isbn"])
        livro.disponivel = data["disponivel"]
        return livro
