import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.models import Request, Response
from shared.serializer import deserialize_request, serialize_response

def get_request(request_json: str) -> Request:
    """Simula a função getRequest: deserializa a mensagem de requisição"""
    return deserialize_request(request_json)

def send_reply(request_id: str, status: str, result: any, error: str) -> Response:
    """Simula a função sendReply: cria a mensagem de resposta"""
    return Response(
        messageType="response",
        requestId=request_id,
        status=status,
        result=result,
        error=error
    )
