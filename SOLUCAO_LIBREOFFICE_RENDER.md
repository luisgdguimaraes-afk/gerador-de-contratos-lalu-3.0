# 🔧 SOLUÇÃO: Erro LibreOffice no Render

## 📋 Problema Identificado

O sistema funciona localmente porque você tem LibreOffice instalado, mas no Render (ambiente Linux) o LibreOffice não está disponível, causando o erro:

```
LibreOffice (soffice) não foi encontrado no sistema.
```

## ✅ SOLUÇÃO 1: Docker com LibreOffice (RECOMENDADA)

Esta é a solução mais robusta e profissional.

### Passo 1: Adicionar Dockerfile na raiz do projeto

Crie o arquivo `Dockerfile` na raiz do seu projeto (mesmo nível de backend/ e frontend/):

```dockerfile
# Usar imagem Python oficial
FROM python:3.11-slim

# Instalar LibreOffice e dependências necessárias
RUN apt-get update && apt-get install -y \
    libreoffice \
    libreoffice-writer \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements e instalar dependências Python
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do backend
COPY backend/ .

# Expor porta
EXPOSE 8000

# Comando para iniciar o servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Passo 2: Adicionar .dockerignore

Crie `.dockerignore` na raiz:

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv
.env
*.log
.git
.gitignore
frontend/
*.md
.DS_Store
```

### Passo 3: Configurar o Render para usar Docker

1. Acesse seu projeto no Render Dashboard
2. Vá em **Settings** do seu backend
3. Em **Build & Deploy**, mude:
   - **Environment**: Python → **Docker**
   - **Dockerfile Path**: `./Dockerfile`
4. Adicione a variável de ambiente:
   - `LIBREOFFICE_PATH` = `/usr/bin/soffice`
5. Clique em **Save Changes**
6. Faça um novo deploy (Manual Deploy > Deploy latest commit)

### Vantagens:
✅ Controle total sobre o ambiente
✅ Mesmas dependências em dev e produção
✅ Fácil de replicar
✅ Suporte nativo do Render

---

## ✅ SOLUÇÃO 2: Usar apt-buildpack do Render

Se você quiser manter a configuração Python sem Docker:

### Passo 1: Criar Aptfile

Crie o arquivo `Aptfile` na raiz do projeto:

```
libreoffice
libreoffice-writer
```

### Passo 2: Configurar Build Command no Render

No Render Dashboard > Settings > Build & Deploy:

**Build Command:**
```bash
pip install -r backend/requirements.txt
```

**Start Command:**
```bash
cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Passo 3: Adicionar variável de ambiente

Adicione em Environment Variables:
- `LIBREOFFICE_PATH` = `/usr/bin/soffice`

### Vantagens:
✅ Não precisa de Docker
✅ Configuração mais simples
⚠️ Menos controle sobre versões

---

## ✅ SOLUÇÃO 3: render.yaml (Infrastructure as Code)

Para projetos maiores, use `render.yaml`:

### Criar render.yaml na raiz:

```yaml
services:
  - type: web
    name: gerador-contratos-backend
    env: docker
    dockerfilePath: ./Dockerfile
    region: oregon
    plan: free
    envVars:
      - key: LIBREOFFICE_PATH
        value: /usr/bin/soffice
      - key: OPENAI_API_KEY
        sync: false
```

### Vantagens:
✅ Configuração versionada
✅ Fácil replicação
✅ Documentação automática

---

## 🚀 IMPLEMENTAÇÃO RÁPIDA

### Se você quer resolver AGORA (5 minutos):

1. **Crie o Dockerfile** (copie o conteúdo acima)
2. **Crie o .dockerignore** (copie o conteúdo acima)
3. **Commit e push para o GitHub:**
   ```bash
   git add Dockerfile .dockerignore
   git commit -m "Add Docker support with LibreOffice"
   git push
   ```
4. **No Render Dashboard:**
   - Settings > Environment = **Docker**
   - Dockerfile Path = `./Dockerfile`
   - Add Environment Variable: `LIBREOFFICE_PATH` = `/usr/bin/soffice`
   - Save Changes
5. **Deploy Manual** (Deploy latest commit)

---

## 🔍 VERIFICAÇÃO

Após o deploy, teste enviando uma requisição. Você deve ver nos logs:

```
Convertendo via LibreOffice: ['/usr/bin/soffice', '--headless', ...]
PDF gerado com sucesso: ...
```

---

## ⚠️ ALTERNATIVAS NÃO RECOMENDADAS

### Opção A: Biblioteca Python pura (docx2pdf)
❌ **NÃO funciona em Linux** sem LibreOffice ou MS Word instalado
❌ Requer Microsoft Word no Windows
❌ Não é portável

### Opção B: Serviços externos (Cloudconvert, PDFShift)
💰 Requer pagamento
🔐 Envia documentos para terceiros
⚠️ Dependência externa

---

## 📊 COMPARAÇÃO DAS SOLUÇÕES

| Solução | Dificuldade | Tempo | Custo | Recomendação |
|---------|-------------|-------|-------|--------------|
| 1. Docker | ⭐⭐ | 10 min | Grátis | ⭐⭐⭐⭐⭐ |
| 2. Aptfile | ⭐ | 5 min | Grátis | ⭐⭐⭐⭐ |
| 3. render.yaml | ⭐⭐ | 15 min | Grátis | ⭐⭐⭐⭐⭐ |

---

## 🆘 TROUBLESHOOTING

### Se ainda der erro após implementar:

**Erro: "Permission denied"**
```yaml
# No Dockerfile, adicione antes do CMD:
RUN chmod +x /usr/bin/soffice
```

**Erro: "Display não disponível"**
✅ Já está correto - estamos usando `--headless`

**Erro: "Timeout na conversão"**
```python
# Aumentar timeout em pdf_generator.py, linha 104:
timeout=300,  # 5 minutos
```

**Erro: "Arquivo muito grande"**
- Verifique o tamanho dos templates DOCX
- Otimize imagens dentro dos templates
- Considere upgrade do plano Render

---

## 📝 CHECKLIST PRÉ-DEPLOY

- [ ] Dockerfile criado na raiz
- [ ] .dockerignore criado
- [ ] Arquivos commitados no Git
- [ ] Push feito para o repositório
- [ ] Render configurado para usar Docker
- [ ] Variável LIBREOFFICE_PATH adicionada
- [ ] Deploy manual iniciado
- [ ] Logs verificados (procure por "LibreOffice")
- [ ] Teste de conversão realizado

---

## 💡 PRÓXIMOS PASSOS APÓS CORREÇÃO

1. **Adicionar monitoramento de erros** (Sentry)
2. **Cache de PDFs** para evitar reconversões
3. **Otimizar templates** para conversão mais rápida
4. **Adicionar testes automatizados**

---

## 📞 SUPORTE

Se ainda tiver problemas:
1. Verifique os logs do Render em tempo real
2. Confirme que LibreOffice foi instalado (`which soffice` nos logs)
3. Teste localmente com Docker antes de fazer deploy

```bash
# Testar localmente:
docker build -t gerador-contratos .
docker run -p 8000:8000 gerador-contratos
```

---

**Boa sorte! 🚀**
