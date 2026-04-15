"""
Questão 3d - Servidor TCP que usa VacinaPerecívelInputStream para decodificar os dados.
Execute ANTES do teste_input_streams.py (teste TCP).
"""

import socket
import io
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from questao3.input_stream import VacinaPerecívelInputStream


def iniciar_servidor(host='localhost', porta=9998):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((host, porta))
        srv.listen(1)
        print(f"[Servidor InputStream TCP] Aguardando em {host}:{porta} ...")
        conn, addr = srv.accept()
        with conn:
            print(f"[Servidor InputStream TCP] Conectado: {addr}")
            raw = conn.makefile('rb')
            stream = VacinaPerecívelInputStream(raw)
            vacinas = stream.ler_vacinas()
            print(f"\n[Servidor] Total desserializado: {len(vacinas)} vacina(s)")


if __name__ == "__main__":
    iniciar_servidor()
