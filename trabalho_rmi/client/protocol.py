import uuid
from shared.models import Request
from shared.serializer import serialize_request, deserialize_response

def do_operation(remote_object_ref, method_id: str, arguments: list):
    """Simula a função doOperation: constrói a requisição e envia ao servidor"""
    # Converte argumentos para tipos serializáveis (URI para string)
    serializable_args = []
    for arg in arguments:
        if hasattr(arg, '__str__') and not isinstance(arg, (str, int, float, bool, list, dict, type(None))):
            serializable_args.append(str(arg))
        else:
            serializable_args.append(arg)
    
    # Monta a mensagem de requisição conforme o protocolo
    request = Request(
        messageType="request",
        requestId=str(uuid.uuid4()),
        objectReference=str(remote_object_ref),  # URI do objeto remoto
        methodId=method_id,
        arguments=serializable_args
    )
    
    # Serializa a requisição
    request_json = serialize_request(request)
    
    # Envia ao servidor via RMI (Pyro5)
    response_json = remote_object_ref.process_request(request_json)
    
    # Deserializa a resposta
    response = deserialize_response(response_json)
    
    if response.status == "error":
        raise Exception(f"Erro remoto: {response.error}")
    return response.result
