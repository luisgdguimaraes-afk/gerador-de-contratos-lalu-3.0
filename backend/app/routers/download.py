"""
Rota para download de documentos preenchidos
"""
import os
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from pathlib import Path
from app.services.document_storage import DocumentStorage

router = APIRouter()
storage = DocumentStorage()


@router.get("/download/{document_id}")
async def download_document(document_id: str, format: str = Query("pdf", pattern="^(pdf|docx)$")):
    """
    Faz download do contrato em PDF ou DOCX.
    """
    try:
        ext = "docx" if format == "docx" else "pdf"
        media_type = (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            if ext == "docx"
            else "application/pdf"
        )
        file_path = str(storage.output_dir / f"{document_id}.{ext}")
        
        print(f"[DOWNLOAD] document_id recebido: {document_id}", flush=True)
        print(f"[DOWNLOAD] format recebido: {format}", flush=True)
        print(f"[DOWNLOAD] Caminho construído: {file_path}", flush=True)
        print(f"[DOWNLOAD] Arquivo existe: {os.path.exists(file_path)}", flush=True)
        
        if not Path(file_path).exists():
            # Tentar encontrar o arquivo por padrão (caso o nome não seja exatamente o esperado)
            output_dir = storage.output_dir
            if output_dir.exists():
                # Tentar encontrar arquivo que começa com o document_id
                matching_files = list(output_dir.glob(f"{document_id}*.{ext}"))
                if matching_files:
                    file_path = str(matching_files[0])
                    print(f"[DOWNLOAD] Arquivo encontrado por padrão: {file_path}", flush=True)
                else:
                    # Listar todos os arquivos disponíveis para debug
                    available_files = list(output_dir.glob(f"*.{ext}"))
                    print(f"[DOWNLOAD] Arquivos disponíveis no output: {[f.name for f in available_files]}", flush=True)
                    print(f"[DOWNLOAD] Caminho absoluto do output: {output_dir.resolve()}", flush=True)
                    
                    raise HTTPException(
                        status_code=404,
                        detail=f"Documento não encontrado no formato {ext}. Procurado: {file_path}. Arquivos disponíveis: {[f.name for f in available_files]}"
                    )
            else:
                raise HTTPException(
                    status_code=404,
                    detail=f"Diretório de output não existe: {output_dir}"
                )
        
        # Gerar nome amigável para o arquivo
        filename = f"contrato_{document_id[:8]}.{ext}"
        
        return FileResponse(
            path=file_path,
            media_type=media_type,
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
