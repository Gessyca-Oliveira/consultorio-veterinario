import socket
import threading
from utils.serializer import recv_json, send_json

HOST = "0.0.0.0"
PORT = 9010

animais_db = [
    {"id": 1, "tipo": "Cachorro", "nome": "Rex", "idade": 5},
    {"id": 2, "tipo": "Gato", "nome": "Mimi", "idade": 3},
    {"id": 3, "tipo": "Coelho", "nome": "Pipoca", "idade": 2},
]

def handle_client(conn, addr):
    print("Cliente conectado:", addr)

    while True:
        req = recv_json(conn)
        if req is None:
            break

        if req["acao"] == "listar_animais":
            reply = {"status": "ok", "animais": animais_db}
            send_json(conn, reply)

        elif req["acao"] == "buscar_por_nome":
            nome = req["nome"]
            encontrados = [a for a in animais_db if a["nome"].lower() == nome.lower()]
            send_json(conn, {"status": "ok", "resultado": encontrados})

        else:
            send_json(conn, {"status": "erro", "mensagem": "Ação inválida"})

    conn.close()
    print("Cliente desconectado:", addr)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(10)

print("Servidor TCP Questão 4 rodando em", PORT)

while True:
    conn, addr = server.accept()
    t = threading.Thread(target=handle_client, args=(conn, addr))
    t.start()
