from .pessoa import Pessoa

class Funcionario(Pessoa):  # Herança: Funcionario É-UM Pessoa
    """Entidade de funcionário da biblioteca"""
    def __init__(self, id: int, nome: str, cpf: str, registro: str, cargo: str):
        super().__init__(id, nome, cpf)
        self.registro = registro
        self.cargo = cargo

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({"registro": self.registro, "cargo": self.cargo, "tipo": "Funcionario"})
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "Funcionario":
        return cls(data["id"], data["nome"], data["cpf"], data["registro"], data["cargo"])
