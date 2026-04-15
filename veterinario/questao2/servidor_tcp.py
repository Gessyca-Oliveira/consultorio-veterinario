"""
Questão 2b-iii - Servidor TCP simples para receber o stream de vacinas.
Execute este servidor ANTES de rodar o teste TCP no teste_streams.py
"""

import socket
import struct


def iniciar_servidor(host='localhost', porta=9999):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((host, porta))
        srv.listen(1)
        print(f"[Servidor TCP] Aguardando conexão em {host}:{porta} ...")
        conn, addr = srv.accept()
        with conn:
            print(f"[Servidor TCP] Conectado: {addr}")
            dados = b""
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                dados += chunk
            print(f"[Servidor TCP] Total recebido: {len(dados)} bytes")
            # Exibe os bytes recebidos em hex (diagnóstico)
            print(f"[Servidor TCP] Hex: {dados.hex()}")

            # Decodifica para conferência
            idx = 0
            qtd = struct.unpack_from('>i', dados, idx)[0]
            idx += 4
            print(f"[Servidor TCP] Quantidade de objetos: {qtd}")
            for _ in range(qtd):
                tam = struct.unpack_from('>i', dados, idx)[0]
                idx += 4
                codigo = struct.unpack_from('>i', dados, idx)[0]; idx += 4
                len_nome = struct.unpack_from('>H', dados, idx)[0]; idx += 2
                nome = dados[idx:idx+len_nome].decode('utf-8'); idx += len_nome
                preco = struct.unpack_from('>d', dados, idx)[0]; idx += 8
                temp = struct.unpack_from('>d', dados, idx)[0]; idx += 8
                diluente = struct.unpack_from('>?', dados, idx)[0]; idx += 1
                print(f"  -> Código:{codigo} | Nome:{nome} | Preço:R${preco:.2f} "
                      f"| Temp:{temp}°C | Diluente:{'Sim' if diluente else 'Não'}")


if __name__ == "__main__":
    iniciar_servidor()
