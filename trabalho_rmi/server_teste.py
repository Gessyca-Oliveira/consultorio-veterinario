#!/usr/bin/env python3
"""
Servidor de teste simples para validar o projeto RMI
"""
import sys
import os
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import Pyro5.api
from server.services import BibliotecaService, RequestHandler

def main():
    # Inicializa o serviço
    service = BibliotecaService()
    handler = RequestHandler(service)
    
    # Inicia o daemon do Pyro5
    daemon = Pyro5.api.Daemon()
    uri = daemon.register(handler)
    
    # Salva a URI para o cliente usar
    with open(os.path.join(os.path.dirname(__file__), "server", "server_uri.txt"), "w") as f:
        f.write(str(uri))
    
    print(f"Servidor RMI iniciado. URI: {uri}")
    print("Aguardando requisições...")
    
    # Loop do servidor
    daemon.requestLoop()

if __name__ == "__main__":
    main()
