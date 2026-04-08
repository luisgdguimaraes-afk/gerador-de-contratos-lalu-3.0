# Script para criar arquivos .env.example
# Execute este script antes de fazer commit no GitHub

# Criar backend/.env.example
$backendEnvExample = @"
# OpenAI API Key (obrigatório)
# Obtenha sua chave em: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# Modelo OpenAI (opcional, padrão: gpt-4o-mini)
# Opções: gpt-4o-mini, gpt-4o, gpt-3.5-turbo
OPENAI_MODEL=gpt-4o-mini

# Configuração do Servidor (opcional)
PORT=8000
HOST=0.0.0.0

# Diretório de arquivos temporários (opcional)
TEMP_DIR=./temp

# Caminho do LibreOffice (opcional, apenas se não estiver no PATH)
# Windows: C:\Program Files\LibreOffice\program\soffice.exe
# Linux/Mac: geralmente já está no PATH
LIBREOFFICE_PATH=
"@

# Criar frontend/.env.local.example
$frontendEnvExample = @"
# URL da API do backend
# Em desenvolvimento local, geralmente é http://localhost:8000
NEXT_PUBLIC_API_URL=http://localhost:8000
"@

# Escrever arquivos
$backendEnvExample | Out-File -FilePath "backend\.env.example" -Encoding UTF8
$frontendEnvExample | Out-File -FilePath "frontend\.env.local.example" -Encoding UTF8

Write-Host "✅ Arquivos .env.example criados com sucesso!" -ForegroundColor Green
Write-Host "   - backend/.env.example" -ForegroundColor Cyan
Write-Host "   - frontend/.env.local.example" -ForegroundColor Cyan
