# Trabalho 2 - Sistemas Distribuídos (UFC Quixadá)
## Remote Method Invocation (RMI) com Python e Pyro5

### Descrição
Sistema de Biblioteca distribuído implementado em Python usando RMI (Pyro5), seguindo o protocolo requisição-resposta da seção 5.2 do livro texto.

### Requisitos Atendidos
- ✅ 5 classes de entidade (Pessoa, Usuario, Funcionario, Livro, Emprestimo)
- ✅ 2 relações de herança (Usuario é-um Pessoa, Funcionario é-um Pessoa)
- ✅ 2 relações de agregação (Emprestimo tem-um Usuario, Emprestimo tem-um Livro)
- ✅ 5 métodos remotos (cadastrar_usuario, cadastrar_livro, listar_livros, realizar_emprestimo, buscar_livro)
- ✅ Passagem por referência (objetos remotos via URI) e por valor (serialização JSON)
- ✅ Protocolo request-response com campos: `messageType`, `requestId`, `objectReference`, `methodId`, `arguments`
- ✅ Serialização JSON
- ✅ Uso de Pyro5 (RMI) sem criação manual de sockets

### Estrutura de Pastas
```
trabalho_rmi/
├── server/
│   ├── server.py
│   ├── services.py
│   ├── entities/
│   │   ├── pessoa.py
│   │   ├── usuario.py
│   │   ├── funcionario.py
│   │   ├── livro.py
│   │   └── emprestimo.py
│   └── protocol.py
├── client/
│   ├── client.py
│   └── protocol.py
├── shared/
│   ├── models.py
│   └── serializer.py
├── venv/                   (ambiente virtual)
└── README.md
```

### Dependências
- Python 3.8+
- Pyro5

### Passo a Passo para Execução

#### 1. Pré-requisitos
Certifique-se de ter o Python 3.8+ instalado:
```bash
python3 --version
```

#### 2. Configurar Ambiente Virtual
Abra um terminal e execute:
```bash
cd trabalho_rmi
python3 -m venv venv
source venv/bin/activate
pip install pyro5
```

#### 3. Iniciar o Servidor
Em um terminal (mantenha aberto):
```bash
cd trabalho_rmi
source venv/bin/activate
python server/server.py
```
**Saída esperada:**
```
Servidor RMI iniciado. URI: PYRO:obj_xxxx@localhost:xxxxx
Aguardando requisições...
```

O servidor criará o arquivo `server/server_uri.txt` automaticamente.

#### 4. Executar o Cliente
Em outro terminal:
```bash
cd trabalho_rmi
source venv/bin/activate
python client/client.py
```

**Saída esperada:**
```
Name Server não disponível, lendo URI do arquivo...
URI direta: PYRO:obj_xxxx@localhost:xxxxx
=== Cliente do Sistema de Biblioteca (RMI) ===

1. Cadastrando usuário (passagem por valor)...
Resultado: {'status': 'sucesso', 'usuario_id': 1}

2. Cadastrando livro (passagem por valor)...
Resultado: {'status': 'sucesso', 'livro_id': 1}

3. Listando livros...
Livros: [{'id': 1, 'titulo': 'Python Distribuído', 'autor': 'Guido van Rossum', 'isbn': '978-85-1111-111-1', 'disponivel': True}]

4. Realizando empréstimo (passagem por referência de usuário)...
Resultado do empréstimo: {'status': 'sucesso', 'emprestimo_id': 1}

5. Buscando livro por ID...
Livro: {'id': 1, 'titulo': 'Python Distribuído', 'autor': 'Guido van Rossum', 'isbn': '978-85-1111-111-1', 'disponivel': False}
```

#### 5. (Opcional) Usar Name Server do Pyro5
Para usar o Name Server (em vez de arquivo URI):
```bash
# Terminal 1: Inicia Name Server
pyro5-ns

# Terminal 2: Inicia servidor
source venv/bin/activate
python server/server.py

# Terminal 3: Executa cliente
source venv/bin/activate
python client/client.py
```

### Teste Automatizado
Para testar todo o projeto de uma vez (servidor + cliente no mesmo processo):
```bash
cd trabalho_rmi
source venv/bin/activate
python teste_completo.py
```

### Explicação do Protocolo Request-Response
O projeto simula o protocolo da seção 5.2 do livro texto:

1. **doOperation()** (`client/protocol.py`): Cliente monta mensagem com campos obrigatórios e envia via RMI
2. **getRequest()** (`server/protocol.py`): Servidor deserializa a requisição JSON
3. **sendReply()** (`server/protocol.py`): Servidor monta resposta e envia ao cliente

Formato da mensagem de requisição (JSON):
```json
{
  "messageType": "request",
  "requestId": "uuid-único",
  "objectReference": "PYRO:obj@localhost:porta",
  "methodId": "cadastrar_usuario",
  "arguments": [{"id": 1, "nome": "João", ...}]
}
```

### Observações para o Trabalho
- O código não usa sockets diretamente (apenas Pyro5)
- A serialização é feita com JSON (em `shared/serializer.py`)
- Há demonstração de passagem por valor (dicionários) e por referência (URI do Pyro5)
- O projeto está organizado em camadas: shared (modelos), server (lógica + entidades), client (interface)
