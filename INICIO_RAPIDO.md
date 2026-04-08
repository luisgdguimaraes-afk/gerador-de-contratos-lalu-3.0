# 🚀 Início Rápido - Sistema de Análise de Contratos

## Status da Aplicação

✅ **Frontend**: Rodando em http://localhost:3000
❌ **Backend**: Precisa de configuração da OPENAI_API_KEY

## ⚠️ Configuração Necessária

### 1. Configurar OpenAI API Key

1. Abra o arquivo `backend/.env`
2. Substitua `your_openai_api_key_here` pela sua chave real da OpenAI
3. Para obter uma chave:
   - Acesse https://platform.openai.com/
   - Faça login ou crie uma conta
   - Vá em "API Keys" → "Create new secret key"
   - Copie a chave e cole no arquivo `.env`

### 2. Reiniciar o Backend

Após configurar a chave, execute:

```powershell
cd "C:\Users\Bieda\Downloads\Contratos LALU\backend"
python run.py
```

Ou use:

```powershell
cd backend
uvicorn app.main:app --reload --port 8000
```

## 📋 Verificação

Após configurar, verifique se ambos os servidores estão rodando:

- **Frontend**: http://localhost:3000 ✅
- **Backend**: http://localhost:8000 (verifique após configurar a API key)

## 🎯 Como Usar

1. Acesse http://localhost:3000 no navegador
2. Faça upload de um arquivo DOCX de contrato
3. O sistema irá:
   - Analisar o documento automaticamente
   - Identificar campos editáveis
   - Gerar um formulário dinâmico
4. Preencha os campos
5. Baixe o documento preenchido em DOCX ou PDF

## 🔧 Solução de Problemas

### Backend não inicia
- Verifique se o arquivo `.env` existe em `backend/`
- Verifique se `OPENAI_API_KEY` está configurada corretamente
- Verifique se todas as dependências foram instaladas: `pip list`

### Erro de API Key
- Certifique-se de que a chave está correta
- Verifique se há créditos disponíveis na conta OpenAI
- Tente usar `gpt-3.5-turbo` em vez de `gpt-4` (edite `backend/app/services/ai_analyzer.py`)

### Frontend não conecta ao backend
- Verifique se o backend está rodando na porta 8000
- Verifique o console do navegador (F12) para erros
- Verifique se há problemas de CORS

## 📝 Notas

- O backend precisa da OpenAI API Key para funcionar
- A primeira análise pode demorar alguns segundos
- Arquivos são temporários e serão removidos após o processamento
- Para produção, configure variáveis de ambiente adequadamente
