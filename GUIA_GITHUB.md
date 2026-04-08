# 🚀 Guia Completo: Hospedando o Projeto no GitHub

Este guia vai te ajudar a hospedar o projeto "Contratos LALU" no GitHub de forma segura e organizada.

## 📑 Índice Rápido

1. [Pré-requisitos](#-pré-requisitos)
2. [Verificar Instalação do Git](#-verificar-instalação-do-git)
3. [Configurar Git](#-passo-1-configurar-git-primeira-vez-apenas)
4. [Criar Repositório no GitHub](#-passo-2-criar-repositório-no-github)
5. [Conectar Repositório Local ao GitHub](#-passo-3-conectar-repositório-local-ao-github)
6. [Criar Arquivos .env.example](#-passo-6-criar-arquivos-envexample-opcional-mas-recomendado)
7. [Trabalhando com o Repositório](#-passo-7-trabalhando-com-o-repositório-futuro)
8. [Solução de Problemas](#-solução-de-problemas)

---

## 📋 Pré-requisitos

Antes de começar, você precisa ter:

1. ✅ Uma conta no GitHub ([criar conta](https://github.com/signup))
2. ✅ Git instalado no seu computador
   - **Windows**: Baixe em [git-scm.com](https://git-scm.com/download/win)
   - **Mac**: `brew install git` ou baixe em [git-scm.com](https://git-scm.com/download/mac)
   - **Linux**: `sudo apt-get install git`

## 🔍 Verificar Instalação do Git

Abra o terminal (PowerShell no Windows) e execute:

```bash
git --version
```

Se aparecer uma versão (ex: `git version 2.42.0`), está tudo certo! ✅

## 📝 Passo 1: Configurar Git (Primeira vez apenas)

Se você nunca usou Git neste computador, configure seu nome e email:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```

**Importante**: Use o mesmo email da sua conta GitHub!

## 📦 Passo 2: Criar Repositório no GitHub

1. Acesse [github.com](https://github.com) e faça login
2. Clique no botão **"+"** no canto superior direito
3. Selecione **"New repository"**
4. Preencha os dados:
   - **Repository name**: `contratos-lalu` (ou o nome que preferir)
   - **Description**: "Sistema de geração automática de contratos com IA"
   - **Visibility**: Escolha **Public** (público) ou **Private** (privado)
   - ⚠️ **NÃO marque** "Initialize this repository with a README" (já temos um)
5. Clique em **"Create repository"**

## 🔗 Passo 3: Conectar Repositório Local ao GitHub

No terminal, navegue até a pasta do projeto:

```bash
cd "C:\Users\luisg\Downloads\Contratos LALU\Contratos LALU"
```

### 3.1. Verificar Status do Git

Primeiro, vamos verificar se já existe um repositório Git:

```bash
git status
```

**Se aparecer erro**: O Git ainda não foi inicializado. Continue para o passo 3.2.

**Se aparecer lista de arquivos**: O Git já está inicializado. Pule para o passo 3.3.

### 3.2. Inicializar Repositório Git (se necessário)

```bash
git init
```

### 3.3. Verificar Arquivos que Serão Adicionados

```bash
git status
```

Você deve ver uma lista de arquivos não rastreados. Arquivos como `.env`, `node_modules/`, `temp/` e `output/` **NÃO devem aparecer** (estão no `.gitignore`).

**⚠️ VERIFICAÇÃO DE SEGURANÇA**: Antes de continuar, verifique se arquivos sensíveis não estão sendo rastreados:

```bash
# Verificar se .env está sendo ignorado (deve retornar o caminho)
git check-ignore backend/.env

# Verificar se arquivos temporários estão sendo ignorados
git check-ignore backend/temp/
git check-ignore backend/output/

# Se algum arquivo sensível aparecer em "git status", NÃO continue!
# Adicione ao .gitignore primeiro.
```

### 3.4. Adicionar Todos os Arquivos

```bash
git add .
```

### 3.5. Criar Primeiro Commit

```bash
git commit -m "Initial commit: Sistema de geração de contratos com IA"
```

### 3.6. Renomear Branch Principal (se necessário)

```bash
git branch -M main
```

### 3.7. Adicionar Repositório Remoto

Substitua `SEU_USUARIO` pelo seu nome de usuário do GitHub e `NOME_DO_REPOSITORIO` pelo nome que você escolheu:

```bash
git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
```

**Exemplo**:
```bash
git remote add origin https://github.com/luisg/contratos-lalu.git
```

### 3.8. Enviar Código para o GitHub

```bash
git push -u origin main
```

Você será solicitado a fazer login no GitHub. Siga as instruções na tela.

## ✅ Passo 4: Verificar Upload

1. Acesse seu repositório no GitHub (ex: `https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO`)
2. Você deve ver todos os arquivos do projeto lá!

## 🔒 Passo 5: Segurança - Arquivos Sensíveis

### ⚠️ IMPORTANTE: Nunca faça commit de:

- ❌ Arquivos `.env` (contém chaves de API)
- ❌ Arquivos `.env.local`
- ❌ Arquivos temporários (`temp/`, `output/`)
- ❌ Arquivos de contrato gerados (`*.docx`, `*.pdf`)

**Boa notícia**: O arquivo `.gitignore` já está configurado para ignorar esses arquivos automaticamente! ✅

### Verificar se arquivos sensíveis estão protegidos:

```bash
# Verificar se .env está sendo ignorado
git check-ignore backend/.env

# Se retornar o caminho, está protegido ✅
# Se não retornar nada, adicione ao .gitignore
```

## 📝 Passo 6: Criar Arquivos .env.example (Opcional mas Recomendado)

Para ajudar outros desenvolvedores, crie arquivos de exemplo com as variáveis de ambiente necessárias:

### 6.1. Executar Script Automático (Recomendado):

```powershell
# Execute o script PowerShell que cria os arquivos automaticamente
.\criar_env_example.ps1
```

### 6.2. Ou Criar Manualmente:

**Criar `backend/.env.example`:**

```powershell
New-Item backend\.env.example
```

Adicione o seguinte conteúdo:

```env
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
LIBREOFFICE_PATH=
```

**Criar `frontend/.env.local.example`:**

```powershell
New-Item frontend\.env.local.example
```

Adicione:

```env
# URL da API do backend
# Em desenvolvimento local, geralmente é http://localhost:8000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 6.3. Fazer commit dos arquivos de exemplo:

```bash
git add backend/.env.example frontend/.env.local.example
git commit -m "docs: Adicionar arquivos .env.example para configuração"
git push
```

## 🔄 Passo 7: Trabalhando com o Repositório (Futuro)

### Fazer alterações e enviar:

```bash
# 1. Ver o que mudou
git status

# 2. Adicionar arquivos modificados
git add .

# 3. Criar commit com mensagem descritiva
git commit -m "feat: Adicionar nova funcionalidade X"

# 4. Enviar para o GitHub
git push
```

### Atualizar código do GitHub:

```bash
git pull
```

## 📚 Recursos Adicionais

### Comandos Git Úteis:

```bash
# Ver histórico de commits
git log

# Ver diferenças não commitadas
git diff

# Ver branches
git branch

# Criar nova branch
git checkout -b nome-da-branch

# Voltar para branch main
git checkout main
```

## 🆘 Solução de Problemas

### Erro: "fatal: not a git repository"

**Solução**: Execute `git init` na pasta do projeto.

### Erro: "fatal: remote origin already exists"

**Solução**: Remova e adicione novamente:
```bash
git remote remove origin
git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
```

### Erro: "Permission denied" ao fazer push

**Soluções**:
1. Verifique se você está logado no GitHub
2. Use autenticação por token: [GitHub Personal Access Token](https://github.com/settings/tokens)
3. Configure SSH: [GitHub SSH Setup](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

### Arquivos sensíveis foram commitados acidentalmente

**Solução**: Remova do histórico (cuidado!):
```bash
# Remover arquivo do Git mas manter localmente
git rm --cached backend/.env

# Fazer commit da remoção
git commit -m "fix: Remover arquivo sensível do repositório"

# Adicionar ao .gitignore (se ainda não estiver)
echo "backend/.env" >> .gitignore

# Fazer push
git push
```

## ✅ Checklist Final

Antes de fazer push, verifique:

- [ ] Git está instalado e configurado (`git --version`)
- [ ] Repositório foi criado no GitHub
- [ ] `.gitignore` está configurado corretamente
- [ ] Arquivos `.env` não estão sendo rastreados (`git check-ignore backend/.env`)
- [ ] Arquivos temporários (`temp/`, `output/`) não estão sendo rastreados
- [ ] `node_modules/` não está sendo rastreado
- [ ] Arquivos de contrato (`*.docx`, `*.pdf`) não estão sendo rastreados
- [ ] Arquivos `.env.example` foram criados (opcional mas recomendado)
- [ ] README.md está atualizado
- [ ] Código está funcionando localmente
- [ ] Commit inicial foi criado com mensagem descritiva

## 🎉 Pronto!

Seu projeto está agora no GitHub! 🚀

Você pode:
- Compartilhar o link do repositório
- Colaborar com outros desenvolvedores
- Usar GitHub Actions para CI/CD
- Fazer deploy automático
- Controlar versões do código

---

**Dúvidas?** Consulte a [documentação oficial do Git](https://git-scm.com/doc) ou [GitHub Docs](https://docs.github.com/).
