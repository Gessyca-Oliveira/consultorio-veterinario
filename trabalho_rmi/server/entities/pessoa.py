class Pessoa:
    """Classe base para entidades de pessoa (herança)"""
    def __init__(self, id: int, nome: str, cpf: str):
        self.id = id
        self.nome = nome
        self.cpf = cpf

    def to_dict(self) -> dict:
        """Serializa para dicionário (JSON)"""
        return {"id": self.id, "nome": self.nome, "cpf": self.cpf}

    @classmethod
    def from_dict(cls, data: dict) -> "Pessoa":
        """Reconstrói a partir de dicionário"""
        return cls(data["id"], data["nome"], data["cpf"])
