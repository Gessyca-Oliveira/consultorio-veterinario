#!/bin/bash
# teste_rmi.sh - Testa o projeto RMI completo

set -e  # Para se houver erro

echo "=== Testando Projeto RMI ==="
echo ""

# Diretório do projeto
PROJETO="/home/borges/Documents/SD/consultorio-veterinario/trabalho_rmi"
cd "$PROJETO"

# 1. Limpar processos antigos
echo "1. Limpando processos antigos..."
pkill -f "server.py" 2>/dev/null || true
pkill -f "pyro5-ns" 2>/dev/null || true
rm -f server/server_uri.txt
sleep 2

# 2. Ativar ambiente virtual
echo "2. Ativando ambiente virtual..."
source /home/borges/Documents/SD/consultorio-veterinario/venv/bin/activate

# 3. Iniciar servidor em background
echo "3. Iniciando servidor..."
cd "$PROJETO"
python server/server.py > /tmp/server.log 2>&1 &
SERVER_PID=$!
echo "   Servidor PID: $SERVER_PID"

# 4. Aguardar servidor criar arquivo URI
echo "4. Aguardando servidor iniciar..."
for i in {1..10}; do
    if [ -f "server/server_uri.txt" ]; then
        echo "   Servidor iniciado com sucesso!"
        URI=$(cat server/server_uri.txt)
        echo "   URI: $URI"
        break
    fi
    sleep 1
done

if [ ! -f "server/server_uri.txt" ]; then
    echo "   ERRO: Servidor não iniciou corretamente"
    echo "   Log do servidor:"
    cat /tmp/server.log
    exit 1
fi

# 5. Executar cliente
echo ""
echo "5. Executando cliente..."
timeout 30 python client/client.py 2>&1
CLIENT_RESULT=$?

# 6. Resultado
echo ""
if [ $CLIENT_RESULT -eq 0 ]; then
    echo "=== TESTE CONCLUÍDO COM SUCESSO ==="
else
    echo "=== TESTE FALHOU (código: $CLIENT_RESULT) ==="
fi

# 7. Limpar
echo ""
echo "6. Limpando..."
kill $SERVER_PID 2>/dev/null || true
pkill -f "server.py" 2>/dev/null || true

exit $CLIENT_RESULT
