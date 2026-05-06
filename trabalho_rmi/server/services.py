import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import Pyro5.api
from server.entities.usuario import Usuario
from server.entities.livro import Livro
from server.protocol import get_request, send_reply
from shared.models import Request, Response

class BibliotecaService:
    """Lógica de negócio do sistema de biblioteca"""
    def __init__(self):
        self.usuarios = {}    # id: Usuario
        self.livros = {}      # id: Livro
        self.emprestimos = {} # id: Emprestimo
        self.next_id = 1

    # Métodos remotos (mais de 4, conforme exigido)
    def cadastrar_usuario(self, usuario_data):
        """Cadastra um usuário (suporta passagem por valor ou referência)"""
        if isinstance(usuario_data, dict):
            # Passagem por valor: reconstrói objeto localmente
            usuario = Usuario.from_dict(usuario_data)
        else:
            # Passagem por referência: usa proxy remoto para obter dados
            usuario = Usuario.from_dict(usuario_data.to_dict())
        
        if usuario.id in self.usuarios:
            raise Exception("Usuário já cadastrado")
        self.usuarios[usuario.id] = usuario
        return {"status": "sucesso", "usuario_id": usuario.id}

    def cadastrar_livro(self, livro_data):
        """Cadastra um livro (suporta passagem por valor ou referência)"""
        if isinstance(livro_data, dict):
            livro = Livro.from_dict(livro_data)
        else:
            livro = Livro.from_dict(livro_data.to_dict())
        
        if livro.id in self.livros:
            raise Exception("Livro já cadastrado")
        self.livros[livro.id] = livro
        return {"status": "sucesso", "livro_id": livro.id}

    def listar_livros(self):
        """Lista todos os livros cadastrados"""
        return [livro.to_dict() for livro in self.livros.values()]

    def realizar_emprestimo(self, usuario_ref, livro_data):
        """Realiza empréstimo (usuário por referência, livro por valor)"""
        import Pyro5.api
        # Se receber uma URI (string), cria um proxy para passagem por referência
        if isinstance(usuario_ref, str):
            usuario_proxy = Pyro5.api.Proxy(usuario_ref)
        else:
            usuario_proxy = usuario_ref
        
        # Passagem por referência: obtém dados do usuário remoto via proxy
        usuario_data = usuario_proxy.to_dict()
        usuario = Usuario.from_dict(usuario_data)
        
        # Passagem por valor: reconstrói livro localmente
        livro = Livro.from_dict(livro_data)
        
        if livro.id not in self.livros:
            raise Exception("Livro não encontrado")
        if not self.livros[livro.id].disponivel:
            raise Exception("Livro não disponível")
        if usuario.id not in self.usuarios:
            raise Exception("Usuário não cadastrado")
        
        emprestimo_id = self.next_id
        self.next_id += 1
        from server.entities.emprestimo import Emprestimo
        emprestimo = Emprestimo(emprestimo_id, usuario, self.livros[livro.id])
        self.emprestimos[emprestimo_id] = emprestimo
        self.livros[livro.id].disponivel = False
        return {"status": "sucesso", "emprestimo_id": emprestimo_id}

    def buscar_livro(self, livro_id):
        """Busca um livro por ID"""
        return self.livros[livro_id].to_dict() if livro_id in self.livros else None


@Pyro5.api.expose
class RequestHandler:
    """Objeto remoto que processa as requisições do protocolo RMI"""
    def __init__(self, service: BibliotecaService):
        self.service = service

    def process_request(self, request_json: str) -> str:
        """Método remoto único que processa todas as requisições"""
        # Simula getRequest(): deserializa a requisição
        request = get_request(request_json)
        
        # Despacha para o método correto
        method_id = request.methodId
        args = request.arguments
        try:
            if method_id == "cadastrar_usuario":
                result = self.service.cadastrar_usuario(*args)
            elif method_id == "cadastrar_livro":
                result = self.service.cadastrar_livro(*args)
            elif method_id == "listar_livros":
                result = self.service.listar_livros(*args)
            elif method_id == "realizar_emprestimo":
                result = self.service.realizar_emprestimo(*args)
            elif method_id == "buscar_livro":
                result = self.service.buscar_livro(*args)
            else:
                raise Exception(f"Método {method_id} não encontrado")
            
            # Simula sendReply(): cria resposta de sucesso
            response = send_reply(request.requestId, "success", result, None)
            return response.to_json()
        except Exception as e:
            # Simula sendReply(): cria resposta de erro
            response = send_reply(request.requestId, "error", None, str(e))
            return response.to_json()
