import socket
import struct
import json

MULTICAST_GROUP = "224.1.1.1"
MULTICAST_PORT = 5007

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind(("", MULTICAST_PORT))

mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print("=== OUVINDO AVISOS MULTICAST ===")
print("Grupo:", MULTICAST_GROUP, "Porta:", MULTICAST_PORT)

while True:
    data, addr = sock.recvfrom(4096)
    msg = json.loads(data.decode("utf-8"))

    print("\n--- AVISO RECEBIDO ---")
    print("De:", addr)
    print("Mensagem:", msg.get("mensagem"))
