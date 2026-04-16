from pojos.consulta import Consulta

class ServicoConsulta:
    def __init__(self):
        self.consultas = []

    def marcar_consulta(self, id_consulta, animal_nome, veterinario, data):
        consulta = Consulta(id_consulta, animal_nome, veterinario, data)
        self.consultas.append(consulta)
        return consulta

    def listar_consultas(self):
        return [c.to_dict() for c in self.consultas]
