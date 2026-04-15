"""
Hierarquia de Classes POJO - Sistema de Controle de Produtos Veterinários

Hierarquia:
  Produto
    └── ProdutoVeterinario
          ├── ProdutoQuimioterapico
          └── ProdutoBiologico
                ├── VacinaPerecivel
                └── VacinaNaoPerecivel
"""

from datetime import date


class Produto:
    """Superclasse base para todos os produtos."""

    def __init__(self, codigo: int, nome: str, preco: float, fabricante: str):
        self.codigo = codigo
        self.nome = nome
        self.preco = preco
        self.fabricante = fabricante

    def __str__(self):
        return (
            f"[Produto] Código: {self.codigo} | Nome: {self.nome} | "
            f"Preço: R${self.preco:.2f} | Fabricante: {self.fabricante}"
        )

    def __repr__(self):
        return self.__str__()


class ProdutoVeterinario(Produto):
    """Representa um produto de uso veterinário."""

    def __init__(self, codigo: int, nome: str, preco: float, fabricante: str,
                 registro_mapa: str, especie_alvo: str, dosagem: str):
        super().__init__(codigo, nome, preco, fabricante)
        self.registro_mapa = registro_mapa   # registro no MAPA
        self.especie_alvo = especie_alvo     # ex: bovinos, caninos
        self.dosagem = dosagem               # ex: "2ml por 10kg"

    def __str__(self):
        return (
            f"[ProdutoVeterinario] Código: {self.codigo} | Nome: {self.nome} | "
            f"Preço: R${self.preco:.2f} | Fabricante: {self.fabricante} | "
            f"Registro MAPA: {self.registro_mapa} | Espécie: {self.especie_alvo} | "
            f"Dosagem: {self.dosagem}"
        )


class ProdutoQuimioterapico(ProdutoVeterinario):
    """Produto veterinário de natureza quimioterápica (antibióticos, antiparasitários, etc.)."""

    def __init__(self, codigo: int, nome: str, preco: float, fabricante: str,
                 registro_mapa: str, especie_alvo: str, dosagem: str,
                 principio_ativo: str, classe_terapeutica: str, periodo_carencia: int):
        super().__init__(codigo, nome, preco, fabricante, registro_mapa, especie_alvo, dosagem)
        self.principio_ativo = principio_ativo         # ex: Ivermectina
        self.classe_terapeutica = classe_terapeutica   # ex: Antiparasitário
        self.periodo_carencia = periodo_carencia       # dias para abate/consumo

    def __str__(self):
        return (
            f"[ProdutoQuimioterapico] Código: {self.codigo} | Nome: {self.nome} | "
            f"Fabricante: {self.fabricante} | Princípio Ativo: {self.principio_ativo} | "
            f"Classe: {self.classe_terapeutica} | Carência: {self.periodo_carencia} dias"
        )


class ProdutoBiologico(ProdutoVeterinario):
    """Produto veterinário de natureza biológica."""

    def __init__(self, codigo: int, nome: str, preco: float, fabricante: str,
                 registro_mapa: str, especie_alvo: str, dosagem: str,
                 agente_biologico: str, numero_lote: str, data_fabricacao: date):
        super().__init__(codigo, nome, preco, fabricante, registro_mapa, especie_alvo, dosagem)
        self.agente_biologico = agente_biologico   # ex: vírus atenuado
        self.numero_lote = numero_lote
        self.data_fabricacao = data_fabricacao

    def __str__(self):
        return (
            f"[ProdutoBiologico] Código: {self.codigo} | Nome: {self.nome} | "
            f"Fabricante: {self.fabricante} | Agente: {self.agente_biologico} | "
            f"Lote: {self.numero_lote} | Fabricação: {self.data_fabricacao}"
        )


class VacinaPerecivel(ProdutoBiologico):
    """Vacina que necessita de refrigeração contínua e possui validade curta."""

    def __init__(self, codigo: int, nome: str, preco: float, fabricante: str,
                 registro_mapa: str, especie_alvo: str, dosagem: str,
                 agente_biologico: str, numero_lote: str, data_fabricacao: date,
                 temperatura_armazenamento: float, data_validade: date,
                 requer_diluente: bool):
        super().__init__(codigo, nome, preco, fabricante, registro_mapa, especie_alvo, dosagem,
                         agente_biologico, numero_lote, data_fabricacao)
        self.temperatura_armazenamento = temperatura_armazenamento  # graus Celsius
        self.data_validade = data_validade
        self.requer_diluente = requer_diluente

    def esta_valida(self) -> bool:
        return date.today() <= self.data_validade

    def __str__(self):
        validade = "VÁLIDA" if self.esta_valida() else "VENCIDA"
        return (
            f"[VacinaPerecivel] Código: {self.codigo} | Nome: {self.nome} | "
            f"Lote: {self.numero_lote} | Temp: {self.temperatura_armazenamento}°C | "
            f"Validade: {self.data_validade} ({validade}) | "
            f"Requer Diluente: {'Sim' if self.requer_diluente else 'Não'}"
        )


class VacinaNaoPerecivel(ProdutoBiologico):
    """Vacina liofilizada ou estável que não exige refrigeração rigorosa."""

    def __init__(self, codigo: int, nome: str, preco: float, fabricante: str,
                 registro_mapa: str, especie_alvo: str, dosagem: str,
                 agente_biologico: str, numero_lote: str, data_fabricacao: date,
                 prazo_validade_meses: int, forma_apresentacao: str,
                 temperatura_max_armazenamento: float):
        super().__init__(codigo, nome, preco, fabricante, registro_mapa, especie_alvo, dosagem,
                         agente_biologico, numero_lote, data_fabricacao)
        self.prazo_validade_meses = prazo_validade_meses
        self.forma_apresentacao = forma_apresentacao            # ex: liofilizado, suspensão
        self.temperatura_max_armazenamento = temperatura_max_armazenamento  # máxima tolerada

    def __str__(self):
        return (
            f"[VacinaNaoPerecivel] Código: {self.codigo} | Nome: {self.nome} | "
            f"Lote: {self.numero_lote} | Validade: {self.prazo_validade_meses} meses | "
            f"Apresentação: {self.forma_apresentacao} | "
            f"Temp. máx: {self.temperatura_max_armazenamento}°C"
        )
