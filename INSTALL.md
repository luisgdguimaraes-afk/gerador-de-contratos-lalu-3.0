# Guia de Instalação Completo

## Pré-requisitos

### Backend
- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)
- OpenAI API Key ([obter aqui](https://platform.openai.com/))

### Frontend
- Node.js 18 ou superior
- npm ou yarn

## Instalação do Backend

1. **Navegar para o diretório backend:**
```bash
cd backend
```

2. **Criar ambiente virtual (recomendado):**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

4. **Configurar variáveis de ambiente:**
```bash
# Criar arquivo .env
# Windows (PowerShell)
New-Item .env

# Linux/Mac
touch .env
```

Edite o arquivo `.env` e adicione:
```env
OPENAI_API_KEY=sua_chave_aqui
PORT=8000
HOST=0.0.0.0
TEMP_DIR=./temp
```

5. **Executar o servidor:**
```bash
# Opção 1: Usando uvicorn diretamente
uvicorn app.main:app --reload --port 8000

# Opção 2: Usando o script run.py
python run.py
```

O servidor estará disponível em `http://localhost:8000`

## Instalação do Frontend

1. **Navegar para o diretório frontend:**
```bash
cd frontend
```

2. **Instalar dependências:**
```bash
npm install
```

3. **Configurar variáveis de ambiente (opcional):**
```bash
# Criar arquivo .env.local
# Windows (PowerShell)
New-Item .env.local

# Linux/Mac
touch .env.local
```

Edite o arquivo `.env.local` e adicione (se o backend estiver em outra porta):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. **Executar em desenvolvimento:**
```bash
npm run dev
```

A aplicação estará disponível em `http://localhost:3000`

## Verificação

1. Acesse `http://localhost:3000` no navegador
2. Faça upload de um arquivo DOCX de contrato
3. O sistema deve:
   - Analisar o documento
   - Identificar campos editáveis
   - Gerar formulário dinâmico
   - Permitir preenchimento e download

## Solução de Problemas

### Backend não inicia
- Verifique se o Python está instalado: `python --version`
- Verifique se todas as dependências foram instaladas: `pip list`
- Verifique se o arquivo `.env` existe e contém `OPENAI_API_KEY`

### Frontend não conecta ao backend
- Verifique se o backend está rodando em `http://localhost:8000`
- Verifique o arquivo `.env.local` no frontend
- Verifique o console do navegador para erros de CORS

### Erro ao converter para PDF
- **Windows**: Instale o Microsoft Word ou use alternativa
- **Linux/Mac**: Instale o LibreOffice:
  ```bash
  # Ubuntu/Debian
  sudo apt-get install libreoffice
  
  # Mac
  brew install --cask libreoffice
  ```

### Erro de memória ao processar documentos grandes
- Limite o tamanho do arquivo no upload
- Aumente o timeout do servidor
- Processe documentos menores primeiro

## Estrutura de Diretórios

```
.
├── backend/
│   ├── app/              # Código da aplicação
│   ├── temp/             # Arquivos temporários (criado automaticamente)
│   ├── .env              # Variáveis de ambiente (criar manualmente)
│   └── requirements.txt  # Dependências Python
├── frontend/
│   ├── app/              # Páginas Next.js
│   ├── components/       # Componentes React
│   ├── .env.local        # Variáveis de ambiente (opcional)
│   └── package.json      # Dependências Node.js
└── README.md             # Documentação principal
```

## Próximos Passos

Após a instalação, consulte o `README.md` principal para:
- Detalhes sobre a arquitetura
- Como usar a aplicação
- Expansões futuras planejadas
