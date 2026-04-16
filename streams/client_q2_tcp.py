import socket
from pojos.cachorro import Cachorro
from pojos.gato import Gato
from pojos.coelho import Coelho
from streams.animal_output_stream import AnimalOutputStream

HOST = "127.0.0.1"
PORT = 9001

animais = [
    Cachorro(1, "Rex", 5, "Labrador"),
    Gato(2, "Mimi", 3, "Preto"),
    Coelho(3, "Pipoca", 2, 1.5)
]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

stream = AnimalOutputStream(animais, 3, sock.makefile("wb"))
stream.write()

sock.close()
print("Enviado para servidor TCP!")
