#!/bin/bash
# teste_completo.sh - Testa o projeto RMI completo

echo "=== Testando projeto RMI ==="
echo ""

# Matar processos antigos
echo "1. Limpando processos antigos..."
pkill -f "server.py" 2>/dev/null
pkill -f "pyro5-ns" 2>/dev/null
sleep 2

# Ativar venv
source venv/bin/activate

# Iniciar servidor em background
echo "2. Iniciando servidor..."
cd trabalho_rmi
python server/server.py > /tmp/server_output.log 2>&1 &
SERVER_PID=$!
echo "   Servidor PID: $SERVER_PID"

# Esperar servidor iniciar
sleep 3

# Verificar se servidor está rodando
if ! ps -p $SERVER_PID > /dev/null 2>&1; then
    echo "   ERRO: Servidor não iniciou corretamente"
    cat /tmp/server_output.log
    exit 1
fi
echo "   Servidor rodando OK"

# Verificar arquivo de URI
if [ ! -f "server/server_uri.txt" ]; then
    echo "   ERRO: Arquivo server_uri.txt não criado"
    exit 1
fi
URI=$(cat server/server_uri.txt)
echo "   URI: $URI"

# Executar cliente
echo ""
echo "3. Executando cliente..."
timeout 30 python client/client.py 2>&1
CLIENT_RESULT=$?

if [ $CLIENT_RESULT -eq 0 ]; then
    echo ""
    echo "=== TESTE CONCLUÍDO COM SUCESSO ==="
else
    echo ""
    echo "=== TESTE FALHOU (código: $CLIENT_RESULT) ==="
fi

# Limpar
echo ""
echo "4. Limpando..."
kill $SERVER_PID 2>/dev/null
pkill -f "server.py" 2>/dev/null

exit $CLIENT_RESULT
