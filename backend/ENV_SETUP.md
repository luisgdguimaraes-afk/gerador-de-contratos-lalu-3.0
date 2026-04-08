# Configuração de Variáveis de Ambiente

Crie um arquivo `.env` na raiz do diretório `backend/` com o seguinte conteúdo:

```env
# OpenAI API Key (obrigatório)
OPENAI_API_KEY=your_openai_api_key_here

# Modelo OpenAI (opcional, padrão: gpt-4o-mini)
# Opções: gpt-4o-mini, gpt-4o, gpt-3.5-turbo
OPENAI_MODEL=gpt-4o-mini

# Configuração do Servidor (opcional)
PORT=8000
HOST=0.0.0.0

# Diretório de arquivos temporários (opcional)
TEMP_DIR=./temp
```

## Como obter a OpenAI API Key

1. Acesse https://platform.openai.com/
2. Faça login ou crie uma conta
3. Vá em "API Keys" no menu
4. Clique em "Create new secret key"
5. Copie a chave e cole no arquivo `.env`

## Nota

- Nunca commite o arquivo `.env` no repositório
- O arquivo `.env` está no `.gitignore` por padrão
- Para produção, use variáveis de ambiente do sistema ou um gerenciador de secrets
