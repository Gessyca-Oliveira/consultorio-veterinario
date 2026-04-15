"""
Questão 4 - Protocolo de serialização manual (empacotamento/desempacotamento)
para comunicação cliente-servidor via TCP.

Formato da mensagem:
  [1 byte: tipo]  [4 bytes: tamanho_payload]  [N bytes: payload]

Tipos de mensagem:
  0x01 = REQUEST_LISTAR
  0x02 = REQUEST_BUSCAR  (codigo como payload)
  0x03 = REQUEST_ADICIONAR (vacina serializada)
  0x11 = REPLY_LISTA
  0x12 = REPLY_VACINA
  0x13 = REPLY_OK
  0xFF = REPLY_ERRO
"""

import struct
import io
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from datetime import date
from modelos.produto import VacinaPerecivel


# ---- Constantes de tipo ----
REQ_LISTAR    = 0x01
REQ_BUSCAR    = 0x02
REQ_ADICIONAR = 0x03
REP_LISTA     = 0x11
REP_VACINA    = 0x12
REP_OK        = 0x13
REP_ERRO      = 0xFF


def _encode_str(s: str) -> bytes:
    b = s.encode('utf-8')
    return struct.pack('>H', len(b)) + b


def _decode_str(buf: bytes, offset: int):
    length = struct.unpack_from('>H', buf, offset)[0]
    offset += 2
    return buf[offset:offset+length].decode('utf-8'), offset + length


def serializar_vacina(v: VacinaPerecivel) -> bytes:
    """Empacota uma VacinaPerecivel em bytes."""
    buf = io.BytesIO()
    buf.write(struct.pack('>i', v.codigo))
    buf.write(_encode_str(v.nome))
    buf.write(struct.pack('>d', v.preco))
    buf.write(_encode_str(v.fabricante))
    buf.write(_encode_str(v.registro_mapa))
    buf.write(_encode_str(v.especie_alvo))
    buf.write(_encode_str(v.dosagem))
    buf.write(_encode_str(v.agente_biologico))
    buf.write(_encode_str(v.numero_lote))
    buf.write(struct.pack('>HHH', v.data_fabricacao.year,
                          v.data_fabricacao.month, v.data_fabricacao.day))
    buf.write(struct.pack('>d', v.temperatura_armazenamento))
    buf.write(struct.pack('>HHH', v.data_validade.year,
                          v.data_validade.month, v.data_validade.day))
    buf.write(struct.pack('>?', v.requer_diluente))
    return buf.getvalue()


def desserializar_vacina(dados: bytes) -> VacinaPerecivel:
    """Desempacota bytes e reconstrói VacinaPerecivel."""
    offset = 0
    codigo = struct.unpack_from('>i', dados, offset)[0]; offset += 4
    nome, offset = _decode_str(dados, offset)
    preco = struct.unpack_from('>d', dados, offset)[0]; offset += 8
    fabricante, offset = _decode_str(dados, offset)
    registro_mapa, offset = _decode_str(dados, offset)
    especie_alvo, offset = _decode_str(dados, offset)
    dosagem, offset = _decode_str(dados, offset)
    agente_biologico, offset = _decode_str(dados, offset)
    numero_lote, offset = _decode_str(dados, offset)
    y, m, d = struct.unpack_from('>HHH', dados, offset); offset += 6
    data_fabricacao = date(y, m, d)
    temperatura = struct.unpack_from('>d', dados, offset)[0]; offset += 8
    y2, m2, d2 = struct.unpack_from('>HHH', dados, offset); offset += 6
    data_validade = date(y2, m2, d2)
    requer_diluente = struct.unpack_from('>?', dados, offset)[0]

    return VacinaPerecivel(
        codigo=codigo, nome=nome, preco=round(preco, 2),
        fabricante=fabricante, registro_mapa=registro_mapa,
        especie_alvo=especie_alvo, dosagem=dosagem,
        agente_biologico=agente_biologico, numero_lote=numero_lote,
        data_fabricacao=data_fabricacao,
        temperatura_armazenamento=temperatura,
        data_validade=data_validade,
        requer_diluente=requer_diluente
    )


def empacotar_mensagem(tipo: int, payload: bytes) -> bytes:
    """Empacota tipo + tamanho + payload em uma mensagem."""
    return struct.pack('>Bi', tipo, len(payload)) + payload


def desempacotar_cabecalho(sock) -> tuple:
    """Lê o cabeçalho de 5 bytes de um socket e retorna (tipo, tamanho)."""
    cabecalho = _receber_exato(sock, 5)
    tipo, tamanho = struct.unpack('>Bi', cabecalho)
    return tipo, tamanho


def _receber_exato(sock, n: int) -> bytes:
    dados = b""
    while len(dados) < n:
        chunk = sock.recv(n - len(dados))
        if not chunk:
            raise ConnectionError("Conexão encerrada antes de receber dados suficientes.")
        dados += chunk
    return dados


def receber_payload(sock, tamanho: int) -> bytes:
    return _receber_exato(sock, tamanho)
