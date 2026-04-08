# ✅ Checklist de Deploy - Gerador de Contratos

## 🎯 Resumo do Problema
**Erro 404 no Netlify** → Aplicação Next.js precisa de configuração especial

## ✅ Arquivos Criados/Modificados

### 1. `frontend/netlify.toml` ✨ NOVO
Configuração do build para Netlify com suporte ao Next.js

### 2. `frontend/next.config.js` 🔧 MODIFICADO
Adicionado:
- `output: 'standalone'`
- `images: { unoptimized: true }`

### 3. `frontend/.env.example` ✨ NOVO
Template de variáveis de ambiente

### 4. `frontend/DEPLOY_NETLIFY.md` ✨ NOVO
Guia completo de deploy

## 📋 Passo a Passo Rápido

### Deploy no Netlify (Frontend)

1. **Fazer upload do projeto corrigido** no GitHub
   
2. **Acessar Netlify**: https://app.netlify.com
   
3. **New site from Git** → Selecionar repositório
   
4. **Configurar Build**:
   ```
   Base directory: frontend
   Build command: npm run build
   Publish directory: .next
   ```

5. **Adicionar variável de ambiente** (depois de fazer deploy do backend):
   ```
   Nome: NEXT_PUBLIC_API_URL
   Valor: https://seu-backend.render.com
   ```

6. **Deploy!**

### Deploy no Render (Backend) - Recomendado

1. **Acessar Render**: https://render.com

2. **New Web Service** → Conectar GitHub

3. **Configurar**:
   ```
   Name: gerador-contratos-api
   Environment: Python 3
   Build Command: pip install -r backend/requirements.txt
   Start Command: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Adicionar variáveis de ambiente**:
   ```
   ANTHROPIC_API_KEY=sua-chave-aqui
   ENVIRONMENT=production
   ```

5. **Deploy!**

### Conectar Frontend ao Backend

1. No Netlify → **Site settings** → **Environment variables**
2. Adicionar:
   ```
   NEXT_PUBLIC_API_URL=https://seu-backend.render.com
   ```
3. **Rebuild** do site

## 🎉 Pronto!

Sua aplicação estará funcionando em:
- Frontend: `https://seu-site.netlify.app`
- Backend: `https://seu-backend.render.com`

## ⚠️ Troubleshooting Rápido

### Erro 404 persiste?
- ✅ Verifique se `netlify.toml` está na pasta `frontend/`
- ✅ Limpe cache: Site settings → Clear cache and retry deploy

### Backend não conecta?
- ✅ Verifique CORS no backend (deve permitir seu domínio Netlify)
- ✅ Confirme que `NEXT_PUBLIC_API_URL` está configurada no Netlify
- ✅ Teste a URL do backend diretamente no navegador

### Build falha?
- ✅ Teste localmente: `cd frontend && npm run build`
- ✅ Verifique logs no painel do Netlify
- ✅ Confirme todas as dependências no `package.json`

## 📞 Precisa de Ajuda?

Consulte o arquivo **DEPLOY_NETLIFY.md** para informações detalhadas!
