"""
Aplicação FastAPI para análise e preenchimento de contratos DOCX
"""
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import upload, analyze, fill, download

app = FastAPI(
    title="Gerador de Contratos LALU",
    description="API para geração automática de contratos",
    version="2.0.0"
)

# Registrar rotas
# Upload mantido para compatibilidade futura, mas não é mais usado no fluxo principal
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(analyze.router, prefix="/api", tags=["Schema"])
app.include_router(fill.router, prefix="/api", tags=["Contratos"])
app.include_router(download.router, prefix="/api", tags=["Download"])


@app.get("/")
async def root():
    return {
        "message": "API Gerador de Contratos LALU",
        "version": "2.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# CORS por último = camada externa. Evite BaseHTTPMiddleware antes do CORS: quebra headers CORS no ASGI.
# Regex cobre deploy previews em *.netlify.app. CORS_EXTRA_ORIGINS para domínios próprios.
_extra = os.getenv("CORS_EXTRA_ORIGINS", "")
_extra_origins = [o.strip() for o in _extra.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://documentoslalu.netlify.app",
        *_extra_origins,
    ],
    # Qualquer subdomínio Netlify (incl. deploy previews), sem path
    allow_origin_regex=r"^https://[^/]+\.netlify\.app$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
