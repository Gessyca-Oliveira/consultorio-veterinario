import Pyro5.api
from server.services import BibliotecaService, RequestHandler

def main():
    """Inicializa o servidor RMI, registra o serviço no Name Server do Pyro5"""
    # Inicializa a lógica de negócio
    service = BibliotecaService()
    handler = RequestHandler(service)

    # Inicia o daemon do Pyro5
    daemon = Pyro5.api.Daemon()
    
    # Registra o serviço no Name Server
    ns = Pyro5.api.locate_ns()
    uri = daemon.register(handler)
    ns.register("bib.requesthandler", uri)

    print(f"Servidor RMI iniciado. URI: {uri}")
    print("Aguardando requisições...")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
