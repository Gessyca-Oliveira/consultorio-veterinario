from shared.models import Request, Response

def serialize_request(request: Request) -> str:
    """Serializa objeto Request para JSON"""
    return request.to_json()

def deserialize_request(json_str: str) -> Request:
    """Deserializa JSON para objeto Request"""
    return Request.from_json(json_str)

def serialize_response(response: Response) -> str:
    """Serializa objeto Response para JSON"""
    return response.to_json()

def deserialize_response(json_str: str) -> Response:
    """Deserializa JSON para objeto Response"""
    return Response.from_json(json_str)
