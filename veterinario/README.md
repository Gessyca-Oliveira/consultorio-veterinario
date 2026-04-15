# Sistema de Controle de Produtos Veterinários
### QXD0043 – Sistemas Distribuídos | UFC Quixadá

---

## Estrutura do Projeto

```
veterinario/
├── modelos/
│   ├── produto.py          # Hierarquia de classes POJO
│   └── servicos.py         # Classes de serviço (EstoqueVeterinario, GerenciadorVacinacao)
├── questao1/
│   └── demo.py             # Demonstração dos POJOs e serviços
├── questao2/
│   ├── output_stream.py    # VacinaPerecívelOutputStream
│   ├── servidor_tcp.py     # Servidor TCP receptor (destino iii)
│   └── teste_streams.py    # Testes: stdout, arquivo e TCP
├── questao3/
│   ├── input_stream.py     # VacinaPerecívelInputStream
│   ├── servidor_tcp_input.py  # Servidor TCP com InputStream
│   └── teste_input_streams.py # Testes: stdin, arquivo e TCP
├── questao4/
│   ├── protocolo.py        # Funções de serialização/desserialização
│   ├── servidor.py         # Servidor TCP multi-threaded
│   └── cliente.py          # Cliente TCP
└── questao5/
    ├── servidor_votacao.py # Servidor de votações (TCP + multicast UDP)
    └── cliente_votacao.py  # Cliente interativo de votação
```

---

## Hierarquia de Classes

```
Produto
└── ProdutoVeterinario
      ├── ProdutoQuimioterapico
      └── ProdutoBiologico
            ├── VacinaPerecivel      ← usada nos streams
            └── VacinaNaoPerecivel
```

---

## Requisitos

- Python 3.8+
- Nenhuma biblioteca externa (somente stdlib)

---

## Execução passo a passo

### Questão 1 – POJOs e Serviços

```bash
cd veterinario
python questao1/demo.py
```

---

### Questão 2 – OutputStream (VacinaPerecívelOutputStream)

**Teste i e ii (stdout e arquivo) – sem servidor:**
```bash
cd veterinario
python questao2/teste_streams.py
```

**Teste iii (TCP) – abrir 2 terminais:**

Terminal 1 (servidor):
```bash
cd veterinario
python questao2/servidor_tcp.py
```

Terminal 2 (cliente):
```bash
cd veterinario
python questao2/teste_streams.py
```

---

### Questão 3 – InputStream (VacinaPerecívelInputStream)

**Teste b e c (stdin simulado e arquivo) – sem servidor:**
```bash
cd veterinario
python questao3/teste_input_streams.py
```

**Teste d (TCP) – abrir 2 terminais:**

Terminal 1 (servidor):
```bash
cd veterinario
python questao3/servidor_tcp_input.py
```

Terminal 2 (cliente):
```bash
cd veterinario
python questao3/teste_input_streams.py
```

---

### Questão 4 – Serialização Cliente-Servidor

Terminal 1 (servidor):
```bash
cd veterinario
python questao4/servidor.py
```

Terminal 2 (cliente):
```bash
cd veterinario
python questao4/cliente.py
```

**Operações disponíveis:**
- Listar vacinas do estoque
- Buscar vacina por código
- Adicionar nova vacina

---

### Questão 5 – Sistema de Votações

Terminal 1 (servidor):
```bash
cd veterinario
python questao5/servidor_votacao.py
```

Terminal 2+ (clientes):
```bash
cd veterinario
python questao5/cliente_votacao.py
```

**Credenciais de login:**

| Usuário | Senha    | Papel   |
|---------|----------|---------|
| joao    | 1234     | Eleitor |
| maria   | abcd     | Eleitor |
| pedro   | pass1    | Eleitor |
| admin   | admin123 | Admin   |

**Fluxo típico:**
1. Admin faz login → adiciona candidatos → envia notas informativas (multicast UDP)
2. Eleitores fazem login → listam candidatos → votam
3. Após 120s a votação é encerrada automaticamente
4. Qualquer usuário pode consultar o resultado

---

## Portas utilizadas

| Questão | Protocolo | Porta |
|---------|-----------|-------|
| Q2 (receptor)       | TCP  | 9999 |
| Q3 (InputStream)    | TCP  | 9998 |
| Q4 (serialização)   | TCP  | 9997 |
| Q5 (votação TCP)    | TCP  | 9996 |
| Q5 (multicast UDP)  | UDP  | 9995 |

---

## Formato do Stream (Questões 2 e 3)

```
[4 bytes: quantidade de objetos]
  Para cada objeto:
    [4 bytes: tamanho do payload]
    [4 bytes: codigo (int)]
    [2 bytes: tamanho do nome] [N bytes: nome UTF-8]
    [8 bytes: preco (double)]
    [8 bytes: temperatura (double)]
    [1 byte: requer_diluente (bool)]
```

## Protocolo de Mensagens (Questão 4)

```
[1 byte: tipo] [4 bytes: tamanho_payload] [N bytes: payload]

Tipos:
  0x01 = REQUEST_LISTAR
  0x02 = REQUEST_BUSCAR
  0x03 = REQUEST_ADICIONAR
  0x11 = REPLY_LISTA
  0x12 = REPLY_VACINA
  0x13 = REPLY_OK
  0xFF = REPLY_ERRO
```

## Serialização (Questão 5)

Utiliza **JSON** (alternativa aceita ao Protocol Buffers conforme enunciado).
