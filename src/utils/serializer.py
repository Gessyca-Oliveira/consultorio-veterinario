import json
import struct

def send_json(sock, obj):
    data = json.dumps(obj).encode("utf-8")
    sock.sendall(struct.pack("!I", len(data)))
    sock.sendall(data)

def recv_json(sock):
    size_data = sock.recv(4)
    if not size_data:
        return None
    size = struct.unpack("!I", size_data)[0]

    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            break
        data += chunk

    return json.loads(data.decode("utf-8"))
