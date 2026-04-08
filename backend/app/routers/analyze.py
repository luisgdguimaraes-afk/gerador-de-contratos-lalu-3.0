"""
Rota para análise de documentos e extração de campos
"""
import os
import traceback
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.document_parser import DocumentParser
from app.services.document_storage import DocumentStorage
from app.services.template_service import TemplateService
from app.services.contract_schema import ROTA_DO_SOL_SCHEMA, SECTION_ORDER, get_all_field_ids
from app.models.schemas import AnalysisResponse, FieldInfo, FieldType, SectionInfo

router = APIRouter()
parser = DocumentParser()
storage = DocumentStorage()


@router.get("/schema")
async def get_contract_schema(template_id: Optional[str] = "rota_do_sol"):
    """
    Retorna o schema do formulário para o template especificado.
    Não precisa mais de upload - usa template hospedado.
    """
    try:
        # Verificar se o template existe
        template_path = TemplateService.get_template_path(template_id)
        
        # Montar resposta com schema do formulário
        fields = []
        for section_id, section_name in SECTION_ORDER:
            section_fields = [
                FieldInfo(
                    field_id=f.field_id,
                    label=f.label,
                    type=FieldType(f.type.value),
                    required=f.required,
                    original_text=f'{{{{{f.field_id}}}}}',  # Placeholder formatado
                    context="",  # Não precisa mais de contexto
                    placeholder=f.placeholder if f.placeholder else None,  # Garantir que None seja None, não string vazia
                    section=section_name,
                    section_id=section_id,
                    options=f.options,
                    mask=f.mask
                )
                for f in ROTA_DO_SOL_SCHEMA.values()
                if f.section == section_id
            ]
            fields.extend(section_fields)
        
        sections_list = [SectionInfo(id=section_id, name=section_name) for section_id, section_name in SECTION_ORDER]
        
        return {
            "template_id": template_id,
            "template_name": TemplateService.AVAILABLE_TEMPLATES[template_id]["name"],
            "fields": fields,
            "sections": sections_list,
            "total_fields": len(fields)
        }
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/templates")
async def list_templates():
    """Lista todos os templates disponíveis"""
    return {
        "templates": TemplateService.list_templates(),
        "default": TemplateService.get_default_template_id()
    }


class AnalyzeRequest(BaseModel):
    document_id: str


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_document(request: AnalyzeRequest):
    """
    Analisa documento e retorna os campos para preenchimento.
    
    Com placeholders padronizados, não precisa mais de IA para inferir campos.
    Apenas valida se o documento contém os placeholders esperados.
    """
    try:
        # Verificar se o documento existe
        file_path = storage.get_file_path(request.document_id)
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404,
                detail="Documento não encontrado"
            )
        
        print(f"Iniciando análise do documento: {request.document_id}")
        
        # Extrair texto e placeholders
        text = parser.extract_text(file_path)
        placeholders = parser.find_placeholders(text)
        
        print(f"Placeholders encontrados: {len(placeholders)}")
        
        # Validar placeholders
        validation = parser.validate_placeholders(placeholders, get_all_field_ids())
        
        if not validation["valid"]:
            print(f"AVISO: Placeholders faltando: {validation['missing']}")
            print(f"AVISO: Placeholders extras: {validation['extra']}")
        
        # Montar resposta com schema do formulário
        fields = []
        for section_id, section_name in SECTION_ORDER:
            section_fields = [
                FieldInfo(
                    field_id=f.field_id,
                    label=f.label,
                    type=FieldType(f.type.value),
                    required=f.required,
                    original_text=f'{{{{{f.field_id}}}}}',  # Placeholder formatado
                    context="",  # Não precisa mais de contexto
                    placeholder=f.placeholder,
                    section=section_name,
                    section_id=section_id
                )
                for f in ROTA_DO_SOL_SCHEMA.values()
                if f.section == section_id
            ]
            fields.extend(section_fields)
        
        sections_list = [SectionInfo(id=section_id, name=section_name) for section_id, section_name in SECTION_ORDER]
        
        print(f"Análise completa: {len(fields)} campos identificados")
        
        return AnalysisResponse(
            document_id=request.document_id,
            fields=fields,
            sections=sections_list,
            total_fields=len(fields)
        )
    except HTTPException:
        raise
    except Exception as e:
        # Log detalhado do erro
        error_trace = traceback.format_exc()
        print(f"Erro ao analisar documento: {str(e)}")
        print(f"Traceback: {error_trace}")
        
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao analisar documento: {str(e)}"
        )
