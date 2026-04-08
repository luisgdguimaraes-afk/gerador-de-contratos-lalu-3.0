#!/usr/bin/env python3
"""
Script para corrigir o arquivo .env removendo BOM e espaços em branco
"""
import re
from pathlib import Path

env_path = Path(__file__).parent / ".env"

if not env_path.exists():
    print("❌ Arquivo .env não encontrado!")
    exit(1)

# Ler arquivo removendo BOM automaticamente
with open(env_path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Limpar linhas e remover espaços em branco
lines = []
for line in content.split('\n'):
    line = line.strip()
    if line and not line.startswith('#'):
        lines.append(line)

# Recriar arquivo sem BOM
new_content = '\n'.join(lines) + '\n'
with open(env_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("OK: Arquivo .env corrigido com sucesso!")
print(f"OK: {len(lines)} variaveis encontradas")

# Verificar se a API key está presente
if 'OPENAI_API_KEY' in new_content:
    match = re.search(r'OPENAI_API_KEY\s*=\s*(.+)', new_content)
    if match:
        key = match.group(1).strip().strip('"\'')
        print(f"OK: OPENAI_API_KEY encontrada: {key[:20]}...")
    else:
        print("AVISO: OPENAI_API_KEY nao encontrada no formato correto")
else:
    print("AVISO: OPENAI_API_KEY nao encontrada no arquivo")
