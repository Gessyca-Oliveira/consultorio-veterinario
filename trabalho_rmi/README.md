# Trabalho 2 - Sistemas Distribuídos (UFC Quixadá)
## Remote Method Invocation (RMI) com Python e Pyro5

### Descrição
Sistema de Biblioteca distribuído implementado em Python usando RMI (Pyro5), seguindo o protocolo requisição-resposta da seção 5.2 do livro texto.

### Requisitos Atendidos
- ✅ 4+ classes de entidade (Pessoa, Usuario, Funcionario, Livro, Emprestimo)
- ✅ 2 relações de herança (Usuario é-um Pessoa, Funcionario é-um Pessoa)
- ✅ 2 relações de agregação (Emprestimo tem-um Usuario, Emprestimo tem-um Livro)
- ✅ 4+ métodos remotos (cadastrar_usuario, cadastrar_livro, listar_livros, realizar_emprestimo, buscar_livro)
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
└── README.md
```

### Dependências
- Python 3.8+
- Pyro5: `pip install pyro5`

### Como Executar
1. **Inicie o Name Server do Pyro5** (terminal 1):
```bash
cd trabalho_rmi
pyro5-ns
```

2. **Inicie o Servidor** (terminal 2):
```bash
cd trabalho_rmi
python server/server.py
```

3. **Inicie o Cliente** (terminal 3):
```bash
cd trabalho_rmi
python client/client.py
```

### Exemplo de Saída
#### Servidor:
```
Servidor RMI iniciado. URI: PYRO:obj_xxx@localhost:9090
Aguardando requisições...
```

#### Cliente:
```
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
