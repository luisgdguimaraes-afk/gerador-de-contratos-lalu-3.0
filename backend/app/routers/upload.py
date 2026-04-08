"""
Rota para upload de documentos DOCX
"""
import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.document_storage import DocumentStorage
from app.models.schemas import UploadResponse

router = APIRouter()
storage = DocumentStorage()


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Recebe um arquivo DOCX e armazena temporariamente
    Retorna um ID único para referenciar o documento
    """
    # Validar tipo de arquivo
    if not file.filename.endswith('.docx'):
        raise HTTPException(
            status_code=400,
            detail="Apenas arquivos DOCX são suportados"
        )
    
    try:
        # Gerar ID único para o documento
        document_id = str(uuid.uuid4())
        
        print(f"Recebendo upload: {file.filename} (ID: {document_id})")
        
        # Salvar arquivo temporariamente
        file_path = await storage.save_uploaded_file(document_id, file)
        
        print(f"Arquivo salvo em: {file_path}")
        
        return UploadResponse(
            document_id=document_id,
            filename=file.filename,
            message="Documento enviado com sucesso"
        )
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Erro ao processar upload: {str(e)}")
        print(f"Traceback: {error_trace}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar upload: {str(e)}"
        )
