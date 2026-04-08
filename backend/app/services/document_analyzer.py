"""
Serviço principal para análise de documentos
Combina parser e IA para gerar análise completa
"""
import os
from typing import List
from app.services.document_parser import DocumentParser
from app.services.ai_analyzer import AIAnalyzer
from app.models.schemas import AnalysisResponse, FieldInfo


class DocumentAnalyzer:
    """Orquestra a análise completa do documento"""
    
    def __init__(self):
        self.parser = DocumentParser()
        # Inicializar AIAnalyzer apenas quando necessário (lazy loading)
        self._ai_analyzer = None
    
    @property
    def ai_analyzer(self):
        """Obtém o AIAnalyzer, inicializando se necessário"""
        if self._ai_analyzer is None:
            self._ai_analyzer = AIAnalyzer()
        return self._ai_analyzer
    
    async def analyze_document(self, docx_path: str) -> AnalysisResponse:
        """
        Analisa documento completo e retorna campos identificados
        """
        try:
            # Extrair texto
            print(f"Extraindo texto do documento: {docx_path}")
            document_text = self.parser.extract_text(docx_path)
            
            if not document_text or len(document_text.strip()) == 0:
                raise ValueError("O documento está vazio ou não pôde ser lido corretamente")
            
            print(f"Texto extraído: {len(document_text)} caracteres")
            
            # Encontrar placeholders
            placeholder_matches = self.parser.find_placeholders(document_text)
            print(f"Placeholders encontrados: {len(placeholder_matches)}")
            
            # Preparar dados dos placeholders com contexto
            placeholders = []
            for placeholder_text, start, end in placeholder_matches:
                context = self.parser.get_context_around_placeholder(
                    document_text, start, end
                )
                placeholders.append({
                    "text": placeholder_text,
                    "start": start,
                    "end": end,
                    "context": context
                })
            
            # Usar IA para análise inteligente
            print("Iniciando análise com IA...")
            print(f"Documento tem {len(document_text)} caracteres")
            print(f"Encontrados {len(placeholders)} placeholders para analisar")
            
            import time
            start_time = time.time()
            fields = await self.ai_analyzer.analyze_fields(document_text, placeholders)
            elapsed_time = time.time() - start_time
            print(f"Análise concluída em {elapsed_time:.2f} segundos")
            print(f"Campos identificados: {len(fields)}")
            
            # Extrair seções únicas
            sections = list(set([f.section for f in fields if f.section]))
            
            # Gerar document_id a partir do caminho do arquivo
            document_id = os.path.basename(docx_path).replace('.docx', '')
            
            return AnalysisResponse(
                document_id=document_id,
                fields=fields,
                sections=sections,
                total_fields=len(fields)
            )
        except Exception as e:
            print(f"Erro em analyze_document: {str(e)}")
            import traceback
            print(traceback.format_exc())
            raise
