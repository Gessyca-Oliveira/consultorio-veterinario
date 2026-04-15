"""
Questão 1 - Demonstração das classes POJO e serviços
Sistema de Controle de Produtos Veterinários
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from datetime import date
from modelos.produto import (ProdutoVeterinario, ProdutoQuimioterapico,
                              VacinaPerecivel, VacinaNaoPerecivel)
from modelos.servicos import EstoqueProdutosVeterinarios, GerenciadorVacinacao


def main():
    print("=" * 60)
    print("  QUESTÃO 1 - Classes POJO e Serviços Veterinários")
    print("=" * 60)

    # --- Criando instâncias dos POJOs ---
    quimio = ProdutoQuimioterapico(
        codigo=1, nome="Ivermectina 1%", preco=45.90, fabricante="LabVet",
        registro_mapa="001/2022", especie_alvo="Bovinos",
        dosagem="1ml/50kg", principio_ativo="Ivermectina",
        classe_terapeutica="Antiparasitário", periodo_carencia=28
    )

    vacina_p = VacinaPerecivel(
        codigo=2, nome="Vacina Febre Aftosa", preco=12.00, fabricante="BoehringerVet",
        registro_mapa="002/2021", especie_alvo="Bovinos",
        dosagem="2ml IM", agente_biologico="Vírus inativado tipo O, A, C",
        numero_lote="L2024-001", data_fabricacao=date(2024, 1, 15),
        temperatura_armazenamento=4.0, data_validade=date(2026, 1, 15),
        requer_diluente=False
    )

    vacina_np = VacinaNaoPerecivel(
        codigo=3, nome="Vacina Raiva Canina", preco=18.50, fabricante="MSD Animal Health",
        registro_mapa="003/2020", especie_alvo="Caninos",
        dosagem="1ml SC", agente_biologico="Vírus atenuado ERA",
        numero_lote="L2024-002", data_fabricacao=date(2024, 3, 1),
        prazo_validade_meses=24, forma_apresentacao="Liofilizado",
        temperatura_max_armazenamento=25.0
    )

    print("\n--- POJOs Criados ---")
    print(quimio)
    print(vacina_p)
    print(vacina_np)

    # --- Usando os serviços ---
    print("\n--- Serviço: Estoque ---")
    estoque = EstoqueProdutosVeterinarios()
    estoque.adicionar(quimio)
    estoque.adicionar(vacina_p)
    estoque.adicionar(vacina_np)
    print(estoque.relatorio())

    print("\n--- Busca por Espécie: Bovinos ---")
    for p in estoque.buscar_por_especie("Bovinos"):
        print(f"  -> {p.nome}")

    print("\n--- Serviço: Gerenciador de Vacinação ---")
    gerenciador = GerenciadorVacinacao()
    gerenciador.criar_campanha("Campanha Aftosa 2024", [vacina_p])
    alertas = gerenciador.alertas_vencimento([vacina_p], dias_aviso=365)
    if alertas:
        for a in alertas:
            print(a)
    else:
        print("Nenhum alerta de vencimento próximo.")


if __name__ == "__main__":
    main()
