```md
# 🐾 Trabalho 1 - Sistemas Distribuídos (QXD0043)
**Universidade Federal do Ceará – Campus Quixadá**  
**Professor:** Rafael Braga  
**Disciplina:** Sistemas Distribuídos (Capítulo 4 - Comunicação entre Processos)  
**Tema:** Sistema Clínica Veterinária  

Este projeto implementa todas as questões do Trabalho 1 utilizando **Python**, aplicando conceitos de:
- Comunicação Cliente-Servidor via **Sockets TCP**
- Comunicação Multicast via **Sockets UDP**
- Manipulação de **Streams (InputStream/OutputStream)**
- Serialização e representação externa de dados via **JSON**
- Servidor **multi-thread**

---

# 📌 Estrutura do Projeto

A estrutura recomendada do projeto é:

```

src/
│
├── pojos/
│   ├── animal.py
│   ├── cachorro.py
│   ├── gato.py
│   ├── coelho.py
│   ├── estoque.py
│   ├── consulta.py
│   ├── servico_consulta.py
│   └── servico_estoque.py
│
├── streams/
│   ├── animal_output_stream.py
│   ├── animal_input_stream.py
│   ├── test_stdout_q2.py
│   ├── test_file_q2.py
│   ├── server_q2_tcp.py
│   ├── client_q2_tcp.py
│   ├── test_file_q3.py
│   ├── test_stdin_q3.py
│   ├── server_q3_tcp.py
│   └── client_q3_tcp.py
│
├── questao4/
│   ├── server_tcp.py
│   └── client_tcp.py
│
├── questao5/
│   ├── server.py
│   ├── client_eleitor.py
│   ├── client_admin.py
│   └── multicast_listener.py
│
└── utils/
└── serializer.py

````

---

# ⚙️ Requisitos

- Python 3.8+
- Linux recomendado (Ubuntu/Debian/Fedora) por causa do Multicast

Verifique se o Python está instalado:

```bash
python3 --version
````

---

# ▶️ Como Executar

Entre na pasta `src/` antes de rodar qualquer coisa:

```bash
cd src
```

---

# ✅ QUESTÃO 1 — POJOs + Serviços

## 🎯 Objetivo

Criar classes do tipo POJO (objetos simples) que representam o sistema de uma clínica veterinária.

### Superclasse

* `Animal`

### Subclasses

* `Cachorro`
* `Gato`
* `Coelho`

### Agregação

* `Estoque` (armazenamento de produtos)

### Interface/Serviço

* `Consulta` (representa consultas)
* `ServicoConsulta` (modelo para criar e listar consultas)
* `ServicoEstoque` (modelo para gerenciar estoque)

📌 Esses arquivos são utilizados como base para as outras questões.

---

# ✅ QUESTÃO 2 — OutputStream (Envio de objetos em fluxo de bytes)

## 🎯 Objetivo

Criar uma subclasse de OutputStream chamada:

* `AnimalOutputStream`

Essa classe envia um **array de objetos** (Cachorro/Gato/Coelho) em formato binário.

### Como funciona o protocolo de envio?

Para cada animal, o stream envia:

* tipo do animal (ex: Cachorro)
* nome
* idade
* atributo extra (raça/cor/peso)

Antes de cada campo, o sistema envia o **tamanho em bytes** daquele campo.

Isso garante que o receptor consiga reconstruir corretamente os dados.

---

## 🧪 Testes da Questão 2

### 1) Teste enviando para stdout (saída padrão)

```bash
python3 streams/test_stdout_q2.py
```

📌 Isso imprime bytes no terminal (não será legível).

---

### 2) Teste enviando para arquivo binário

```bash
python3 streams/test_file_q2.py
```

Isso gera o arquivo:

```
animais.bin
```

---

### 3) Teste enviando para servidor remoto TCP

#### Terminal 1 (servidor TCP recebendo bytes)

```bash
python3 streams/server_q2_tcp.py
```

#### Terminal 2 (cliente enviando bytes)

```bash
python3 streams/client_q2_tcp.py
```

Isso gera o arquivo:

```
animais_tcp.bin
```

---

# ✅ QUESTÃO 3 — InputStream (Leitura dos bytes gerados)

## 🎯 Objetivo

Criar uma subclasse de InputStream chamada:

* `AnimalInputStream`

Ela é capaz de ler os dados binários enviados pelo `AnimalOutputStream`
e reconstruir os objetos corretamente.

---

## 🧪 Testes da Questão 3

### 1) Ler do arquivo criado na Questão 2

Primeiro gere o arquivo:

```bash
python3 streams/test_file_q2.py
```

Depois leia:

```bash
python3 streams/test_file_q3.py
```

Você verá algo como:

```
Cachorro Rex 5
Gato Mimi 3
Coelho Pipoca 2
```

---

### 2) Ler via TCP

#### Terminal 1 (Servidor lendo com AnimalInputStream)

```bash
python3 streams/server_q3_tcp.py
```

#### Terminal 2 (Cliente enviando usando AnimalOutputStream)

```bash
python3 streams/client_q3_tcp.py
```

O servidor exibirá os animais recebidos via TCP.

---

### 3) Ler via stdin (entrada padrão)

📌 Esse teste pode ser feito redirecionando arquivo:

```bash
python3 streams/test_stdin_q3.py < animais.bin
```

---

# ✅ QUESTÃO 4 — Serialização Cliente-Servidor (TCP)

## 🎯 Objetivo

Criar um serviço remoto cliente-servidor utilizando sockets TCP, com:

* request empacotado no cliente
* reply empacotado no servidor
* desempacotamento dos dois lados

Para isso foi implementado um protocolo simples em JSON usando:

📌 `utils/serializer.py`

Esse módulo implementa:

* `send_json(sock, obj)` → envia JSON com tamanho fixo (4 bytes + mensagem)
* `recv_json(sock)` → recebe JSON baseado no tamanho

---

## 🧪 Como rodar Questão 4

### Terminal 1 (Servidor)

```bash
python3 questao4/server_tcp.py
```

### Terminal 2 (Cliente)

```bash
python3 questao4/client_tcp.py
```

O cliente faz duas requisições:

* listar animais
* buscar animal pelo nome

---

# ✅ QUESTÃO 5 — TCP + Multicast UDP + Multi-thread (Clínica Veterinária)

## 🎯 Objetivo

Implementar uma aplicação distribuída que suporta:

* login de usuário (TCP)
* envio de lista de candidatos (TCP)
* envio de voto (TCP)
* envio de notas informativas via multicast UDP
* servidor multi-thread

---

## 🐾 Adaptação ao Tema Clínica Veterinária

No enunciado original o sistema é de votação.

Neste projeto, a votação foi adaptada para:

### 📌 Sistema de Prioridade de Atendimento

Os "candidatos" agora são animais na fila de consulta.

* Eleitores = funcionários/recepção
* Admin = veterinário responsável
* Voto = animal que deve ter prioridade no atendimento

📌 Multicast é usado exclusivamente para enviar avisos administrativos.

Exemplos de aviso multicast:

* "Vacinas chegaram no estoque"
* "Clínica fecha às 17h"
* "Emergência chegando"

---

## 🔐 Usuários do sistema

### Eleitores (funcionários)

| Usuário     | Senha |
| ----------- | ----- |
| recepcao    | 123   |
| funcionario | 123   |

### Admin

| Usuário | Senha    |
| ------- | -------- |
| admin   | admin123 |

---

# 🧪 Como Rodar Questão 5

⚠️ Para testar corretamente, use **3 ou 4 terminais**.

---

## Terminal 1 — Servidor TCP (multi-thread)

```bash
python3 questao5/server.py
```

Esse servidor:

* aceita múltiplos clientes simultaneamente
* controla tempo de votação (60 segundos)
* calcula resultado e prioridade

---

## Terminal 2 — Listener Multicast (recebe avisos)

```bash
python3 questao5/multicast_listener.py
```

Esse programa simula funcionários escutando mensagens multicast.

---

## Terminal 3 — Cliente Admin

```bash
python3 questao5/client_admin.py
```

O admin pode:

* adicionar animais na fila
* remover animais
* enviar aviso multicast
* visualizar resultado da votação

---

## Terminal 4 — Cliente Eleitor

```bash
python3 questao5/client_eleitor.py
```

O eleitor pode:

* fazer login
* listar fila de consultas
* votar em um animal para ter prioridade
* visualizar resultado parcial

---

# 📌 Funcionamento do Multicast

O multicast é enviado no grupo:

* IP: `224.1.1.1`
* Porta: `5007`

📌 Apenas o admin envia mensagens UDP multicast.
📌 Todos que estiverem rodando `multicast_listener.py` recebem.

---

# 🧠 Observações Importantes

## Sobre o tempo limite da votação

O servidor permite votação por **60 segundos** após iniciar.

Depois disso:

* votos não são mais aceitos
* resultado pode ser consultado normalmente

---

## Sobre multi-thread

O servidor Questão 5 usa `threading.Thread`, permitindo múltiplos clientes simultâneos.

---

# 📌 Resumo de Execução por Questão

## Questão 2

```bash
python3 streams/test_stdout_q2.py
python3 streams/test_file_q2.py
python3 streams/server_q2_tcp.py
python3 streams/client_q2_tcp.py
```

## Questão 3

```bash
python3 streams/test_file_q3.py
python3 streams/server_q3_tcp.py
python3 streams/client_q3_tcp.py
python3 streams/test_stdin_q3.py < animais.bin
```

## Questão 4

```bash
python3 questao4/server_tcp.py
python3 questao4/client_tcp.py
```

## Questão 5

```bash
python3 questao5/server.py
python3 questao5/multicast_listener.py
python3 questao5/client_admin.py
python3 questao5/client_eleitor.py
```

---

# 📌 Conclusão

Este projeto implementa todas as etapas solicitadas no Trabalho 1,
aplicando conceitos de:

* Sockets TCP (unicast)
* Sockets UDP multicast
* Streams binários (InputStream/OutputStream)
* Serialização manual de mensagens
* Multi-threading em servidor

