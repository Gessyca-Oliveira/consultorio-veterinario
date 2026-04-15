"""
Questão 4 - Servidor TCP com serialização manual de VacinaPerecivel.
Suporta: LISTAR, BUSCAR por código, ADICIONAR vacina.
"""

import socket
import struct
import threading
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from datetime import date
from modelos.produto import VacinaPerecivel
from modelos.servicos import EstoqueProdutosVeterinarios
from questao4.protocolo import (
    REQ_LISTAR, REQ_BUSCAR, REQ_ADICIONAR,
    REP_LISTA, REP_VACINA, REP_OK, REP_ERRO,
    serializar_vacina, desserializar_vacina,
    empacotar_mensagem, desempacotar_cabecalho, receber_payload
)


class ServidorVeterinario:
    def __init__(self, host='localhost', porta=9997):
        self.host = host
        self.porta = porta
        self.estoque = EstoqueProdutosVeterinarios()
        self._popular_estoque()

    def _popular_estoque(self):
        """Adiciona vacinas de exemplo ao estoque inicial."""
        self.estoque.adicionar(VacinaPerecivel(
            codigo=1, nome="Vacina Febre Aftosa", preco=12.00, fabricante="BoehringerVet",
            registro_mapa="002/2021", especie_alvo="Bovinos", dosagem="2ml IM",
            agente_biologico="Vírus inativado", numero_lote="L2024-001",
            data_fabricacao=date(2024, 1, 15), temperatura_armazenamento=4.0,
            data_validade=date(2026, 1, 15), requer_diluente=False
        ))
        self.estoque.adicionar(VacinaPerecivel(
            codigo=2, nome="Vacina Brucelose", preco=9.50, fabricante="Vallée",
            registro_mapa="005/2019", especie_alvo="Bovinos", dosagem="2ml SC",
            agente_biologico="B. abortus B19", numero_lote="L2024-010",
            data_fabricacao=date(2024, 2, 1), temperatura_armazenamento=5.0,
            data_validade=date(2025, 8, 1), requer_diluente=True
        ))

    def iniciar(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
            srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            srv.bind((self.host, self.porta))
            srv.listen(5)
            print(f"[Servidor Q4] Rodando em {self.host}:{self.porta}")
            while True:
                conn, addr = srv.accept()
                t = threading.Thread(target=self._tratar_cliente,
                                     args=(conn, addr), daemon=True)
                t.start()

    def _tratar_cliente(self, conn, addr):
        print(f"[Servidor Q4] Cliente conectado: {addr}")
        with conn:
            try:
                while True:
                    tipo, tamanho = desempacotar_cabecalho(conn)
                    payload = receber_payload(conn, tamanho)
                    self._processar(conn, tipo, payload)
            except (ConnectionError, EOFError, struct.error):
                print(f"[Servidor Q4] Cliente {addr} desconectado.")

    def _processar(self, conn, tipo: int, payload: bytes):
        if tipo == REQ_LISTAR:
            vacinas = self.estoque.listar_todos()
            bloco = struct.pack('>i', len(vacinas))
            for v in vacinas:
                dados = serializar_vacina(v)
                bloco += struct.pack('>i', len(dados)) + dados
            conn.sendall(empacotar_mensagem(REP_LISTA, bloco))
            print(f"[Servidor Q4] LISTAR → {len(vacinas)} vacinas enviadas.")

        elif tipo == REQ_BUSCAR:
            codigo = struct.unpack('>i', payload)[0]
            vacina = self.estoque.buscar_por_codigo(codigo)
            if vacina:
                dados = serializar_vacina(vacina)
                conn.sendall(empacotar_mensagem(REP_VACINA, dados))
                print(f"[Servidor Q4] BUSCAR código={codigo} → encontrada.")
            else:
                msg = f"Vacina código {codigo} não encontrada.".encode()
                conn.sendall(empacotar_mensagem(REP_ERRO, msg))

        elif tipo == REQ_ADICIONAR:
            try:
                vacina = desserializar_vacina(payload)
                self.estoque.adicionar(vacina)
                conn.sendall(empacotar_mensagem(REP_OK, b"OK"))
                print(f"[Servidor Q4] ADICIONAR '{vacina.nome}' → ok.")
            except ValueError as e:
                conn.sendall(empacotar_mensagem(REP_ERRO, str(e).encode()))

        else:
            conn.sendall(empacotar_mensagem(REP_ERRO, b"Tipo desconhecido"))


if __name__ == "__main__":
    ServidorVeterinario().iniciar()
