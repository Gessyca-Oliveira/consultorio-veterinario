from .pessoa import Pessoa

class Usuario(Pessoa):  # Herança: Usuario É-UM Pessoa
    """Entidade de usuário da biblioteca"""
    def __init__(self, id: int, nome: str, cpf: str, matricula: str, telefone: str):
        super().__init__(id, nome, cpf)
        self.matricula = matricula
        self.telefone = telefone

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({"matricula": self.matricula, "telefone": self.telefone, "tipo": "Usuario"})
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "Usuario":
        return cls(data["id"], data["nome"], data["cpf"], data["matricula"], data["telefone"])
