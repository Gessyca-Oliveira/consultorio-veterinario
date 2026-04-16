from pojos.animal import Animal

class Coelho(Animal):
    def __init__(self, id_animal, nome, idade, peso):
        super().__init__(id_animal, nome, idade)
        self.peso = peso

    def to_dict(self):
        d = super().to_dict()
        d["tipo"] = "Coelho"
        d["peso"] = self.peso
        return d
