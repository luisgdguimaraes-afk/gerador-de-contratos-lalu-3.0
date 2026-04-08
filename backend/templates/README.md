# Templates de Contratos

Este diretório contém os templates padrão de contratos com placeholders padronizados.

## Arquivos

- **CONTRATO_ROTA_DO_SOL_TEMPLATE.pdf**: Template do contrato "RESIDENCIAL ROTA DO SOL" em formato PDF (referência visual)
- **CONTRATO_ROTA_DO_SOL_TEMPLATE.docx**: Template do contrato "RESIDENCIAL ROTA DO SOL" em formato DOCX (para edição e uso no sistema)

## Formato dos Placeholders

Todos os campos editáveis no contrato devem usar o formato padronizado:

```
{{CAMPO_ID}}
```

Exemplos:
- `{{COMPRADOR_PF_NOME}}`
- `{{COMPRADOR_PF_CPF}}`
- `{{PRECO_TOTAL_VALOR}}`
- `{{UNIDADE_LOTE_NUMERO}}`

## Uso

O sistema detecta automaticamente os placeholders `{{CAMPO}}` no documento DOCX e gera um formulário dinâmico baseado no schema definido em `backend/app/services/contract_schema.py`.

## Manutenção

- Para adicionar novos campos: atualize `contract_schema.py` e adicione os placeholders correspondentes no template DOCX
- Para modificar o template: edite o arquivo `.docx` mantendo o formato `{{CAMPO}}`
- Após modificar o DOCX, gere um novo PDF para referência
