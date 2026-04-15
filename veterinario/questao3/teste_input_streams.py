"""
Questão 3 - Testes do VacinaPerecívelInputStream
  b. Entrada padrão (stdin)  → envia com VacinaPerecívelOutputStream e lê de volta
  c. Arquivo (FileInputStream)
  d. Servidor remoto TCP
"""

import io
import socket
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from datetime import date
from modelos.produto import VacinaPerecivel
from questao2.output_stream import VacinaPerecívelOutputStream
from questao3.input_stream import VacinaPerecívelInputStream


def criar_vacinas():
    return [
        VacinaPerecivel(
            codigo=10, nome="Vacina Leptospirose", preco=15.75, fabricante="Zoetis",
            registro_mapa="010/2022", especie_alvo="Caninos", dosagem="1ml SC",
            agente_biologico="L. icterohaemorrhagiae", numero_lote="LZ2024-05",
            data_fabricacao=date(2024, 5, 1), temperatura_armazenamento=4.0,
            data_validade=date(2026, 5, 1), requer_diluente=False
        ),
        VacinaPerecivel(
            codigo=11, nome="Vacina Parvovirose", preco=19.00, fabricante="Elanco",
            registro_mapa="011/2022", especie_alvo="Caninos", dosagem="1ml IM",
            agente_biologico="Parvovírus atenuado", numero_lote="EL2024-06",
            data_fabricacao=date(2024, 6, 1), temperatura_armazenamento=2.0,
            data_validade=date(2026, 6, 1), requer_diluente=True
        ),
    ]


# ---------- Teste b: piped buffer (simula stdin/stdout) ----------
def teste_stdin_simulado():
    print("\n" + "="*50)
    print("TESTE b: stdin simulado (pipe entre OutputStream e InputStream)")
    print("="*50)
    buffer = io.BytesIO()
    vacinas = criar_vacinas()

    # Escreve no buffer (simula System.out / stdin)
    out = VacinaPerecívelOutputStream(vacinas, len(vacinas), buffer)
    out.enviar()

    # Volta ao início para leitura
    buffer.seek(0)
    inp = VacinaPerecívelInputStream(buffer)
    lidas = inp.ler_vacinas()
    print(f"[OK] {len(lidas)} vacina(s) lidas do stdin simulado.")


# ---------- Teste c: arquivo ----------
def teste_arquivo(caminho=None):
    if caminho is None:
        caminho = os.path.join(os.path.dirname(__file__), '..', 'vacinas.bin')

    print("\n" + "="*50)
    print(f"TESTE c: Lendo de ARQUIVO → {caminho}")
    print("="*50)

    # Gera o arquivo se não existir
    if not os.path.exists(caminho):
        print("  [INFO] Arquivo não encontrado, gerando...")
        vacinas = criar_vacinas()
        with open(caminho, 'wb') as f:
            out = VacinaPerecívelOutputStream(vacinas, len(vacinas), f)
            out.enviar()

    with open(caminho, 'rb') as f:
        inp = VacinaPerecívelInputStream(f)
        lidas = inp.ler_vacinas()
    print(f"[OK] {len(lidas)} vacina(s) lidas do arquivo '{caminho}'.")


# ---------- Teste d: TCP ----------
def teste_tcp_cliente(host='localhost', porta=9998):
    print("\n" + "="*50)
    print(f"TESTE d: Enviando e lendo via TCP {host}:{porta}")
    print("="*50)
    vacinas = criar_vacinas()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, porta))
            destino = s.makefile('wb')
            out = VacinaPerecívelOutputStream(vacinas, len(vacinas), destino)
            out.enviar()
            destino.flush()
        print("[OK] Dados enviados. O servidor decodificará os objetos.")
    except ConnectionRefusedError:
        print(f"[AVISO] Servidor TCP não encontrado em {host}:{porta}.")
        print("  → Execute primeiro: python questao3/servidor_tcp_input.py")


if __name__ == "__main__":
    teste_stdin_simulado()
    teste_arquivo()
    teste_tcp_cliente()
