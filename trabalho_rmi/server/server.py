import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import Pyro5.api
from server.services import BibliotecaService, RequestHandler

def main():
    """Inicializa o servidor RMI, registra o serviço no Name Server do Pyro5"""
    # Inicializa a lógica de negócio
    service = BibliotecaService()
    handler = RequestHandler(service)

    # Inicia o daemon do Pyro5
    daemon = Pyro5.api.Daemon()
    uri = daemon.register(handler)
    
    # Salva URI em arquivo para o cliente usar (funciona com ou sem Name Server)
    with open(os.path.join(os.path.dirname(__file__), "server_uri.txt"), "w") as f:
        f.write(str(uri))
    
    # Tenta registrar no Name Server (opcional)
    try:
        ns = Pyro5.api.locate_ns()
        ns.register("bib.requesthandler", uri)
        print(f"Servidor RMI iniciado. URI registrada no Name Server: {uri}")
    except Exception as e:
        print(f"Name Server não disponível, usando URI direta: {uri}")

    print("Aguardando requisições...")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
