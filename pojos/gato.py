from pojos.animal import Animal

class Gato(Animal):
    def __init__(self, id_animal, nome, idade, cor):
        super().__init__(id_animal, nome, idade)
        self.cor = cor

    def to_dict(self):
        d = super().to_dict()
        d["tipo"] = "Gato"
        d["cor"] = self.cor
        return d
