"""
Schemas Pydantic para validação de dados
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class FieldType(str, Enum):
    """Tipos de campos suportados"""
    TEXT = "text"
    NUMBER = "number"
    CURRENCY = "currency"
    DATE = "date"
    CPF = "cpf"
    CNPJ = "cnpj"
    CEP = "cep"
    PHONE = "phone"
    EMAIL = "email"
    SELECT = "select"
    TEXTAREA = "textarea"


class FieldInfo(BaseModel):
    """Informações sobre um campo identificado"""
    field_id: str = Field(..., description="ID único do campo")
    label: str = Field(..., description="Label descritivo do campo")
    type: FieldType = Field(..., description="Tipo de dado do campo")
    required: bool = Field(default=True, description="Se o campo é obrigatório")
    original_text: str = Field(..., description="Texto original encontrado no documento")
    context: str = Field(default="", description="Contexto/seção onde o campo aparece")
    placeholder: Optional[str] = Field(None, description="Texto placeholder sugerido")
    section: Optional[str] = Field(None, description="Seção do contrato (ex: COMPRADOR, VENDEDOR)")
    section_id: Optional[str] = Field(None, description="ID da seção para agrupamento")
    options: Optional[List[str]] = Field(None, description="Opções para campos SELECT")
    mask: Optional[str] = Field(None, description="Máscara de input para o campo")
    found_in_document: Optional[bool] = Field(None, description="Se o campo foi encontrado no documento")


class UploadResponse(BaseModel):
    """Resposta do upload"""
    document_id: str
    filename: str
    message: str


class SectionInfo(BaseModel):
    """Informações sobre uma seção"""
    id: str
    name: str


class AnalysisResponse(BaseModel):
    """Resposta da análise do documento"""
    document_id: str
    fields: List[FieldInfo]
    sections: List[SectionInfo] = Field(default_factory=list, description="Seções identificadas no documento")
    total_fields: int


class FillResponse(BaseModel):
    """Resposta do preenchimento"""
    filled_document_id: str
    message: str
