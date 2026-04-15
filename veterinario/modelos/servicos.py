"""
Classes de Serviço - Sistema de Controle de Produtos Veterinários
Implementam operações de negócio sobre os POJOs.
"""

from datetime import date
from typing import List, Optional
from modelos.produto import (Produto, ProdutoVeterinario, ProdutoQuimioterapico,
                              ProdutoBiologico, VacinaPerecivel, VacinaNaoPerecivel)


class EstoqueProdutosVeterinarios:
    """
    Serviço 1: Gerencia o estoque de produtos veterinários.
    Permite adicionar, remover, buscar e listar produtos.
    """

    def __init__(self):
        self._estoque: List[ProdutoVeterinario] = []

    def adicionar(self, produto: ProdutoVeterinario) -> None:
        if any(p.codigo == produto.codigo for p in self._estoque):
            raise ValueError(f"Produto com código {produto.codigo} já existe no estoque.")
        self._estoque.append(produto)
        print(f"[Estoque] Produto '{produto.nome}' adicionado com sucesso.")

    def remover(self, codigo: int) -> bool:
        for i, p in enumerate(self._estoque):
            if p.codigo == codigo:
                self._estoque.pop(i)
                print(f"[Estoque] Produto código {codigo} removido.")
                return True
        print(f"[Estoque] Produto código {codigo} não encontrado.")
        return False

    def buscar_por_codigo(self, codigo: int) -> Optional[ProdutoVeterinario]:
        for p in self._estoque:
            if p.codigo == codigo:
                return p
        return None

    def buscar_por_especie(self, especie: str) -> List[ProdutoVeterinario]:
        return [p for p in self._estoque
                if especie.lower() in p.especie_alvo.lower()]

    def listar_todos(self) -> List[ProdutoVeterinario]:
        return list(self._estoque)

    def listar_vacinas_vencidas(self) -> List[VacinaPerecivel]:
        return [p for p in self._estoque
                if isinstance(p, VacinaPerecivel) and not p.esta_valida()]

    def total_em_estoque(self) -> int:
        return len(self._estoque)

    def relatorio(self) -> str:
        if not self._estoque:
            return "Estoque vazio."
        linhas = ["=== Relatório de Estoque ==="]
        for p in self._estoque:
            linhas.append(str(p))
        linhas.append(f"Total: {self.total_em_estoque()} produto(s)")
        return "\n".join(linhas)


class GerenciadorVacinacao:
    """
    Serviço 2: Controla campanhas de vacinação e validação de vacinas.
    """

    def __init__(self):
        self._campanhas: dict = {}   # nome_campanha -> lista de VacinaPerecivel

    def criar_campanha(self, nome: str, vacinas: List[VacinaPerecivel]) -> None:
        if nome in self._campanhas:
            raise ValueError(f"Campanha '{nome}' já existe.")
        validas = [v for v in vacinas if v.esta_valida()]
        invalidas = len(vacinas) - len(validas)
        self._campanhas[nome] = validas
        print(f"[Vacinação] Campanha '{nome}' criada com {len(validas)} vacinas válidas "
              f"({invalidas} descartadas por vencimento).")

    def vacinas_da_campanha(self, nome: str) -> List[VacinaPerecivel]:
        return self._campanhas.get(nome, [])

    def validar_lote(self, numero_lote: str, lista_vacinas: List[VacinaPerecivel]) -> dict:
        resultado = {"lote": numero_lote, "total": 0, "validas": 0, "vencidas": 0, "itens": []}
        for v in lista_vacinas:
            if v.numero_lote == numero_lote:
                resultado["total"] += 1
                if v.esta_valida():
                    resultado["validas"] += 1
                else:
                    resultado["vencidas"] += 1
                resultado["itens"].append(str(v))
        return resultado

    def alertas_vencimento(self, lista_vacinas: List[VacinaPerecivel],
                           dias_aviso: int = 30) -> List[str]:
        alertas = []
        hoje = date.today()
        for v in lista_vacinas:
            if v.esta_valida():
                delta = (v.data_validade - hoje).days
                if delta <= dias_aviso:
                    alertas.append(
                        f"ALERTA: Vacina '{v.nome}' (Lote {v.numero_lote}) "
                        f"vence em {delta} dias ({v.data_validade})."
                    )
        return alertas

    def listar_campanhas(self) -> List[str]:
        return list(self._campanhas.keys())
