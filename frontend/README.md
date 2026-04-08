# Frontend - Sistema de Análise de Contratos

Interface Next.js para análise e preenchimento de contratos DOCX.

## 🚀 Instalação

1. Instalar dependências:
```bash
npm install
```

2. Configurar variáveis de ambiente:
```bash
cp .env.example .env.local
# Editar .env.local se necessário
```

3. Executar em desenvolvimento:
```bash
npm run dev
```

A aplicação estará disponível em `http://localhost:3000`

## 📋 Funcionalidades

- **Upload de Documentos**: Interface drag-and-drop para upload de arquivos DOCX
- **Formulário Dinâmico**: Geração automática de formulário baseado nos campos identificados
- **Validações**: Validação de CPF, CNPJ, e-mail, telefone, datas e valores monetários
- **Download**: Download do documento preenchido em DOCX ou PDF

## 🎨 Tecnologias

- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- React Hook Form
- Axios

## 📁 Estrutura

```
frontend/
├── app/
│   ├── page.tsx          # Página principal
│   ├── layout.tsx        # Layout raiz
│   └── globals.css       # Estilos globais
├── components/
│   ├── UploadStep.tsx   # Componente de upload
│   ├── FormStep.tsx     # Componente de formulário
│   ├── DownloadStep.tsx # Componente de download
│   └── DynamicField.tsx # Campo dinâmico com validações
├── lib/
│   └── api.ts           # Cliente API
└── types/
    └── index.ts         # Tipos TypeScript
```
