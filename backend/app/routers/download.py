"""
Rota para download de documentos preenchidos
"""
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from app.services.document_storage import DocumentStorage

router = APIRouter()
storage = DocumentStorage()


@router.get("/download/{document_id}")
async def download_document(document_id: str):
    """
    Faz download do contrato em PDF.
    Agora sempre retorna PDF (não há mais opção de formato).
    """
    try:
        # Buscar arquivo PDF (sempre PDF agora)
        pdf_path = storage.get_filled_file_path(document_id)
        
        print(f"[DOWNLOAD] document_id recebido: {document_id}", flush=True)
        print(f"[DOWNLOAD] Caminho construído: {pdf_path}", flush=True)
        print(f"[DOWNLOAD] Arquivo existe: {os.path.exists(pdf_path)}", flush=True)
        
        if not Path(pdf_path).exists():
            # Tentar encontrar o arquivo por padrão (caso o nome não seja exatamente o esperado)
            output_dir = storage.output_dir
            if output_dir.exists():
                # Tentar encontrar arquivo que começa com o document_id
                matching_files = list(output_dir.glob(f"{document_id}*.pdf"))
                if matching_files:
                    pdf_path = str(matching_files[0])
                    print(f"[DOWNLOAD] Arquivo encontrado por padrão: {pdf_path}", flush=True)
                else:
                    # Listar todos os arquivos disponíveis para debug
                    available_files = list(output_dir.glob("*.pdf"))
                    print(f"[DOWNLOAD] Arquivos disponíveis no output: {[f.name for f in available_files]}", flush=True)
                    print(f"[DOWNLOAD] Caminho absoluto do output: {output_dir.resolve()}", flush=True)
                    
                    raise HTTPException(
                        status_code=404,
                        detail=f"Documento não encontrado. Procurado: {pdf_path}. Arquivos disponíveis: {[f.name for f in available_files]}"
                    )
            else:
                raise HTTPException(
                    status_code=404,
                    detail=f"Diretório de output não existe: {output_dir}"
                )
        
        # Gerar nome amigável para o arquivo
        filename = f"contrato_{document_id[:8]}.pdf"
        
        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=filename,
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar download: {str(e)}"
        )
