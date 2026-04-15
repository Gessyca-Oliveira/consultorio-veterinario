"""
Questão 5 - Sistema de Votações - CLIENTE
  - Login via TCP
  - Recebe lista de candidatos
  - Vota em candidato
  - Recebe notas informativas via UDP multicast
"""

import socket
import threading
import struct
import json
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

TCP_HOST    = 'localhost'
TCP_PORTA   = 9996
MCAST_GROUP = '224.1.1.1'
MCAST_PORTA = 9995


def _enviar(conn, obj: dict):
    payload = json.dumps(obj, ensure_ascii=False).encode('utf-8')
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
    return json.loads(dados.decode('utf-8'))


def ouvir_multicast():
    """Thread que escuta notas informativas do admin via UDP multicast."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', MCAST_PORTA))
        mreq = struct.pack("4sL", socket.inet_aton(MCAST_GROUP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        sock.settimeout(1.0)
        while True:
            try:
                dados, _ = sock.recvfrom(1024)
                print(f"\n  📢 [NOTA INFORMATIVA]: {dados.decode('utf-8')}")
            except socket.timeout:
                pass
    except Exception as e:
        print(f"[Multicast] Erro: {e}")


def executar_cliente_interativo():
    print("=" * 55)
    print("  QUESTÃO 5 - Cliente de Votação")
    print("=" * 55)

    # Thread para escutar multicast
    t = threading.Thread(target=ouvir_multicast, daemon=True)
    t.start()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((TCP_HOST, TCP_PORTA))

            # Login
            usuario = input("\nUsuário: ").strip()
            senha   = input("Senha:   ").strip()
            _enviar(s, {"acao": "LOGIN", "usuario": usuario, "senha": senha})
            resp = _receber(s)

            if resp["status"] != "OK":
                print(f"[ERRO] {resp['msg']}")
                return

            papel = resp["papel"]
            print(f"\n[OK] Login realizado! Papel: {papel}")

            while True:
                print("\n--- Menu ---")
                if papel == "ELEITOR":
                    print("1. Listar candidatos")
                    print("2. Votar")
                    print("3. Ver resultado (se encerrado)")
                    print("0. Sair")
                else:
                    print("1. Listar candidatos")
                    print("2. Adicionar candidato")
                    print("3. Remover candidato")
                    print("4. Enviar nota informativa (multicast)")
                    print("5. Ver resultado (se encerrado)")
                    print("6. Encerrar votação")
                    print("0. Sair")

                op = input("Opção: ").strip()

                if op == "0":
                    _enviar(s, {"acao": "ENCERRAR"})
                    break

                elif op == "1":
                    _enviar(s, {"acao": "LISTAR_CANDIDATOS"})
                    r = _receber(s)
                    cands = r.get("candidatos", {})
                    aberto = r.get("votacao_aberta", False)
                    restante = r.get("tempo_restante", 0)
                    print(f"\n  Votação: {'ABERTA' if aberto else 'ENCERRADA'}")
                    if aberto:
                        print(f"  Tempo restante: {restante} segundos")
                    if cands:
                        for cid, info in cands.items():
                            print(f"  [{cid}] {info['nome']}")
                    else:
                        print("  Nenhum candidato cadastrado.")

                elif op == "2" and papel == "ELEITOR":
                    cid = input("  ID do candidato: ").strip()
                    _enviar(s, {"acao": "VOTAR", "candidato_id": cid})
                    r = _receber(s)
                    print(f"  {'[OK]' if r['status'] == 'OK' else '[ERRO]'} {r['msg']}")

                elif op == "2" and papel == "ADMIN":
                    nome = input("  Nome do candidato: ").strip()
                    _enviar(s, {"acao": "ADICIONAR_CANDIDATO", "nome": nome})
                    r = _receber(s)
                    print(f"  {'[OK]' if r['status'] == 'OK' else '[ERRO]'} {r.get('msg','')}")

                elif op == "3" and papel == "ADMIN":
                    cid = input("  ID do candidato a remover: ").strip()
                    _enviar(s, {"acao": "REMOVER_CANDIDATO", "candidato_id": cid})
                    r = _receber(s)
                    print(f"  {'[OK]' if r['status'] == 'OK' else '[ERRO]'} {r['msg']}")

                elif op == "4" and papel == "ADMIN":
                    nota = input("  Nota informativa: ").strip()
                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
                        udp.sendto(nota.encode('utf-8'), (MCAST_GROUP, MCAST_PORTA))
                    print("  [OK] Nota enviada por multicast.")

                elif op in ("3", "5") and papel == "ELEITOR":
                    _enviar(s, {"acao": "RESULTADO"})
                    r = _receber(s)
                    if r["status"] == "OK":
                        print(f"\n  === RESULTADO FINAL ===")
                        print(f"  Total de votos: {r['total_votos']}")
                        print(f"  Ganhador: 🏆 {r['ganhador']}")
                        for cid, info in r["resultado"].items():
                            print(f"  [{cid}] {info['nome']}: {info['votos']} votos ({info['percentual']}%)")
                    else:
                        print(f"  [ERRO] {r['msg']}")

                elif op == "5" and papel == "ADMIN":
                    _enviar(s, {"acao": "RESULTADO"})
                    r = _receber(s)
                    if r["status"] == "OK":
                        print(f"\n  === RESULTADO FINAL ===")
                        print(f"  Total de votos: {r['total_votos']}")
                        print(f"  Ganhador: 🏆 {r['ganhador']}")
                        for cid, info in r["resultado"].items():
                            print(f"  [{cid}] {info['nome']}: {info['votos']} votos ({info['percentual']}%)")
                    else:
                        print(f"  [ERRO] {r['msg']}")

                elif op == "6" and papel == "ADMIN":
                    _enviar(s, {"acao": "ENCERRAR_VOTACAO"})
                    r = _receber(s)
                    print(f"  {'[OK]' if r['status'] == 'OK' else '[ERRO]'} {r['msg']}")

                else:
                    print("  Opção inválida.")

    except ConnectionRefusedError:
        print("[ERRO] Servidor não encontrado. Execute primeiro: python questao5/servidor_votacao.py")


if __name__ == "__main__":
    executar_cliente_interativo()
