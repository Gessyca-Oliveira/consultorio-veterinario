import threading
import Pyro5.api
from client.protocol import do_operation
from server.entities.usuario import Usuario
from server.entities.livro import Livro

def main():
    # Conecta ao serviço remoto via Name Server
    ns = Pyro5.api.locate_ns()
    request_handler = Pyro5.api.Proxy(ns.lookup("bib.requesthandler"))
    request_handler._pyroTimeout = 5

    print("=== Cliente do Sistema de Biblioteca (RMI) ===")

    # 1. Cadastrar usuário (passagem por valor)
    print("\n1. Cadastrando usuário (passagem por valor)...")
    usuario = Usuario(1, "João Silva", "111.111.111-11", "202301", "88999999999")
    result = do_operation(request_handler, "cadastrar_usuario", [usuario.to_dict()])
    print(f"Resultado: {result}")

    # 2. Cadastrar livro (passagem por valor)
    print("\n2. Cadastrando livro (passagem por valor)...")
    livro = Livro(1, "Python Distribuído", "Guido van Rossum", "978-85-1111-111-1")
    result = do_operation(request_handler, "cadastrar_livro", [livro.to_dict()])
    print(f"Resultado: {result}")

    # 3. Listar livros
    print("\n3. Listando livros...")
    result = do_operation(request_handler, "listar_livros", [])
    print(f"Livros: {result}")

    # 4. Demonstrar passagem por referência (objeto remoto no cliente)
    print("\n4. Realizando empréstimo (passagem por referência de usuário)...")
    daemon = Pyro5.api.Daemon()
    usuario_remoto = Usuario(2, "Maria Souza", "222.222.222-22", "202302", "88988888888")
    uri = daemon.register(usuario_remoto)
    
    # Inicia o daemon em thread separada para receber chamadas do servidor
    def run_daemon():
        daemon.requestLoop()
    threading.Thread(target=run_daemon, daemon=True).start()

    livro_data = Livro(1, "Python Distribuído", "Guido van Rossum", "978-85-1111-111-1").to_dict()
    result = do_operation(request_handler, "realizar_emprestimo", [uri, livro_data])
    print(f"Resultado do empréstimo: {result}")

    # 5. Buscar livro
    print("\n5. Buscando livro por ID...")
    result = do_operation(request_handler, "buscar_livro", [1])
    print(f"Livro: {result}")

if __name__ == "__main__":
    main()
