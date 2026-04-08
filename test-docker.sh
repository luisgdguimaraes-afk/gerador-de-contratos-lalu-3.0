#!/bin/bash
# Script para testar o Docker localmente antes do deploy

echo "🐳 Testando Docker com LibreOffice..."
echo ""

# Build da imagem
echo "📦 1. Construindo imagem Docker..."
docker build -t gerador-contratos-test .

if [ $? -ne 0 ]; then
    echo "❌ Erro ao construir imagem Docker"
    exit 1
fi

echo "✅ Imagem construída com sucesso!"
echo ""

# Verificar se LibreOffice está instalado
echo "🔍 2. Verificando instalação do LibreOffice..."
docker run --rm gerador-contratos-test which soffice

if [ $? -ne 0 ]; then
    echo "❌ LibreOffice não encontrado na imagem"
    exit 1
fi

echo "✅ LibreOffice instalado corretamente!"
echo ""

# Testar versão do LibreOffice
echo "📋 3. Versão do LibreOffice:"
docker run --rm gerador-contratos-test soffice --version
echo ""

# Iniciar container
echo "🚀 4. Iniciando container..."
echo "   Servidor estará disponível em: http://localhost:8000"
echo "   Pressione Ctrl+C para parar"
echo ""

docker run --rm -p 8000:8000 \
    -e OPENAI_API_KEY="${OPENAI_API_KEY}" \
    -e LIBREOFFICE_PATH="/usr/bin/soffice" \
    gerador-contratos-test
