import socket
import threading
import time
from utils.serializer import send_json, recv_json

HOST = "0.0.0.0"
PORT = 9020

# Multicast config
MULTICAST_GROUP = "224.1.1.1"
MULTICAST_PORT = 5007

# Tempo limite de votação (segundos)
TEMPO_VOTACAO = 60
inicio_votacao = time.time()

# Usuários do sistema
eleitores = {
    "recepcao": "123",
    "funcionario": "123"
}

admins = {
    "admin": "admin123"
}

# "Candidatos" = animais aguardando atendimento
fila_consultas = [
    {"id": 1, "nome": "Rex", "tipo": "Cachorro", "idade": 5},
    {"id": 2, "nome": "Mimi", "tipo": "Gato", "idade": 3},
    {"id": 3, "nome": "Pipoca", "tipo": "Coelho", "idade": 2}
]

# Votos por animal (id -> quantidade votos)
votos = {
    1: 0,
    2: 0,
    3: 0
}

lock = threading.Lock()


def votacao_ativa():
    return (time.time() - inicio_votacao) < TEMPO_VOTACAO


def calcular_resultado():
    total = sum(votos.values())
    resultado = []

    for animal in fila_consultas:
        animal_id = animal["id"]
        qtd_votos = votos.get(animal_id, 0)

        if total == 0:
            percentual = 0
        else:
            percentual = (qtd_votos / total) * 100

        resultado.append({
            "animal": animal,
            "votos": qtd_votos,
            "percentual": percentual
        })

    vencedor = None
    if total > 0:
        vencedor_id = max(votos, key=votos.get)
        for animal in fila_consultas:
            if animal["id"] == vencedor_id:
                vencedor = animal
                break

    return {
        "tempo_restante": max(0, TEMPO_VOTACAO - int(time.time() - inicio_votacao)),
        "total_votos": total,
        "resultado": resultado,
        "prioridade_atendimento": vencedor
    }


def handle_client(conn, addr):
    print("Cliente conectado:", addr)

    autenticado = False
    tipo_usuario = None

    while True:
        req = recv_json(conn)
        if req is None:
            break

        acao = req.get("acao")

        # LOGIN
        if acao == "login":
            usuario = req.get("usuario")
            senha = req.get("senha")

            if usuario in eleitores and eleitores[usuario] == senha:
                autenticado = True
                tipo_usuario = "eleitor"
                send_json(conn, {"status": "ok", "tipo": "eleitor"})
            elif usuario in admins and admins[usuario] == senha:
                autenticado = True
                tipo_usuario = "admin"
                send_json(conn, {"status": "ok", "tipo": "admin"})
            else:
                send_json(conn, {"status": "erro", "mensagem": "Login inválido"})

        elif not autenticado:
            send_json(conn, {"status": "erro", "mensagem": "Usuário não autenticado"})

        # LISTAR FILA
        elif acao == "listar_fila":
            send_json(conn, {"status": "ok", "fila": fila_consultas})

        # VOTAR NA PRIORIDADE
        elif acao == "votar_prioridade":
            if tipo_usuario != "eleitor":
                send_json(conn, {"status": "erro", "mensagem": "Somente eleitores podem votar"})
                continue

            if not votacao_ativa():
                send_json(conn, {"status": "erro", "mensagem": "Tempo de votação encerrado"})
                continue

            animal_id = req.get("animal_id")

            with lock:
                existe = False
                for a in fila_consultas:
                    if a["id"] == animal_id:
                        existe = True
                        break

                if not existe:
                    send_json(conn, {"status": "erro", "mensagem": "Animal não existe na fila"})
                else:
                    votos[animal_id] += 1
                    send_json(conn, {"status": "ok", "mensagem": "Voto computado com sucesso"})

        # RESULTADO
        elif acao == "resultado":
            send_json(conn, {"status": "ok", "dados": calcular_resultado()})

        # ADMIN ADICIONAR ANIMAL NA FILA
        elif acao == "adicionar_animal":
            if tipo_usuario != "admin":
                send_json(conn, {"status": "erro", "mensagem": "Somente admin pode adicionar"})
                continue

            novo = req.get("animal")
            if not novo:
                send_json(conn, {"status": "erro", "mensagem": "Dados inválidos"})
                continue

            with lock:
                fila_consultas.append(novo)
                votos[novo["id"]] = 0

            send_json(conn, {"status": "ok", "mensagem": "Animal adicionado na fila"})

        # ADMIN REMOVER ANIMAL
        elif acao == "remover_animal":
            if tipo_usuario != "admin":
                send_json(conn, {"status": "erro", "mensagem": "Somente admin pode remover"})
                continue

            animal_id = req.get("animal_id")

            with lock:
                removido = False
                for a in fila_consultas:
                    if a["id"] == animal_id:
                        fila_consultas.remove(a)
                        votos.pop(animal_id, None)
                        removido = True
                        break

            if removido:
                send_json(conn, {"status": "ok", "mensagem": "Animal removido da fila"})
            else:
                send_json(conn, {"status": "erro", "mensagem": "Animal não encontrado"})

        else:
            send_json(conn, {"status": "erro", "mensagem": "Ação inválida"})

    conn.close()
    print("Cliente desconectado:", addr)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(10)

print("Servidor Questão 5 rodando na porta", PORT)
print("Tempo de votação:", TEMPO_VOTACAO, "segundos")
print("Multicast Group:", MULTICAST_GROUP, "Port:", MULTICAST_PORT)

while True:
    conn, addr = server.accept()
    t = threading.Thread(target=handle_client, args=(conn, addr))
    t.start()
