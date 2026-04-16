import socket
import json
from utils.serializer import send_json, recv_json

HOST = "127.0.0.1"
PORT = 9020

MULTICAST_GROUP = "224.1.1.1"
MULTICAST_PORT = 5007

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

print("=== LOGIN ADMIN ===")
usuario = input("Usuário: ")
senha = input("Senha: ")

send_json(sock, {"acao": "login", "usuario": usuario, "senha": senha})
resp = recv_json(sock)
print(resp)

if resp["status"] != "ok":
    sock.close()
    exit()

while True:
    print("\n===== MENU ADMIN =====")
    print("1 - Adicionar animal na fila")
    print("2 - Remover animal da fila")
    print("3 - Enviar aviso multicast")
    print("4 - Ver resultado")
    print("0 - Sair")

    op = input("Escolha: ")

    if op == "1":
        print("\n--- Adicionar Animal ---")
        animal_id = int(input("ID: "))
        nome = input("Nome: ")
        tipo = input("Tipo (Cachorro/Gato/Coelho): ")
        idade = int(input("Idade: "))

        animal = {"id": animal_id, "nome": nome, "tipo": tipo, "idade": idade}

        send_json(sock, {"acao": "adicionar_animal", "animal": animal})
        print(recv_json(sock))

    elif op == "2":
        animal_id = int(input("Digite o ID do animal para remover: "))
        send_json(sock, {"acao": "remover_animal", "animal_id": animal_id})
        print(recv_json(sock))

    elif op == "3":
        aviso = input("Digite o aviso para enviar aos funcionários: ")

        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

        pacote = {
            "tipo": "aviso_admin",
            "mensagem": aviso
        }

        udp.sendto(json.dumps(pacote).encode("utf-8"), (MULTICAST_GROUP, MULTICAST_PORT))
        udp.close()

        print("Aviso multicast enviado!")

    elif op == "4":
        send_json(sock, {"acao": "resultado"})
        print(recv_json(sock))

    elif op == "0":
        break

sock.close()
