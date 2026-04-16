import struct
from pojos.cachorro import Cachorro
from pojos.gato import Gato
from pojos.coelho import Coelho

class AnimalInputStream:
    def __init__(self, input_stream):
        self.input_stream = input_stream

    def _read_int(self):
        data = self.input_stream.read(4)
        if not data or len(data) < 4:
            return None
        return struct.unpack("!I", data)[0]

    def _read_bytes(self, n):
        return self.input_stream.read(n)

    def read_animais(self):
        qtd = self._read_int()
        if qtd is None:
            return []

        animais = []

        for _ in range(qtd):
            len_tipo = self._read_int()
            tipo = self._read_bytes(len_tipo).decode("utf-8")

            len_nome = self._read_int()
            nome = self._read_bytes(len_nome).decode("utf-8")

            len_idade = self._read_int()
            idade = int(self._read_bytes(len_idade).decode("utf-8"))

            len_extra = self._read_int()
            extra = self._read_bytes(len_extra).decode("utf-8")

            if tipo == "Cachorro":
                animais.append(Cachorro(0, nome, idade, extra))
            elif tipo == "Gato":
                animais.append(Gato(0, nome, idade, extra))
            elif tipo == "Coelho":
                animais.append(Coelho(0, nome, idade, float(extra)))

        return animais
