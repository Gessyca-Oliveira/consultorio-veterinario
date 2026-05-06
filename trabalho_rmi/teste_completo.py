#!/usr/bin/env python3
"""
Teste completo do projeto RMI - executa servidor e cliente no mesmo processo
"""
import sys
import os
import threading
import time

sys.path.insert(0, '/home/borges/Documents/SD/consultorio-veterinario/trabalho_rmi')

from server.services import BibliotecaService, RequestHandler
from client.protocol import do_operation
from server.entities.usuario import Usuario
from server.entities.livro import Livro
import Pyro5.api

def main():
    print("=== TESTE COMPLETO DO PROJETO RMI ===\n")
    
    # 1. Inicia servidor em thread
    print("1. Iniciando servidor...")
    service = BibliotecaService()
    handler = RequestHandler(service)
    daemon = Pyro5.api.Daemon()
    uri = daemon.register(handler)
    
    def server_loop():
        daemon.requestLoop()
    
    server_thread = threading.Thread(target=server_loop, daemon=True)
    server_thread.start()
    print(f"   Servidor iniciado. URI: {uri}\n")
    
    # 2. Cria proxy para o cliente
    print("2. Criando conexão do cliente...")
    proxy = Pyro5.api.Proxy(uri)
    proxy._pyroTimeout = 5
    print("   Conexão estabelecida.\n")
    
    # 3. Testa cadastrar usuário (passagem por valor)
    print("3. Cadastrando usuário (passagem por valor)...")
    usuario = Usuario(1, "João Silva", "111.111.111-11", "202301", "88999999999")
    result = do_operation(proxy, "cadastrar_usuario", [usuario.to_dict()])
    print(f"   Resultado: {result}\n")
    
    # 4. Testa cadastrar livro (passagem por valor)
    print("4. Cadastrando livro (passagem por valor)...")
    livro = Livro(1, "Python Distribuído", "Guido van Rossum", "978-85-1111-111-1")
    result = do_operation(proxy, "cadastrar_livro", [livro.to_dict()])
    print(f"   Resultado: {result}\n")
    
    # 5. Testa listar livros
    print("5. Listando livros...")
    result = do_operation(proxy, "listar_livros", [])
    print(f"   Livros: {result}\n")
    
    # 6. Testa buscar livro
    print("6. Buscando livro por ID...")
    result = do_operation(proxy, "buscar_livro", [1])
    print(f"   Livro: {result}\n")
    
    # 7. Testa realizar empréstimo (passagem por referência)
    print("7. Realizando empréstimo (passagem por referência)...")
    # Cria daemon para o objeto remoto do cliente
    client_daemon = Pyro5.api.Daemon()
    usuario_remoto = Usuario(1, "João Silva", "111.111.111-11", "202301", "88999999999")
    uri_usuario = client_daemon.register(usuario_remoto)
    
    def client_server_loop():
        client_daemon.requestLoop()
    
    client_thread = threading.Thread(target=client_server_loop, daemon=True)
    client_thread.start()
    
    livro_data = Livro(1, "Python Distribuído", "Guido van Rossum", "978-85-1111-111-1").to_dict()
    result = do_operation(proxy, "realizar_emprestimo", [uri_usuario, livro_data])
    print(f"   Resultado: {result}\n")
    
    # 8. Verifica se livro foi marcado como indisponível
    print("8. Verificando se livro está indisponível...")
    result = do_operation(proxy, "buscar_livro", [1])
    print(f"   Livro: {result}\n")
    
    print("=== TESTE CONCLUÍDO COM SUCESSO ===")

if __name__ == "__main__":
    main()
