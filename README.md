#  Sistema Clínica Veterinária — Trabalho 1 (Sistemas Distribuídos)

 **Universidade Federal do Ceará — Campus Quixadá** 
 **Disciplina:** Sistemas Distribuídos 
 **Docente:** Antônio Rafael Braga 
 **Discentes:** Alfredo Borges do Nascimento Neto | Gessyca de Oliveira Cunha
 **Trabalho 1:** Comunicação entre processos
 **Tema:** **Clínica Veterinária** 
 **Linguagem:** **Python 3** 
 **Tecnologias:** TCP Sockets, UDP Multicast, Streams, JSON, Multi-thread 

---

#  Visão Geral do Projeto

Este projeto implementa um sistema distribuído baseado em uma **Clínica Veterinária**, seguindo as questões do Trabalho 1.

O objetivo principal é demonstrar conceitos de:

 Comunicação **TCP (unicast)** cliente-servidor 
 Comunicação **UDP Multicast** (mensagens em grupo) 
 Criação de streams customizados (InputStream/OutputStream) 
 Serialização de dados (JSON e bytes) 
 Servidor concorrente com **multi-thread** 

---

#  Pré-requisitos

- Python 3.8+ (recomendado 3.10+)

```bash
python3 --version
```

---

#  Como Rodar o Projeto

 **IMPORTANTE:** 
Sempre execute os comandos a partir da raiz do projeto:

```
~/Documents/SD/consultorio-veterinario-back
```

E sempre utilize:

 `PYTHONPATH=src`

Isso faz o Python reconhecer `src/` como raiz dos imports.

---

#  Portas Utilizadas no Projeto

| Questão | Tipo | Porta |
|--------|------|-------|
| Q2 TCP | TCP | 9001 |
| Q3 TCP | TCP | 9002 |
| Q4 TCP | TCP | 9010 |
| Q5 TCP | TCP | 9020 |
| Q5 Multicast | UDP | 5007 |
| Q5 Multicast Group | IP | 224.1.1.1 |

---

#  Como Liberar Todas as Portas de Uma Vez

Se você receber erro de porta ocupada (**Address already in use**), rode:

```bash
sudo fuser -k 9001/tcp 9002/tcp 9010/tcp 9020/tcp 5007/udp
```

 Isso mata todos os processos presos nessas portas.

---

#  Questão 1 — POJOs e Modelos (Classes do Sistema)

##  Objetivo
Criar classes que representam o sistema de uma clínica veterinária.

 Implementado:

-  Superclasse: `Animal`
-  Subclasse: `Cachorro`
-  Subclasse: `Gato`
-  Subclasse: `Coelho`
-  Agregação: `Estoque`
-  Interface/Entidade: `Consulta`
-  Serviços:
  - `ServicoConsulta`
  - `ServicoEstoque`

 Essa questão não tem execução direta. 
Ela é a base para o restante do projeto.

---

#  Questão 2 — OutputStream (Envio binário de objetos)

##  Objetivo
Criar um stream de saída chamado:

 `AnimalOutputStream`

Ele envia um **array de objetos Animal** (Cachorro/Gato/Coelho) como bytes.

---

##  Como o protocolo funciona

O stream envia:

1.  quantidade de objetos
2. Para cada animal:
   - tamanho do campo em bytes
   - conteúdo do campo em bytes

Campos enviados:
- tipo do animal
- nome
- idade
- atributo extra (raça/cor/peso)

 Isso permite reconstruir o objeto depois.

---

## Rodar Questão 2

###  Teste 1: stdout (imprime bytes no terminal)

```bash
PYTHONPATH=src python3 -m streams.test_stdout_q2
```

 Vai aparecer texto "estranho" porque são bytes binários.

---

###  Teste 2: arquivo binário (gera `animais.bin`)

```bash
PYTHONPATH=src python3 -m streams.test_file_q2
```

 Gera o arquivo:
- `animais.bin`

---

###  Teste 3: TCP (cliente envia bytes para servidor)

#### Terminal 1 (Servidor TCP)

```bash
PYTHONPATH=src python3 -m streams.server_q2_tcp
```

#### Terminal 2 (Cliente TCP)

```bash
PYTHONPATH=src python3 -m streams.client_q2_tcp
```

 Resultado:
- servidor recebe bytes e salva `animais_tcp.bin`

---

#  Questão 3 — InputStream (Leitura e reconstrução)

##  Objetivo
Criar um stream de entrada chamado:

 `AnimalInputStream`

Ele lê os bytes gerados na Questão 2 e reconstrói os objetos.

---

##  Rodar Questão 3

###  Teste 1: Ler arquivo `animais.bin`

 Primeiro gere o arquivo (Questão 2):

```bash
PYTHONPATH=src python3 -m streams.test_file_q2
```

 Depois leia:

```bash
PYTHONPATH=src python3 -m streams.test_file_q3
```

---

###  Teste 2: Ler via stdin (entrada padrão)

```bash
PYTHONPATH=src python3 -m streams.test_stdin_q3 < animais.bin
```

---

###  Teste 3: Ler via TCP

#### Terminal 1 (Servidor)

```bash
PYTHONPATH=src python3 -m streams.server_q3_tcp
```

#### Terminal 2 (Cliente)

```bash
PYTHONPATH=src python3 -m streams.client_q3_tcp
```

 O servidor imprime os animais reconstruídos.

---

#  Questão 4 — Serialização Cliente-Servidor (TCP + JSON)

##  Objetivo
Criar um serviço remoto cliente-servidor via TCP.

 A comunicação usa JSON e é serializada como:

- 4 bytes (tamanho da mensagem)
- mensagem JSON em bytes

Isso é implementado no arquivo:

 `utils/serializer.py`

Funções principais:
- `send_json()` → empacota e envia JSON
- `recv_json()` → recebe e desempacota JSON

---

##  Rodar Questão 4

### Terminal 1 (Servidor)

```bash
PYTHONPATH=src python3 -m questao4.server_tcp
```

### Terminal 2 (Cliente)

```bash
PYTHONPATH=src python3 -m questao4.client_tcp
```

 O cliente faz requisições como:
- listar animais
- buscar animal por nome

---

#  Questão 5 — Sistema Distribuído Completo (TCP + Multicast UDP)

##  Objetivo
Implementar um sistema distribuído completo, contendo:

Login via TCP 
Lista de candidatos via TCP 
Envio de voto via TCP 
Notas informativas via UDP Multicast 
Servidor multi-thread 

---

#  Adaptação ao Tema Clínica Veterinária

No enunciado, existe votação de candidatos.

Aqui, isso foi adaptado para:

##  Sistema de Prioridade de Atendimento

 "Candidatos" = animais na fila de consulta 
 "Eleitor" = recepção/funcionário 
 "Admin" = administrador/veterinário 
 "Voto" = escolher qual animal deve ser atendido primeiro 

O servidor calcula:
- total de votos
- percentual de cada animal
- animal com maior prioridade

---

#  Multicast UDP (Avisos)

 O admin pode enviar avisos para todos os funcionários conectados.

Exemplos:
- "Vacinas chegaram no estoque"
- "Clínica fecha às 17h"
- "Emergência chegando"

Multicast:
- Grupo: `224.1.1.1`
- Porta: `5007`

---

#  Usuários cadastrados

### Eleitores (funcionários)

| Usuário | Senha |
|--------|------|
| recepcao | 123 |
| funcionario | 123 |

### Admin

| Usuário | Senha |
|--------|------|
| admin | admin123 |

---

#  Rodar Questão 5 (modo completo)

 Para testar corretamente, use **4 terminais**.

---

## Terminal 1 — Servidor TCP multi-thread

```bash
PYTHONPATH=src python3 -m questao5.server
```

---

## Terminal 2 — Listener Multicast (recebe avisos)

```bash
PYTHONPATH=src python3 -m questao5.multicast_listener
```

---

## Terminal 3 — Admin (gerencia fila e envia avisos)

```bash
PYTHONPATH=src python3 -m questao5.client_admin
```

Login:
- admin / admin123

---

## Terminal 4 — Eleitor (funcionário votando)

```bash
PYTHONPATH=src python3 -m questao5.client_eleitor
```

Login:
- recepcao / 123

---

#  Fluxo Geral do Projeto (Resumo Visual)

##  Questão 2 e 3 (Streams)
 Objetos Animal → bytes → arquivo/TCP → bytes → objetos Animal

```
AnimalOutputStream  --->  arquivo/TCP  --->  AnimalInputStream
```

---

##  Questão 4 (TCP JSON)
 Cliente envia JSON e servidor responde JSON

```
Cliente TCP ---> Request JSON ---> Servidor TCP
Cliente TCP <--- Reply JSON  <--- Servidor TCP
```

---

##  Questão 5 (TCP + Multicast UDP)
 Login e voto via TCP, avisos via multicast

```
Eleitor (TCP)  ---> login/voto ---> Servidor
Admin (TCP)    ---> gerencia    ---> Servidor
Admin (UDP)    ---> aviso multicast ---> Todos os ouvintes
```

---

#  Conclusão

Este projeto atende completamente ao enunciado do Trabalho 1, aplicando:

 Streams binários customizados 
 Comunicação TCP com serialização JSON 
 Comunicação UDP Multicast para mensagens em grupo 
 Servidor multi-thread para múltiplos clientes 
 Aplicação baseada no tema Clínica Veterinária 