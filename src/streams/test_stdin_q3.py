import sys
from streams.animal_input_stream import AnimalInputStream

print("Cole os bytes binários aqui (ou redirecione de arquivo):")

stream = AnimalInputStream(sys.stdin.buffer)
animais = stream.read_animais()

for a in animais:
    print(a.__class__.__name__, a.nome, a.idade)
