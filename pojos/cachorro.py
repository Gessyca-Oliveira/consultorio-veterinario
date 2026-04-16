from pojos.animal import Animal

class Cachorro(Animal):
    def __init__(self, id_animal, nome, idade, raca):
        super().__init__(id_animal, nome, idade)
        self.raca = raca

    def to_dict(self):
        d = super().to_dict()
        d["tipo"] = "Cachorro"
        d["raca"] = self.raca
        return d
