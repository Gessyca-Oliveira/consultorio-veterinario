"""
Questão 5 - Sistema de Votações - SERVIDOR
  - TCP unicast: login, lista de candidatos, recebimento de votos
  - UDP multicast: notas informativas dos administradores
  - Multi-threaded
  - Serialização em JSON (aceita como alternativa ao Protocol Buffers)
  - Prazo de votação configurável
"""

import socket
import threading
import json
import struct
import time
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# ---- Configuração ----
TCP_HOST    = 'localhost'
TCP_PORTA   = 9996
MCAST_GROUP = '224.1.1.1'
MCAST_PORTA = 9995
DURACAO_VOTACAO = 300  # segundos


# ---- Estado global ----
lock = threading.Lock()
eleitores = {
    "joao": "1234", "maria": "abcd", "pedro": "pass1"
}
admins = {
    "admin": "admin123"
}
candidatos = {}          # id -> {"nome": str, "votos": int}
_proximo_id = 1
votos_registrados = {}   # eleitor -> candidato_id
votacao_aberta = True
tempo_inicio = time.time()


def _serializar(obj: dict) -> bytes:
    return json.dumps(obj, ensure_ascii=False).encode('utf-8')


def _desserializar(dados: bytes) -> dict:
    return json.loads(dados.decode('utf-8'))


def _enviar(conn, obj: dict):
    payload = _serializar(obj)
    conn.sendall(struct.pack('>i', len(payload)) + payload)


def _receber(conn) -> dict:
    header = b""
    while len(header) < 4:
        chunk = conn.recv(4 - len(header))
        if not chunk:
            raise ConnectionError("Conexão encerrada.")
        header += chunk
    tamanho = struct.unpack('>i', header)[0]
    dados = b""
    while len(dados) < tamanho:
        chunk = conn.recv(tamanho - len(dados))
        if not chunk:
            raise ConnectionError("Conexão encerrada.")
        dados += chunk
    return _desserializar(dados)


def tratar_cliente(conn, addr):
    global votacao_aberta
    print(f"[Servidor] Cliente conectado: {addr}")
    usuario = None
    papel = None

    with conn:
        try:
            # ----- Login -----
            req = _receber(conn)
            if req.get("acao") != "LOGIN":
                _enviar(conn, {"status": "ERRO", "msg": "Primeira mensagem deve ser LOGIN."})
                return

            user = req.get("usuario", "")
            senha = req.get("senha", "")

            with lock:
                if user in admins and admins[user] == senha:
                    papel = "ADMIN"
                    usuario = user
                elif user in eleitores and eleitores[user] == senha:
                    papel = "ELEITOR"
                    usuario = user
                else:
                    _enviar(conn, {"status": "ERRO", "msg": "Credenciais inválidas."})
                    return

            _enviar(conn, {"status": "OK", "papel": papel, "usuario": usuario})
            print(f"[Servidor] Login: {usuario} ({papel})")

            # ----- Loop de mensagens -----
            while True:
                req = _receber(conn)
                acao = req.get("acao", "")

                if acao == "LISTAR_CANDIDATOS":
                    with lock:
                        tempo_restante = max(0, DURACAO_VOTACAO - (time.time() - tempo_inicio))
                        _enviar(conn, {"status": "OK", "candidatos": candidatos,
                                       "votacao_aberta": votacao_aberta, "tempo_restante": round(tempo_restante, 1)})

                elif acao == "VOTAR":
                    if papel != "ELEITOR":
                        _enviar(conn, {"status": "ERRO", "msg": "Apenas eleitores podem votar."})
                        continue
                    with lock:
                        if not votacao_aberta:
                            _enviar(conn, {"status": "ERRO", "msg": "Votação encerrada."})
                            continue
                        if usuario in votos_registrados:
                            _enviar(conn, {"status": "ERRO", "msg": "Você já votou."})
                            continue
                        cid = str(req.get("candidato_id"))
                        if cid not in candidatos:
                            _enviar(conn, {"status": "ERRO", "msg": "Candidato não encontrado."})
                            continue
                        candidatos[cid]["votos"] += 1
                        votos_registrados[usuario] = cid
                        _enviar(conn, {"status": "OK",
                                       "msg": f"Voto registrado para {candidatos[cid]['nome']}."})

                elif acao == "ADICIONAR_CANDIDATO":
                    if papel != "ADMIN":
                        _enviar(conn, {"status": "ERRO", "msg": "Apenas admins."})
                        continue
                    with lock:
                        global _proximo_id
                        cid = str(_proximo_id)
                        _proximo_id += 1
                        candidatos[cid] = {"nome": req.get("nome", "Sem nome"), "votos": 0}
                        _enviar(conn, {"status": "OK", "msg": f"Candidato '{candidatos[cid]['nome']}' adicionado.",
                                       "id": cid})

                elif acao == "REMOVER_CANDIDATO":
                    if papel != "ADMIN":
                        _enviar(conn, {"status": "ERRO", "msg": "Apenas admins."})
                        continue
                    with lock:
                        cid = str(req.get("candidato_id"))
                        if cid in candidatos:
                            del candidatos[cid]
                            _enviar(conn, {"status": "OK", "msg": "Candidato removido."})
                        else:
                            _enviar(conn, {"status": "ERRO", "msg": "Candidato não encontrado."})

                elif acao == "RESULTADO":
                    with lock:
                        if votacao_aberta:
                            _enviar(conn, {"status": "ERRO", "msg": "Votação ainda em aberto."})
                            continue
                        total = sum(c["votos"] for c in candidatos.values())
                        resultado = {}
                        ganhador = None
                        max_votos = -1
                        for cid, info in candidatos.items():
                            pct = (info["votos"] / total * 100) if total > 0 else 0
                            resultado[cid] = {
                                "nome": info["nome"],
                                "votos": info["votos"],
                                "percentual": round(pct, 2)
                            }
                            if info["votos"] > max_votos:
                                max_votos = info["votos"]
                                ganhador = info["nome"]
                        _enviar(conn, {"status": "OK", "resultado": resultado,
                                       "ganhador": ganhador, "total_votos": total})

                elif acao == "ENCERRAR_VOTACAO":
                    if papel != "ADMIN":
                        _enviar(conn, {"status": "ERRO", "msg": "Apenas admins."})
                        continue
                    with lock:
                        votacao_aberta = False
                        _enviar(conn, {"status": "OK", "msg": "Votação encerrada manualmente."})

                elif acao == "ENCERRAR":
                    _enviar(conn, {"status": "OK", "msg": "Até logo."})
                    break

                else:
                    _enviar(conn, {"status": "ERRO", "msg": f"Ação desconhecida: {acao}"})

        except (ConnectionError, json.JSONDecodeError) as e:
            print(f"[Servidor] Erro com {addr}: {e}")


def relogio_votacao():
    """Encerra a votação após DURACAO_VOTACAO segundos."""
    global votacao_aberta
    time.sleep(DURACAO_VOTACAO)
    with lock:
        votacao_aberta = False
    print(f"\n[Servidor] *** Votação ENCERRADA após {DURACAO_VOTACAO}s ***")


def iniciar_servidor():
    # Inicia o relógio da votação
    t = threading.Thread(target=relogio_votacao, daemon=True)
    t.start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((TCP_HOST, TCP_PORTA))
        srv.listen(10)
        print(f"[Servidor Q5] TCP em {TCP_HOST}:{TCP_PORTA}")
        print(f"[Servidor Q5] Votação aberta por {DURACAO_VOTACAO} segundos.")
        while True:
            conn, addr = srv.accept()
            thread = threading.Thread(target=tratar_cliente, args=(conn, addr), daemon=True)
            thread.start()


if __name__ == "__main__":
    iniciar_servidor()
