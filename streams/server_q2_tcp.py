import socket

HOST = "0.0.0.0"
PORT = 9001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Servidor TCP aguardando conexão na porta", PORT)

conn, addr = server.accept()
print("Conectado por:", addr)

data = conn.recv(4096)
with open("animais_tcp.bin", "wb") as f:
    f.write(data)

print("Dados recebidos e salvos em animais_tcp.bin")

conn.close()
server.close()
