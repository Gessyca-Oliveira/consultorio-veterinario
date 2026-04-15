from pojos.cachorro import Cachorro
from pojos.gato import Gato
from pojos.coelho import Coelho
from streams.animal_output_stream import AnimalOutputStream

animais = [
    Cachorro(1, "Rex", 5, "Labrador"),
    Gato(2, "Mimi", 3, "Preto"),
    Coelho(3, "Pipoca", 2, 1.5)
]

with open("animais.bin", "wb") as f:
    stream = AnimalOutputStream(animais, 3, f)
    stream.write()

print("Arquivo animais.bin gerado!")
