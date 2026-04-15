"""
Questão 2 - VacinaPerecívelOutputStream
Subclasse de io.RawIOBase (equivalente Python de OutputStream) que serializa
um array de VacinaPerecivel em bytes e os envia para um stream de destino.

Formato de cada vacina no stream:
  [4 bytes: codigo int] [2 bytes: len(nome)] [N bytes: nome] 
  [8 bytes: preco double] [4 bytes: periodo_carencia ou temperatura*100 int]
  Total de bytes escritos por objeto é gravado antes dos dados como prefixo de 4 bytes.
"""

import io
import struct
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from modelos.produto import VacinaPerecivel


class VacinaPerecívelOutputStream(io.RawIOBase):
    """
    Subclasse de RawIOBase (OutputStream em Python) que serializa
    um array de VacinaPerecivel para bytes e os envia para um stream destino.

    Atributos serializados por vacina (>= 3 conforme requisito):
      - codigo       (int,   4 bytes)
      - nome         (str,   2 bytes de tamanho + N bytes UTF-8)
      - preco        (float, 8 bytes)
      - temperatura  (float, 8 bytes)
      - requer_diluente (bool, 1 byte)
    """

    def __init__(self, vacinas: list, quantidade: int, destino: io.RawIOBase):
        """
        :param vacinas:    array de VacinaPerecivel a transmitir
        :param quantidade: quantos objetos do array serão enviados
        :param destino:    OutputStream de destino
        """
        super().__init__()
        self._vacinas = vacinas
        self._quantidade = min(quantidade, len(vacinas))
        self._destino = destino

    def _serializar_vacina(self, vacina: VacinaPerecivel) -> bytes:
        """Serializa uma VacinaPerecivel em bytes."""
        # codigo: 4 bytes
        b_codigo = struct.pack('>i', vacina.codigo)

        # nome: 2 bytes de tamanho + conteúdo UTF-8
        nome_bytes = vacina.nome.encode('utf-8')
        b_nome = struct.pack('>H', len(nome_bytes)) + nome_bytes

        # preco: 8 bytes double
        b_preco = struct.pack('>d', vacina.preco)

        # temperatura_armazenamento: 8 bytes double
        b_temp = struct.pack('>d', vacina.temperatura_armazenamento)

        # requer_diluente: 1 byte boolean
        b_diluente = struct.pack('>?', vacina.requer_diluente)

        payload = b_codigo + b_nome + b_preco + b_temp + b_diluente
        return payload

    def enviar(self):
        """Serializa e envia as vacinas para o stream destino."""
        # cabeçalho: quantidade de objetos (4 bytes)
        self._destino.write(struct.pack('>i', self._quantidade))

        for i in range(self._quantidade):
            vacina = self._vacinas[i]
            payload = self._serializar_vacina(vacina)

            # prefixo: número de bytes deste objeto (4 bytes)
            self._destino.write(struct.pack('>i', len(payload)))
            self._destino.write(payload)
            print(f"  [Stream] Vacina '{vacina.nome}' → {4 + len(payload)} bytes enviados")

        if hasattr(self._destino, 'flush'):
            self._destino.flush()

    # Implementação mínima de RawIOBase
    def readinto(self, b):
        return 0

    def write(self, b):
        return self._destino.write(b)
