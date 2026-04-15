import socket
from streams.animal_input_stream import AnimalInputStream

HOST = "0.0.0.0"
PORT = 9002

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Servidor TCP esperando conexão na porta", PORT)

conn, addr = server.accept()
print("Cliente conectado:", addr)

stream = AnimalInputStream(conn.makefile("rb"))
animais = stream.read_animais()

print("Animais recebidos:")
for a in animais:
    print(a.__class__.__name__, a.nome, a.idade)

conn.close()
server.close()
