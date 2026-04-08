# 🔍 DIAGNÓSTICO TÉCNICO COMPLETO - Sistema de Análise de Contratos

## 1. VISÃO GERAL DO PROJETO

### Objetivo Principal
Sistema web completo para análise inteligente e preenchimento automático de contratos em formato DOCX usando Inteligência Artificial. O sistema identifica automaticamente campos editáveis em contratos, gera labels semânticos e descritivos, cria um formulário dinâmico e permite o download do documento preenchido.

### Fluxo Completo da Aplicação

1. **Upload do Documento** (`/api/upload`)
   - Usuário faz upload de um arquivo DOCX através da interface web
   - Backend recebe o arquivo e armazena temporariamente em `backend/temp/`
   - Retorna um `document_id` único (UUID) para referenciar o documento

2. **Análise do Documento** (`/api/analyze`)
   - **Extração de Texto**: Usa `python-docx` para extrair todo o texto do documento
   - **Identificação de Placeholders**: Usa regex para encontrar padrões como:
     - `xxxx`, `xxxxxx` (múltiplos 'x')
     - `____`, `______` (múltiplos underscores)
     - `...`, `......` (múltiplos pontos)
     - `[texto]`, `{texto}`, `(texto)` (colchetes, chaves, parênteses)
   - **Análise com IA**: Envia o texto e placeholders encontrados para a API da OpenAI (GPT-4o-mini)
   - **Geração de Metadados**: IA retorna:
     - `field_id`: ID semântico único (ex: "buyer_name", "property_address")
     - `label`: Label descritivo em português (ex: "Nome completo do comprador")
     - `type`: Tipo de dado (text, number, currency, date, cpf, cnpj, phone, email)
     - `section`: Seção do contrato (COMPRADOR, VENDEDOR, IMÓVEL, etc.)
     - `required`: Se o campo é obrigatório
     - `original_text`: Texto placeholder original encontrado
     - `context`: Contexto ao redor do campo
   - Retorna `AnalysisResponse` com lista de campos identificados

3. **Preenchimento do Formulário** (Frontend)
   - Interface gera formulário dinâmico baseado nos campos identificados
   - Campos são agrupados por seção
   - Validações client-side conforme tipo de campo
   - Usuário preenche os dados

4. **Preenchimento do Documento** (`/api/fill`)
   - Backend recebe os dados do formulário (`field_id` -> `value`)
   - Re-analisa o documento para obter mapeamento `field_id` -> `original_text`
   - Substitui os placeholders no documento DOCX usando `python-docx`
   - Formata valores conforme tipo (CPF, CNPJ, moeda, etc.)
   - Salva documento preenchido como `{document_id}_filled.docx`

5. **Download do Documento** (`/api/download/{document_id}`)
   - Usuário pode baixar em dois formatos:
     - **DOCX**: Documento Word preenchido
     - **PDF**: Conversão do DOCX para PDF usando `docx2pdf` (requer LibreOffice ou Microsoft Word)

---

## 2. STACK TECNOLÓGICA

### Frontend
- **Framework**: Next.js 14.0.3 (React 18.2.0)
- **Linguagem**: TypeScript 5.3.3
- **Estilização**: Tailwind CSS 3.3.6
- **Gerenciamento de Formulários**: React Hook Form 7.48.2
- **Validação**: Zod 3.22.4
- **HTTP Client**: Axios 1.6.2
- **Máscaras de Input**: react-input-mask 2.0.4
- **Datas**: date-fns 2.30.0

### Backend
- **Linguagem**: Python 3.14.2 (compatível com 3.9+)
- **Framework Web**: FastAPI 0.104.1
- **Servidor ASGI**: Uvicorn 0.24.0 (com extensões standard)
- **Validação de Dados**: Pydantic 2.12.5
- **Upload de Arquivos**: python-multipart 0.0.6
- **Variáveis de Ambiente**: python-dotenv 1.0.0

### Bibliotecas para Manipulação de Documentos
- **DOCX**: python-docx 1.1.0
  - Extração de texto
  - Manipulação de parágrafos e tabelas
  - Preservação de formatação
- **PDF**: docx2pdf 0.1.8
  - Conversão DOCX → PDF
  - Requer LibreOffice (Linux/Mac) ou Microsoft Word (Windows)
- **PDF (alternativa)**: pypdf2 3.0.1 (instalado mas não usado atualmente)

### API de IA
- **Provedor**: OpenAI
- **Biblioteca**: openai 2.15.0 (atualizado de 1.3.5)
- **Modelo Padrão**: gpt-4o-mini (configurável via `OPENAI_MODEL`)
- **Modelos Alternativos**: gpt-4o, gpt-3.5-turbo
- **Uso**: Análise de contexto jurídico, geração de labels semânticos, classificação de tipos de dados

### Banco de Dados
- **Não utiliza banco de dados**
- Armazenamento temporário em sistema de arquivos (`backend/temp/`)
- Arquivos são identificados por UUID

### Outras Dependências
- **Async I/O**: aiofiles 23.2.1 (para upload assíncrono de arquivos)
- **HTTP Client**: httpx 0.28.1 (usado internamente pela OpenAI)

---

## 3. ESTRUTURA DE ARQUIVOS

```
Contratos LALU/
├── backend/
│   ├── app/
│   │   ├── main.py                    # Aplicação FastAPI principal, configuração CORS, rotas
│   │   ├── models/
│   │   │   └── schemas.py              # Schemas Pydantic (FieldInfo, UploadResponse, AnalysisResponse, etc.)
│   │   ├── routers/
│   │   │   ├── upload.py               # Endpoint POST /api/upload - Recebe arquivo DOCX
│   │   │   ├── analyze.py              # Endpoint POST /api/analyze - Analisa documento e extrai campos
│   │   │   ├── fill.py                 # Endpoint POST /api/fill - Preenche documento com dados
│   │   │   └── download.py             # Endpoint GET /api/download/{id} - Download DOCX ou PDF
│   │   └── services/
│   │       ├── document_storage.py     # Gerenciamento de arquivos temporários
│   │       ├── document_parser.py     # Extração de texto e identificação de placeholders (regex)
│   │       ├── document_analyzer.py   # Orquestra parser + IA para análise completa
│   │       ├── ai_analyzer.py          # Integração com OpenAI API, análise inteligente
│   │       ├── document_filler.py     # Preenchimento de campos no documento DOCX
│   │       ├── field_validator.py     # Validação de campos (CPF, CNPJ, email, etc.)
│   │       └── pdf_generator.py       # Conversão DOCX para PDF
│   ├── temp/                           # Diretório de arquivos temporários (criado automaticamente)
│   ├── .env                            # Variáveis de ambiente (OPENAI_API_KEY, PORT, etc.)
│   ├── requirements.txt                # Dependências Python
│   └── run.py                          # Script para executar servidor
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx                    # Página principal, orquestra os 3 passos (upload, form, download)
│   │   ├── layout.tsx                  # Layout base da aplicação
│   │   └── globals.css                 # Estilos globais Tailwind
│   ├── components/
│   │   ├── UploadStep.tsx              # Componente de upload de arquivo
│   │   ├── FormStep.tsx                # Componente de formulário dinâmico
│   │   ├── DynamicField.tsx             # Campo de formulário dinâmico com validações
│   │   └── DownloadStep.tsx            # Componente de download (DOCX/PDF)
│   ├── lib/
│   │   └── api.ts                      # Cliente HTTP (Axios) para comunicação com backend
│   ├── types/
│   │   └── index.ts                    # Tipos TypeScript (FieldInfo, AnalysisResponse, etc.)
│   ├── package.json                    # Dependências Node.js
│   └── tsconfig.json                   # Configuração TypeScript
│
└── README.md                            # Documentação principal
```

### Responsabilidades por Funcionalidade

| Funcionalidade | Arquivo Backend | Arquivo Frontend |
|---------------|----------------|-----------------|
| **Upload do documento** | `routers/upload.py` + `services/document_storage.py` | `components/UploadStep.tsx` |
| **Extração/análise dos campos** | `routers/analyze.py` + `services/document_analyzer.py` + `services/document_parser.py` + `services/ai_analyzer.py` | `components/UploadStep.tsx` (chama API) |
| **Interface do formulário** | - | `components/FormStep.tsx` + `components/DynamicField.tsx` |
| **Geração do documento final** | `routers/fill.py` + `services/document_filler.py` | `components/FormStep.tsx` (chama API) |
| **Download** | `routers/download.py` + `services/pdf_generator.py` | `components/DownloadStep.tsx` |

---

## 4. LÓGICA DE EXTRAÇÃO DE CAMPOS

### Método Híbrido: Regex + IA

#### Etapa 1: Identificação de Placeholders (Regex)
**Arquivo**: `backend/app/services/document_parser.py`

O sistema usa **regex** para identificar padrões comuns de campos editáveis:

```python
PLACEHOLDER_PATTERNS = [
    r'x{3,}',      # xxxx, xxxxxx (múltiplos 'x')
    r'_+',         # ____, ______ (múltiplos underscores)
    r'\.{3,}',     # ..., ...... (múltiplos pontos)
    r'\[.*?\]',    # [texto] (colchetes)
    r'\{.*?\}',    # {texto} (chaves)
    r'\(.*?\)',    # (texto) (parênteses - pode ser placeholder)
]
```

**Processo**:
1. Extrai todo o texto do DOCX usando `python-docx`
2. Aplica cada padrão regex no texto
3. Remove sobreposições (mantém o maior placeholder)
4. Filtra placeholders muito pequenos (< 3 caracteres)
5. Extrai contexto ao redor de cada placeholder (±100 caracteres)

**Limitações**:
- Não identifica campos que não seguem esses padrões
- Pode identificar falsos positivos (texto que parece placeholder mas não é)
- Não preserva formatação original (apenas texto)

#### Etapa 2: Análise Inteligente com IA
**Arquivo**: `backend/app/services/ai_analyzer.py`

Após identificar placeholders, o sistema envia para a **OpenAI API**:

**Prompt enviado**:
```
Analise o seguinte contrato e identifique os campos editáveis:

TEXTO DO CONTRATO:
[texto completo do documento, limitado a 12000 caracteres]

CAMPOS IDENTIFICADOS:
[lista de placeholders com contexto]

Para cada campo, forneça:
1. field_id: ID único e semântico (ex: "buyer_name", "property_address")
2. label: Label descritivo em português
3. type: Tipo de dado (text, number, currency, date, cpf, cnpj, phone, email)
4. required: Se é obrigatório
5. original_text: O texto placeholder original
6. context: Contexto ao redor do campo
7. section: Seção do contrato (COMPRADOR, VENDEDOR, IMÓVEL, etc.)

IMPORTANTE: Campos semelhantes devem ter o mesmo field_id.
```

**Resposta da IA**:
- JSON estruturado com lista de campos
- Cada campo contém todos os metadados necessários
- Campos semelhantes recebem o mesmo `field_id` (reutilização)

**Fallback**:
Se a IA falhar, o sistema cria campos básicos:
- `field_id`: "field_1", "field_2", etc.
- `label`: "Campo 1", "Campo 2", etc.
- `type`: TEXT (padrão)

### Mapeamento para o Formulário

**Arquivo**: `frontend/components/FormStep.tsx`

1. Campos são agrupados por `section` (COMPRADOR, VENDEDOR, etc.)
2. Cada campo é renderizado como `DynamicField` com:
   - Input apropriado ao tipo (text, number, date, etc.)
   - Máscara conforme tipo (CPF, CNPJ, telefone)
   - Validação client-side
   - Label descritivo gerado pela IA

---

## 5. LÓGICA DE GERAÇÃO DO CONTRATO

### Processo de Preenchimento
**Arquivo**: `backend/app/services/document_filler.py`

#### Etapa 1: Mapeamento
- Re-analisa o documento para obter `field_id` -> `original_text`
- Cria mapeamento: `original_text` -> `valor_formatado`

#### Etapa 2: Substituição
**Método**: Substituição de texto usando regex

1. **Substituição Exata** (prioritária):
   - Usa `field_mapping` para substituir exatamente o `original_text` pelo valor formatado
   - Escapa caracteres especiais do regex
   - Ordena por tamanho (maior primeiro) para evitar substituições parciais

2. **Substituição Genérica** (fallback):
   - Se ainda houver placeholders não substituídos, tenta padrões genéricos
   - Substitui `xxxx`, `____`, `...` por valores restantes

3. **Locais de Substituição**:
   - Parágrafos (`doc.paragraphs`)
   - Células de tabelas (`doc.tables` -> `rows` -> `cells` -> `paragraphs`)

#### Etapa 3: Formatação de Valores
**Método**: `_format_field_value()`

- **CPF**: `12345678901` → `123.456.789-01`
- **CNPJ**: `12345678000190` → `12.345.678/0001-90`
- **Moeda**: `100000` → `R$ 1.000,00`
- **Outros**: Mantém como string

#### Etapa 4: Preservação de Formatação
- **Preservada**: Formatação de parágrafos, tabelas, estrutura do documento
- **Não preservada**: Formatação dentro dos placeholders (negrito, itálico, etc.)
- **Limitação**: Substituição é feita no texto, não nos runs individuais do DOCX

### Formatos de Saída

1. **DOCX** (`/api/download/{id}?format=docx`)
   - Documento Word preenchido
   - Preserva estrutura e formatação básica
   - Gerado diretamente pelo `python-docx`

2. **PDF** (`/api/download/{id}?format=pdf`)
   - Conversão do DOCX para PDF
   - Usa `docx2pdf` que requer:
     - **Windows**: Microsoft Word instalado
     - **Linux/Mac**: LibreOffice instalado
   - Pode falhar se essas dependências não estiverem disponíveis

---

## 6. PROBLEMAS ATUAIS

### Erro Principal: Inicialização do Cliente OpenAI

**Erro**: `Client.__init__() got an unexpected keyword argument 'proxies'`

**Localização**: `backend/app/services/ai_analyzer.py`, linha 62

**Causa**:
- Versão antiga da biblioteca OpenAI (1.3.5) tinha incompatibilidades
- Atualizado para 2.15.0, mas servidor pode não ter sido reiniciado
- Possível conflito com configurações de proxy ou variáveis de ambiente

**Status**: 
- ✅ Biblioteca atualizada para 2.15.0
- ✅ Código ajustado para compatibilidade
- ⚠️ Pode precisar reiniciar servidor backend
- ⚠️ Pode haver cache de módulos Python

**Solução Aplicada**:
1. Atualizado `requirements.txt`: `openai>=1.40.0`
2. Simplificada inicialização do cliente: apenas `OpenAI(api_key=api_key)`
3. Removida configuração de timeout com httpx que poderia causar conflitos
4. Adicionado tratamento de erros mais robusto

### Outros Problemas Potenciais

1. **Conversão para PDF**
   - Requer LibreOffice (Linux/Mac) ou Microsoft Word (Windows)
   - Pode falhar silenciosamente se não estiver instalado
   - **Arquivo**: `backend/app/services/pdf_generator.py`

2. **Timeout de Análise**
   - Análise com IA pode demorar muito em documentos grandes
   - Timeout configurado para 5 minutos (300s) no frontend
   - Pode não ser suficiente para documentos muito grandes

3. **Limite de Tamanho do Documento**
   - Texto truncado para 12000 caracteres antes de enviar para IA
   - Pode perder informações em documentos muito grandes
   - **Arquivo**: `backend/app/services/ai_analyzer.py`, linha 166

4. **Armazenamento Temporário**
   - Arquivos não são limpos automaticamente
   - Pode acumular arquivos no diretório `temp/`
   - **Arquivo**: `backend/app/services/document_storage.py`

5. **Validação de Campos**
   - Validação ocorre apenas no backend após preenchimento
   - Validação client-side pode não cobrir todos os casos
   - **Arquivo**: `backend/app/services/field_validator.py`

### Logs de Erro Relevantes

**Backend** (console):
```
Erro ao analisar documento: Erro ao inicializar cliente OpenAI: Client.__init__() got an unexpected keyword argument 'proxies'
```

**Frontend** (console do navegador):
```
Erro ao processar documento: Erro ao analisar documento: Erro ao inicializar cliente OpenAI: Client.__init__() got an unexpected keyword argument 'proxies'
```

---

## 7. CÓDIGO RELEVANTE

### Função de Extração de Campos

**Arquivo**: `backend/app/services/document_analyzer.py`

```python
async def analyze_document(self, docx_path: str) -> AnalysisResponse:
    """
    Analisa documento completo e retorna campos identificados
    """
    # 1. Extrair texto
    document_text = self.parser.extract_text(docx_path)
    
    # 2. Encontrar placeholders (regex)
    placeholder_matches = self.parser.find_placeholders(document_text)
    
    # 3. Preparar dados dos placeholders com contexto
    placeholders = []
    for placeholder_text, start, end in placeholder_matches:
        context = self.parser.get_context_around_placeholder(
            document_text, start, end
        )
        placeholders.append({
            "text": placeholder_text,
            "start": start,
            "end": end,
            "context": context
        })
    
    # 4. Usar IA para análise inteligente
    fields = await self.ai_analyzer.analyze_fields(document_text, placeholders)
    
    # 5. Extrair seções únicas
    sections = list(set([f.section for f in fields if f.section]))
    
    return AnalysisResponse(
        document_id=document_id,
        fields=fields,
        sections=sections,
        total_fields=len(fields)
    )
```

### Função de Análise com IA

**Arquivo**: `backend/app/services/ai_analyzer.py`

```python
async def analyze_fields(self, document_text: str, 
                        placeholders: List[Dict]) -> List[FieldInfo]:
    """
    Analisa placeholders e gera informações estruturadas sobre cada campo
    """
    # Preparar contexto para a IA
    context_prompt = self._build_analysis_prompt(document_text, placeholders)
    
    # Enviar para OpenAI
    response = self.client.chat.completions.create(
        model=self.model,
        messages=[
            {
                "role": "system",
                "content": """Você é um especialista em análise de contratos jurídicos..."""
            },
            {
                "role": "user",
                "content": context_prompt
            }
        ],
        temperature=0.3,
        response_format={"type": "json_object"}
    )
    
    # Parsear resposta JSON
    result = json.loads(response.choices[0].message.content)
    fields = result.get("fields", [])
    
    # Converter para FieldInfo
    field_infos = []
    for field_data in fields:
        field_info = FieldInfo(
            field_id=field_data.get("field_id"),
            label=field_data.get("label"),
            type=FieldType(field_data.get("type", "text")),
            required=field_data.get("required", True),
            original_text=field_data.get("original_text"),
            context=field_data.get("context", ""),
            placeholder=field_data.get("placeholder"),
            section=field_data.get("section")
        )
        field_infos.append(field_info)
    
    return field_infos
```

### Função de Geração do Documento

**Arquivo**: `backend/app/services/document_filler.py`

```python
async def fill_document(self, original_document_id: str, 
                       original_path: str, 
                       fields: Dict[str, Any],
                       field_mapping: Optional[Dict[str, str]] = None) -> str:
    """
    Preenche o documento com os dados fornecidos
    """
    # Carregar documento original
    doc = Document(original_path)
    
    # Validar campos
    self.validator.validate_fields(fields)
    
    # Preencher campos no documento
    self._replace_fields_in_document(doc, fields, field_mapping)
    
    # Salvar documento preenchido
    filled_document_id = f"{original_document_id}_filled"
    filled_path = self.storage.get_filled_file_path(filled_document_id)
    doc.save(filled_path)
    
    return filled_document_id

def _replace_fields_in_document(self, doc: Document, 
                                fields: Dict[str, Any],
                                field_mapping: Optional[Dict[str, str]] = None):
    """
    Substitui placeholders no documento pelos valores fornecidos
    """
    # Mapear valores formatados
    formatted_values = {}
    for field_id, value in fields.items():
        formatted_values[field_id] = self._format_field_value(field_id, value)
    
    # Criar mapeamento original_text -> valor formatado
    text_to_value = {}
    if field_mapping:
        for field_id, original_text in field_mapping.items():
            if field_id in formatted_values:
                escaped_text = re.escape(original_text)
                text_to_value[escaped_text] = formatted_values[field_id]
    
    # Substituir em parágrafos
    for para in doc.paragraphs:
        para.text = self._replace_in_text(
            para.text, fields, formatted_values, text_to_value, field_mapping
        )
    
    # Substituir em tabelas
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    para.text = self._replace_in_text(
                        para.text, fields, formatted_values, text_to_value, field_mapping
                    )
```

### Schema/Tipos dos Campos

**Backend** (`backend/app/models/schemas.py`):

```python
class FieldType(str, Enum):
    TEXT = "text"
    NUMBER = "number"
    CURRENCY = "currency"
    DATE = "date"
    CPF = "cpf"
    CNPJ = "cnpj"
    PHONE = "phone"
    EMAIL = "email"

class FieldInfo(BaseModel):
    field_id: str
    label: str
    type: FieldType
    required: bool = True
    original_text: str
    context: str
    placeholder: Optional[str] = None
    section: Optional[str] = None
```

**Frontend** (`frontend/types/index.ts`):

```typescript
export type FieldType = 
  | 'text'
  | 'number'
  | 'currency'
  | 'date'
  | 'cpf'
  | 'cnpj'
  | 'phone'
  | 'email'

export interface FieldInfo {
  field_id: string
  label: string
  type: FieldType
  required: boolean
  original_text: string
  context: string
  placeholder?: string
  section?: string
}
```

---

## 8. CONFIGURAÇÃO E VARIÁVEIS DE AMBIENTE

### Backend (`.env`)

```env
OPENAI_API_KEY=sk-proj-... (chave configurada)
PORT=8000
HOST=0.0.0.0
TEMP_DIR=./temp
OPENAI_MODEL=gpt-4o-mini  # Opcional, padrão: gpt-4o-mini
```

### Frontend (`.env.local` - opcional)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 9. ENDPOINTS DA API

### POST `/api/upload`
- **Request**: `multipart/form-data` com arquivo DOCX
- **Response**: `UploadResponse` com `document_id`, `filename`, `message`

### POST `/api/analyze`
- **Request**: `{"document_id": "uuid"}`
- **Response**: `AnalysisResponse` com `fields[]`, `sections[]`, `total_fields`

### POST `/api/fill`
- **Request**: `{"document_id": "uuid", "fields": {"field_id": "value"}}`
- **Response**: `{"filled_document_id": "uuid_filled", "message": "..."}`

### GET `/api/download/{document_id}?format=docx|pdf`
- **Response**: Arquivo binário (DOCX ou PDF)

---

## 10. PRÓXIMOS PASSOS PARA RESOLUÇÃO

1. **Reiniciar servidor backend** para aplicar mudanças na biblioteca OpenAI
2. **Verificar logs do backend** durante upload para identificar erro exato
3. **Testar inicialização do cliente OpenAI** isoladamente
4. **Verificar variáveis de ambiente** que possam estar causando conflito
5. **Limpar cache Python** (`__pycache__`) se necessário

---

**Data do Diagnóstico**: 2025-01-27
**Versão da Biblioteca OpenAI**: 2.15.0
**Versão Python**: 3.14.2
**Versão Node.js**: 24.13.0
