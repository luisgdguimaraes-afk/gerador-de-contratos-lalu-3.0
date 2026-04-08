# Backend - Sistema de Análise de Contratos

API FastAPI para análise inteligente e preenchimento de contratos DOCX.

## 🚀 Instalação

1. Instalar dependências:
```bash
pip install -r requirements.txt
```

2. Configurar variáveis de ambiente:
```bash
cp .env.example .env
# Editar .env e adicionar sua OPENAI_API_KEY
```

3. Executar servidor:
```bash
uvicorn app.main:app --reload --port 8000
```

## 📋 Endpoints

### POST `/api/upload`
Upload de arquivo DOCX
- **Body**: `multipart/form-data` com arquivo
- **Response**: `{ document_id, filename, message }`

### POST `/api/analyze`
Analisa documento e identifica campos
- **Body**: `{ document_id: string }`
- **Response**: `{ document_id, fields[], sections[], total_fields }`

### POST `/api/fill`
Preenche documento com dados do formulário
- **Body**: `{ document_id: string, fields: { field_id: value } }`
- **Response**: `{ filled_document_id, message }`

### GET `/api/download/{document_id}?format=docx|pdf`
Download do documento preenchido
- **Query params**: `format` (docx ou pdf)
- **Response**: Arquivo para download

## 🔧 Estrutura

```
backend/
├── app/
│   ├── main.py              # Aplicação FastAPI
│   ├── models/
│   │   └── schemas.py       # Schemas Pydantic
│   ├── routers/             # Endpoints da API
│   │   ├── upload.py
│   │   ├── analyze.py
│   │   ├── fill.py
│   │   └── download.py
│   └── services/            # Lógica de negócio
│       ├── document_storage.py
│       ├── document_parser.py
│       ├── document_analyzer.py
│       ├── ai_analyzer.py
│       ├── document_filler.py
│       ├── field_validator.py
│       └── pdf_generator.py
├── temp/                    # Arquivos temporários
└── requirements.txt
```

## ⚠️ Requisitos

- Python 3.9+
- OpenAI API Key
- Para conversão PDF: LibreOffice ou Microsoft Word (Windows)
