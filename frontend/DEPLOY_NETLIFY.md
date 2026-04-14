# 🚀 Guia de Deploy no Netlify

## Problema do Erro 404

O erro 404 acontece porque o Next.js é uma aplicação que precisa de Server-Side Rendering (SSR) e o Netlify por padrão serve apenas sites estáticos.

## ✅ Solução Implementada

1. **Arquivo `netlify.toml` na raiz do repositório** - `base = "frontend"`, build e plugin Next.js
2. **`next.config.js` atualizado** - Otimizado para deploy no Netlify

## 📋 Passo a Passo para Deploy

### Opção 1: Deploy via Interface do Netlify (Recomendado)

1. **Acesse o Netlify** em https://www.netlify.com
2. Faça login ou crie uma conta
3. Clique em **"Add new site"** > **"Import an existing project"**
4. Conecte seu repositório GitHub/GitLab/Bitbucket
5. Configure o build:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `.next`
6. Clique em **"Deploy site"**

### Opção 2: Deploy via Netlify CLI

```bash
# Instale a CLI do Netlify
npm install -g netlify-cli

# Navegue para a pasta do frontend
cd frontend

# Faça login no Netlify
netlify login

# Inicialize o site
netlify init

# Faça o deploy
netlify deploy --prod
```

## 🔧 Estrutura de Arquivos Criados

### `netlify.toml`
```toml
[build]
  command = "npm run build"
  publish = ".next"

[[plugins]]
  package = "@netlify/plugin-nextjs"
```

Este arquivo:
- Define o comando de build
- Especifica o diretório de publicação
- Habilita o plugin oficial do Next.js para Netlify

### `next.config.js` (atualizado)
```javascript
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  images: {
    unoptimized: true,
  },
}
```

Configurações adicionadas:
- `output: 'standalone'` - Gera um build otimizado
- `images: { unoptimized: true }` - Desabilita otimização de imagens (o Netlify tem seu próprio sistema)

## ⚠️ Importante: Backend

Esta aplicação tem um **backend FastAPI** que **NÃO PODE** ser hospedado no Netlify (que é apenas para frontend).

### Opções para o Backend:

1. **Render.com** (Recomendado - Gratuito)
   - Deploy gratuito
   - Suporta Python/FastAPI
   - https://render.com

2. **Railway.app**
   - Fácil integração
   - Suporte a Python
   - https://railway.app

3. **Heroku** (Pago)
   - Tradicional
   - Boa documentação

4. **AWS/GCP/Azure** (Mais complexo)
   - Para produção robusta

### Configuração do Frontend com Backend Separado

Você precisará atualizar a URL da API no arquivo `frontend/lib/api.ts`:

```typescript
// Altere de:
const API_URL = 'http://localhost:8000'

// Para:
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://seu-backend.render.com'
```

E adicionar a variável de ambiente no Netlify:
- Site settings > Environment variables
- Adicione: `NEXT_PUBLIC_API_URL` = `https://seu-backend.render.com`

## 🔍 Troubleshooting

### Erro 404 persiste?
1. Verifique se o `netlify.toml` está na pasta raiz do projeto
2. Confirme que a pasta base está configurada como `frontend`
3. Limpe o cache do Netlify: Site settings > Build & deploy > Clear cache and retry deploy

### Build falha?
1. Verifique se todas as dependências estão no `package.json`
2. Teste o build localmente: `npm run build`
3. Verifique os logs de erro no painel do Netlify

### Rotas não funcionam?
- O plugin `@netlify/plugin-nextjs` resolve isso automaticamente
- Se persistir, adicione ao `netlify.toml`:
```toml
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

## 📚 Recursos Adicionais

- [Documentação Next.js no Netlify](https://docs.netlify.com/integrations/frameworks/next-js/)
- [Plugin @netlify/plugin-nextjs](https://www.npmjs.com/package/@netlify/plugin-nextjs)
- [Netlify Deploy Docs](https://docs.netlify.com/site-deploys/overview/)

## ✨ Próximos Passos

1. ✅ Deploy do Frontend no Netlify (com os arquivos criados)
2. 🔄 Deploy do Backend no Render/Railway
3. 🔗 Conectar Frontend ao Backend via variáveis de ambiente
4. 🧪 Testar a aplicação completa

Qualquer dúvida, estou aqui para ajudar! 🚀
