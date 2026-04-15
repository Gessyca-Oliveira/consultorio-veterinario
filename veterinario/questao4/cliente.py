"""
Questão 4 - Cliente TCP com serialização manual de VacinaPerecivel.
"""

import socket
import struct
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from datetime import date
from modelos.produto import VacinaPerecivel
from questao4.protocolo import (
    REQ_LISTAR, REQ_BUSCAR, REQ_ADICIONAR,
    REP_LISTA, REP_VACINA, REP_OK, REP_ERRO,
    serializar_vacina, desserializar_vacina,
    empacotar_mensagem, desempacotar_cabecalho, receber_payload
)


class ClienteVeterinario:
    def __init__(self, host='localhost', porta=9997):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, porta))
        print(f"[Cliente Q4] Conectado em {host}:{porta}")

    def listar_vacinas(self):
        self.sock.sendall(empacotar_mensagem(REQ_LISTAR, b""))
        tipo, tamanho = desempacotar_cabecalho(self.sock)
        payload = receber_payload(self.sock, tamanho)

        if tipo == REP_LISTA:
            qtd = struct.unpack_from('>i', payload, 0)[0]
            offset = 4
            vacinas = []
            for _ in range(qtd):
                tam = struct.unpack_from('>i', payload, offset)[0]; offset += 4
                v = desserializar_vacina(payload[offset:offset+tam]); offset += tam
                vacinas.append(v)
            return vacinas
        elif tipo == REP_ERRO:
            raise RuntimeError(payload.decode())

    def buscar_vacina(self, codigo: int):
        self.sock.sendall(empacotar_mensagem(REQ_BUSCAR, struct.pack('>i', codigo)))
        tipo, tamanho = desempacotar_cabecalho(self.sock)
        payload = receber_payload(self.sock, tamanho)

        if tipo == REP_VACINA:
            return desserializar_vacina(payload)
        elif tipo == REP_ERRO:
            raise RuntimeError(payload.decode())

    def adicionar_vacina(self, vacina: VacinaPerecivel):
        dados = serializar_vacina(vacina)
        self.sock.sendall(empacotar_mensagem(REQ_ADICIONAR, dados))
        tipo, tamanho = desempacotar_cabecalho(self.sock)
        payload = receber_payload(self.sock, tamanho)

        if tipo == REP_OK:
            return True
        elif tipo == REP_ERRO:
            raise RuntimeError(payload.decode())

    def fechar(self):
        self.sock.close()


def main():
    print("=" * 55)
    print("  QUESTÃO 4 - Cliente/Servidor com Serialização Manual")
    print("=" * 55)

    try:
        cliente = ClienteVeterinario()

        # 1. Listar
        print("\n--- Listando vacinas do servidor ---")
        vacinas = cliente.listar_vacinas()
        for v in vacinas:
            print(f"  {v}")

        # 2. Buscar por código
        print("\n--- Buscando vacina código=1 ---")
        v = cliente.buscar_vacina(1)
        print(f"  Encontrada: {v}")

        # 3. Adicionar nova vacina
        print("\n--- Adicionando nova vacina ---")
        nova = VacinaPerecivel(
            codigo=99, nome="Vacina Cinomose Teste", preco=25.00, fabricante="TesteLab",
            registro_mapa="099/2024", especie_alvo="Caninos", dosagem="1ml SC",
            agente_biologico="Vírus atenuado", numero_lote="T2024-099",
            data_fabricacao=date(2024, 7, 1), temperatura_armazenamento=4.0,
            data_validade=date(2026, 7, 1), requer_diluente=False
        )
        cliente.adicionar_vacina(nova)
        print(f"  Vacina '{nova.nome}' adicionada com sucesso!")

        # 4. Listar novamente
        print("\n--- Listando após adição ---")
        vacinas = cliente.listar_vacinas()
        for v in vacinas:
            print(f"  {v.nome}")

        cliente.fechar()

    except ConnectionRefusedError:
        print("[ERRO] Servidor não encontrado. Execute primeiro: python questao4/servidor.py")


if __name__ == "__main__":
    main()
