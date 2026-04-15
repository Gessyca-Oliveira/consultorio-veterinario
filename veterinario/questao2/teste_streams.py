"""
Questão 2b - Testes do VacinaPerecívelOutputStream
  i.   Saída padrão (stdout)
  ii.  Arquivo (FileOutputStream)
  iii. Servidor remoto TCP
"""

import io
import socket
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from datetime import date
from modelos.produto import VacinaPerecivel
from questao2.output_stream import VacinaPerecívelOutputStream


# ---------- Dados de teste ----------
def criar_vacinas():
    return [
        VacinaPerecivel(
            codigo=1, nome="Vacina Febre Aftosa", preco=12.00, fabricante="BoehringerVet",
            registro_mapa="002/2021", especie_alvo="Bovinos", dosagem="2ml IM",
            agente_biologico="Vírus inativado", numero_lote="L2024-001",
            data_fabricacao=date(2024, 1, 15), temperatura_armazenamento=4.0,
            data_validade=date(2026, 1, 15), requer_diluente=False
        ),
        VacinaPerecivel(
            codigo=2, nome="Vacina Brucelose", preco=9.50, fabricante="Vallée",
            registro_mapa="005/2019", especie_alvo="Bovinos", dosagem="2ml SC",
            agente_biologico="B. abortus B19", numero_lote="L2024-010",
            data_fabricacao=date(2024, 2, 1), temperatura_armazenamento=5.0,
            data_validade=date(2025, 8, 1), requer_diluente=True
        ),
        VacinaPerecivel(
            codigo=3, nome="Vacina Cinomose", preco=22.00, fabricante="MSD Animal",
            registro_mapa="009/2020", especie_alvo="Caninos", dosagem="1ml SC",
            agente_biologico="Vírus atenuado", numero_lote="L2024-020",
            data_fabricacao=date(2024, 4, 10), temperatura_armazenamento=4.0,
            data_validade=date(2026, 4, 10), requer_diluente=False
        ),
    ]


# ---------- Teste i: stdout ----------
def teste_stdout():
    print("\n" + "="*50)
    print("TESTE i: Enviando para STDOUT (System.out)")
    print("="*50)
    vacinas = criar_vacinas()
    destino = sys.stdout.buffer  # equivalente ao System.out em Java
    stream = VacinaPerecívelOutputStream(vacinas, len(vacinas), destino)
    stream.enviar()
    sys.stdout.buffer.flush()
    print("\n[OK] Bytes escritos em stdout.")


# ---------- Teste ii: arquivo ----------
def teste_arquivo(caminho="vacinas.bin"):
    print("\n" + "="*50)
    print(f"TESTE ii: Enviando para ARQUIVO → {caminho}")
    print("="*50)
    vacinas = criar_vacinas()
    with open(caminho, 'wb') as f:
        stream = VacinaPerecívelOutputStream(vacinas, len(vacinas), f)
        stream.enviar()
    tamanho = os.path.getsize(caminho)
    print(f"[OK] Arquivo '{caminho}' criado com {tamanho} bytes.")
    return caminho


# ---------- Teste iii: TCP ----------
def teste_tcp(host='localhost', porta=9999):
    print("\n" + "="*50)
    print(f"TESTE iii: Enviando para SERVIDOR TCP {host}:{porta}")
    print("="*50)
    vacinas = criar_vacinas()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, porta))
            destino = s.makefile('wb')
            stream = VacinaPerecívelOutputStream(vacinas, len(vacinas), destino)
            stream.enviar()
            destino.flush()
        print("[OK] Dados enviados ao servidor TCP.")
    except ConnectionRefusedError:
        print(f"[AVISO] Servidor TCP não encontrado em {host}:{porta}.")
        print("  → Execute primeiro: python questao2/servidor_tcp.py")


if __name__ == "__main__":
    # Roda todos os testes
    # i.  stdout
    teste_stdout()

    # ii. arquivo
    caminho_arquivo = os.path.join(os.path.dirname(__file__), '..', 'vacinas.bin')
    teste_arquivo(caminho_arquivo)

    # iii. TCP (só funciona se o servidor estiver rodando)
    teste_tcp()
