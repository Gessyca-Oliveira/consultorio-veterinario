from streams.animal_input_stream import AnimalInputStream

with open("animais.bin", "rb") as f:
    stream = AnimalInputStream(f)
    animais = stream.read_animais()

print("Animais lidos do arquivo:")
for a in animais:
    print(a.__class__.__name__, a.nome, a.idade)
