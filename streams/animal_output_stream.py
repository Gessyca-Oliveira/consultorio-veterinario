import struct

class AnimalOutputStream:
    def __init__(self, animais, quantidade, output_stream):
        self.animais = animais
        self.quantidade = quantidade
        self.output_stream = output_stream

    def write(self):
        self.output_stream.write(struct.pack("!I", self.quantidade))

        for i in range(self.quantidade):
            animal = self.animais[i]

            tipo = animal.__class__.__name__.encode("utf-8")
            nome = animal.nome.encode("utf-8")
            idade = str(animal.idade).encode("utf-8")

            extra = b""
            if animal.__class__.__name__ == "Cachorro":
                extra = animal.raca.encode("utf-8")
            elif animal.__class__.__name__ == "Gato":
                extra = animal.cor.encode("utf-8")
            elif animal.__class__.__name__ == "Coelho":
                extra = str(animal.peso).encode("utf-8")

            self.output_stream.write(struct.pack("!I", len(tipo)))
            self.output_stream.write(tipo)

            self.output_stream.write(struct.pack("!I", len(nome)))
            self.output_stream.write(nome)

            self.output_stream.write(struct.pack("!I", len(idade)))
            self.output_stream.write(idade)

            self.output_stream.write(struct.pack("!I", len(extra)))
            self.output_stream.write(extra)

        self.output_stream.flush()
