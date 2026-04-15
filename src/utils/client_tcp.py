import socket
from utils.serializer import send_json, recv_json

HOST = "127.0.0.1"
PORT = 9010

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

send_json(sock, {"acao": "listar_animais"})
resp = recv_json(sock)
print("Resposta listar_animais:", resp)

send_json(sock, {"acao": "buscar_por_nome", "nome": "Rex"})
resp = recv_json(sock)
print("Resposta buscar_por_nome:", resp)

sock.close()
