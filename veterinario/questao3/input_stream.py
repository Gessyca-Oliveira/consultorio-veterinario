"""
Questão 3 - VacinaPerecívelInputStream
Subclasse de io.RawIOBase (equivalente Python de InputStream) que lê
os bytes gerados pelo VacinaPerecívelOutputStream e reconstrói os objetos.
"""

import io
import struct
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from datetime import date
from modelos.produto import VacinaPerecivel


class VacinaPerecívelInputStream(io.RawIOBase):
    """
    Subclasse de RawIOBase (InputStream em Python) que lê os bytes
    produzidos por VacinaPerecívelOutputStream e reconstrói objetos VacinaPerecivel.
    """

    def __init__(self, origem: io.IOBase):
        """
        :param origem: InputStream de origem (stdin, FileInputStream, socket, ...)
        """
        super().__init__()
        self._origem = origem

    def _ler_exato(self, n: int) -> bytes:
        """Lê exatamente n bytes do stream de origem."""
        dados = b""
        while len(dados) < n:
            chunk = self._origem.read(n - len(dados))
            if not chunk:
                raise EOFError(f"Stream encerrou antes de ler {n} bytes.")
            dados += chunk
        return dados

    def _desserializar_vacina(self) -> VacinaPerecivel:
        """Lê os bytes de uma VacinaPerecivel e reconstrói o objeto."""
        # prefixo de tamanho (4 bytes)
        tam_bytes = self._ler_exato(4)
        _tam = struct.unpack('>i', tam_bytes)[0]

        # codigo (4 bytes)
        codigo = struct.unpack('>i', self._ler_exato(4))[0]

        # nome (2 bytes tamanho + N bytes)
        len_nome = struct.unpack('>H', self._ler_exato(2))[0]
        nome = self._ler_exato(len_nome).decode('utf-8')

        # preco (8 bytes)
        preco = struct.unpack('>d', self._ler_exato(8))[0]

        # temperatura (8 bytes)
        temperatura = struct.unpack('>d', self._ler_exato(8))[0]

        # requer_diluente (1 byte)
        requer_diluente = struct.unpack('>?', self._ler_exato(1))[0]

        return VacinaPerecivel(
            codigo=codigo,
            nome=nome,
            preco=round(preco, 2),
            fabricante="(desconhecido)",       # não serializado
            registro_mapa="(desconhecido)",
            especie_alvo="(desconhecido)",
            dosagem="(desconhecido)",
            agente_biologico="(desconhecido)",
            numero_lote="(desconhecido)",
            data_fabricacao=date.today(),       # não serializado
            temperatura_armazenamento=temperatura,
            data_validade=date(9999, 12, 31),   # não serializado
            requer_diluente=requer_diluente
        )

    def ler_vacinas(self) -> list:
        """Lê e retorna a lista de VacinaPerecivel do stream."""
        qtd_bytes = self._ler_exato(4)
        quantidade = struct.unpack('>i', qtd_bytes)[0]
        print(f"  [InputStream] Lendo {quantidade} objeto(s) do stream...")

        vacinas = []
        for i in range(quantidade):
            v = self._desserializar_vacina()
            vacinas.append(v)
            print(f"  [InputStream] #{i+1} Lido: {v.nome} | Preço: R${v.preco:.2f} | "
                  f"Temp: {v.temperatura_armazenamento}°C")
        return vacinas

    # Implementação mínima exigida por RawIOBase
    def readinto(self, b):
        data = self._origem.read(len(b))
        n = len(data)
        b[:n] = data
        return n
