"""
Aplicação FastAPI para análise e preenchimento de contratos DOCX
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import traceback
from app.routers import upload, analyze, fill, download

app = FastAPI(
    title="Gerador de Contratos LALU",
    description="API para geração automática de contratos",
    version="2.0.0"
)

# Configurar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://documentoslalu.netlify.app",
        "https://*.netlify.app"  # Permite deploy previews
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


# Middleware para log de requisições
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {request.method} {request.url.path} - {response.status_code} - {process_time:.2f}s")
        return response
    except Exception as e:
        process_time = time.time() - start_time
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ERRO em {request.method} {request.url.path} - {process_time:.2f}s")
        print(f"Erro: {str(e)}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"detail": f"Erro interno: {str(e)}"}
        )
