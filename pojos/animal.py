class Animal:
    def __init__(self, id_animal, nome, idade):
        self.id_animal = id_animal
        self.nome = nome
        self.idade = idade

    def to_dict(self):
        return {
            "tipo": "Animal",
            "id_animal": self.id_animal,
            "nome": self.nome,
            "idade": self.idade
        }
