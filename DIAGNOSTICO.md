# 🔍 Guia de Diagnóstico de Erros

## Erro: "Erro ao processar documento"

Este erro pode ter várias causas. Siga este guia para identificar e resolver:

### 1. Verificar se o Backend está rodando

```powershell
# Verificar se o backend responde
Invoke-WebRequest -Uri "http://localhost:8000/health"
```

**Se não responder:**
- Execute: `cd backend; python run.py`
- Verifique se há erros no console

### 2. Verificar API Key da OpenAI

```powershell
# Verificar se a API key está configurada
cd backend
Get-Content .env | Select-String "OPENAI_API_KEY"
```

**Se não estiver configurada:**
- Edite `backend/.env`
- Adicione: `OPENAI_API_KEY=sua_chave_aqui`
- Reinicie o backend

### 3. Verificar Logs do Backend

Quando você faz upload, o backend deve mostrar logs como:
```
Recebendo upload: arquivo.docx (ID: ...)
Arquivo salvo em: ...
Extraindo texto do documento: ...
Texto extraído: X caracteres
Placeholders encontrados: X
Iniciando análise com IA...
Enviando requisição para OpenAI com modelo: gpt-4o-mini
```

**Se aparecer erro sobre API Key:**
- Verifique se a chave está correta
- Verifique se há créditos na conta OpenAI

**Se aparecer erro sobre modelo:**
- O modelo pode não estar disponível
- Edite `backend/app/services/ai_analyzer.py`
- Altere `self.model = "gpt-4o-mini"` para `self.model = "gpt-3.5-turbo"`

### 4. Erros Comuns

#### "OPENAI_API_KEY não configurada"
- **Solução**: Configure a chave no arquivo `backend/.env`

#### "Rate limit exceeded"
- **Solução**: Aguarde alguns minutos e tente novamente

#### "Insufficient quota"
- **Solução**: Adicione créditos à sua conta OpenAI

#### "Model not found"
- **Solução**: Altere o modelo para `gpt-3.5-turbo` em `ai_analyzer.py`

#### "Documento não encontrado"
- **Solução**: O arquivo pode não ter sido salvo corretamente. Tente fazer upload novamente.

### 5. Testar Manualmente

```powershell
# Testar upload via curl (se tiver curl instalado)
curl -X POST "http://localhost:8000/api/upload" -F "file=@seu_arquivo.docx"

# Ou usar PowerShell
$filePath = "caminho\para\seu\arquivo.docx"
$form = @{
    file = Get-Item $filePath
}
Invoke-RestMethod -Uri "http://localhost:8000/api/upload" -Method Post -Form $form
```

### 6. Verificar Console do Navegador

1. Abra o DevTools (F12)
2. Vá na aba "Console"
3. Faça upload novamente
4. Veja os erros detalhados

### 7. Verificar Arquivo DOCX

- Certifique-se de que o arquivo é um DOCX válido
- Tente abrir o arquivo no Word para verificar se não está corrompido
- Verifique o tamanho do arquivo (muito grande pode causar problemas)

### 8. Modo de Fallback

Se a IA falhar, o sistema deve usar campos básicos. Se isso não acontecer, pode haver um erro no código.

### 9. Contatar Suporte

Se nenhuma das soluções funcionar:
1. Copie os logs do backend
2. Copie os erros do console do navegador
3. Verifique a versão do Python: `python --version` (deve ser 3.9+)
4. Verifique as dependências: `pip list`

## Logs Úteis

Os logs do backend mostram:
- ✅ Upload recebido
- ✅ Arquivo salvo
- ✅ Texto extraído
- ✅ Placeholders encontrados
- ✅ Requisição para OpenAI
- ❌ Qualquer erro que ocorrer

Use esses logs para identificar onde o processo está falhando.
