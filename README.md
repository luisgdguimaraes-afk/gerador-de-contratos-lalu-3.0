# Sistema de Geração de Contratos

Aplicação web completa para análise inteligente e preenchimento automático de contratos DOCX.

## 🎯 Objetivo

Sistema que recebe contratos em formato DOCX, identifica automaticamente campos editáveis, gera labels inteligentes e semânticos, cria um formulário dinâmico e permite o download do documento preenchido em PDF.

## ✨ Funcionalidades

- ✅ Upload de contratos DOCX
- ✅ Análise automática de campos editáveis
- ✅ Identificação de tipos de campo (texto, CPF, CNPJ, data, moeda, etc.)
- ✅ Formulário dinâmico com validações
- ✅ Preenchimento automático do documento
- ✅ Download em PDF
- ✅ Interface moderna e intuitiva

## 🏗️ Arquitetura

### Backend (FastAPI)
- **Python 3.9+**
- **FastAPI** - Framework web
- **python-docx** - Processamento de DOCX
- **OpenAI API** - Análise inteligente
- **docx2pdf** - Conversão para PDF

### Frontend (Next.js)
- **Next.js 14** - Framework React
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Estilização
- **React Hook Form** - Gerenciamento de formulários

## 🚀 Instalação e Execução

### Backend

```bash
cd backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env e adicionar OPENAI_API_KEY

# Executar servidor
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend

# Instalar dependências
npm install

# Configurar variáveis de ambiente (opcional)
cp .env.example .env.local

# Executar em desenvolvimento
npm run dev
```

Acesse `http://localhost:3000` no navegador.

## 📋 Requisitos

### Backend
- Python 3.9+
- OpenAI API Key
- Para conversão PDF: LibreOffice (Linux/Mac) ou Microsoft Word (Windows)

### Frontend
- Node.js 18+
- npm ou yarn

## 🔧 Configuração

### Variáveis de Ambiente

**Backend (.env):**
```env
OPENAI_API_KEY=your_key_here
PORT=8000
HOST=0.0.0.0
TEMP_DIR=./temp
```

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📖 Uso

1. **Upload**: Faça upload do arquivo DOCX do contrato
2. **Análise**: O sistema identifica automaticamente os campos editáveis
3. **Preenchimento**: Preencha o formulário gerado dinamicamente
4. **Download**: Baixe o documento preenchido em DOCX ou PDF

## 🧠 Inteligência Artificial

O sistema usa GPT-4 (ou GPT-3.5) para:
- Identificar contexto jurídico dos campos
- Gerar labels semânticos e descritivos
- Classificar tipos de dados
- Agrupar campos por seção do contrato
- Reutilizar campos semelhantes automaticamente

## 🔐 Segurança e LGPD

- Arquivos são armazenados temporariamente
- Dados sensíveis não são logados
- Documentos são removidos após processamento
- Código preparado para uso jurídico real

## 📁 Estrutura do Projeto

```
.
├── backend/
│   ├── app/
│   │   ├── main.py              # Aplicação FastAPI
│   │   ├── models/               # Schemas Pydantic
│   │   ├── routers/              # Endpoints da API
│   │   └── services/             # Lógica de negócio
│   ├── temp/                     # Arquivos temporários
│   └── requirements.txt
├── frontend/
│   ├── app/                      # Páginas Next.js
│   ├── components/               # Componentes React
│   ├── lib/                      # Utilitários
│   └── types/                    # Tipos TypeScript
└── README.md
```

## 🧪 MVP - Funcionalidades Implementadas

- ✅ Suporte a DOCX
- ✅ Análise automática de campos
- ✅ Geração de formulário dinâmico
- ✅ Validações de campos
- ✅ Preenchimento de documentos
- ✅ Download em DOCX e PDF
- ✅ Interface responsiva

## 🔮 Expansões Futuras

- [ ] Múltiplos modelos de contrato
- [ ] Templates personalizados
- [ ] Histórico de documentos
- [ ] Assinatura digital
- [ ] Autenticação de usuários
- [ ] Armazenamento em nuvem

## 📝 Licença

Este projeto é um MVP para uso interno.

## ⚠️ Notas Importantes

- O sistema não altera texto jurídico, apenas identifica e preenche campos editáveis
- Campos são identificados automaticamente, sem hardcoding
- A estrutura do contrato não é assumida como fixa
- Código modular e extensível para futuras melhorias
