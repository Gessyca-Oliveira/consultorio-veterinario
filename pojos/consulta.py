class Consulta:
    def __init__(self, id_consulta, animal_nome, veterinario, data):
        self.id_consulta = id_consulta
        self.animal_nome = animal_nome
        self.veterinario = veterinario
        self.data = data

    def to_dict(self):
        return {
            "id_consulta": self.id_consulta,
            "animal_nome": self.animal_nome,
            "veterinario": self.veterinario,
            "data": self.data
        }
