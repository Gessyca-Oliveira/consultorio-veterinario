import socket
from utils.serializer import send_json, recv_json

HOST = "127.0.0.1"
PORT = 9020

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

print("=== LOGIN ELEITOR (FUNCIONÁRIO) ===")
usuario = input("Usuário: ")
senha = input("Senha: ")

send_json(sock, {"acao": "login", "usuario": usuario, "senha": senha})
resp = recv_json(sock)
print(resp)

if resp["status"] != "ok":
    sock.close()
    exit()

send_json(sock, {"acao": "listar_fila"})
resp = recv_json(sock)

if resp["status"] != "ok":
    print(resp)
    sock.close()
    exit()

fila = resp["fila"]

print("\n=== FILA DE CONSULTAS ===")
for a in fila:
    print(f"ID: {a['id']} | Nome: {a['nome']} | Tipo: {a['tipo']} | Idade: {a['idade']}")

animal_id = int(input("\nDigite o ID do animal que deve ter prioridade: "))

send_json(sock, {"acao": "votar_prioridade", "animal_id": animal_id})
resp = recv_json(sock)
print(resp)

send_json(sock, {"acao": "resultado"})
resp = recv_json(sock)

print("\n=== RESULTADO ATUAL ===")
print(resp)

sock.close()
