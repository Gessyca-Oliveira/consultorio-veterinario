import json
from dataclasses import dataclass

@dataclass
class Request:
    """Modelo da mensagem de requisição (protocolo request-response)"""
    messageType: str       # Tipo da mensagem (sempre "request")
    requestId: str         # ID único da requisição
    objectReference: str   # Referência do objeto remoto (URI do Pyro5)
    methodId: str          # ID do método a ser invocado
    arguments: list        # Argumentos do método

    def to_json(self) -> str:
        """Serializa a requisição para JSON"""
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(json_str: str) -> "Request":
        """Deserializa JSON para objeto Request"""
        data = json.loads(json_str)
        return Request(**data)

@dataclass
class Response:
    """Modelo da mensagem de resposta (protocolo request-response)"""
    messageType: str       # Tipo da mensagem (sempre "response")
    requestId: str         # ID da requisição original
    status: str            # Status da execução ("success" ou "error")
    result: any            # Resultado da execução (se sucesso)
    error: str             # Mensagem de erro (se houver)

    def to_json(self) -> str:
        """Serializa a resposta para JSON"""
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(json_str: str) -> "Response":
        """Deserializa JSON para objeto Response"""
        data = json.loads(json_str)
        return Response(**data)
