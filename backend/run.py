#!/usr/bin/env python3
"""
Script para executar o servidor FastAPI
"""
import uvicorn
import os
import sys
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar stdout para garantir que os prints apareçam (pode falhar em alguns terminais)
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    print("=" * 60, flush=True)
    print("  Backend LALU - Gerador de Contratos", flush=True)
    print("  Porta:", port, "| Nao execute outro 'python run.py' ao mesmo tempo.", flush=True)
    print("=" * 60, flush=True)

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
