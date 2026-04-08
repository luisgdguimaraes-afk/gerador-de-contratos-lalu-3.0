"""
Serviço para gerenciar templates de contratos hospedados no backend.

Agora suporta múltiplos documentos por template (ex: Quadro Resumo + Condições Gerais).
"""
from pathlib import Path
from typing import List, Dict


class TemplateService:
    """Serviço para gerenciar templates de contratos"""

    TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"

    # Mapeamento de templates disponíveis e seus documentos
    AVAILABLE_TEMPLATES: Dict[str, Dict] = {
        "rota_do_sol": {
            "name": "Contrato Residencial Rota do Sol",
            "description": "Contrato de compra e venda do loteamento Residencial Rota do Sol",
            "documents": [
                {
                    "id": "quadro_resumo",
                    "filename": "CONTRATO_ROTA_DO_SOL_TEMPLATE.docx",
                    "name": "Quadro Resumo",
                    "order": 1,
                },
                {
                    "id": "condicoes_gerais",
                    "filename": "CONDICOES_GERAIS_TEMPLATE.docx",
                    "name": "Condições Gerais",
                    "order": 2,
                },
            ],
        }
    }

    @classmethod
    def get_template_documents(cls, template_id: str = "rota_do_sol") -> List[Dict]:
        """
        Retorna lista de documentos configurados para um template.

        Cada item contém:
        - id
        - name
        - path (caminho absoluto do arquivo DOCX)
        - order
        """
        if template_id not in cls.AVAILABLE_TEMPLATES:
            raise ValueError(f"Template '{template_id}' não encontrado")

        template = cls.AVAILABLE_TEMPLATES[template_id]
        documents: List[Dict] = []

        for doc in sorted(template.get("documents", []), key=lambda x: x.get("order", 0)):
            doc_path = cls.TEMPLATES_DIR / doc["filename"]
            if not doc_path.exists():
                raise FileNotFoundError(f"Arquivo de template não encontrado: {doc_path}")

            documents.append(
                {
                    "id": doc["id"],
                    "name": doc["name"],
                    "path": str(doc_path),
                    "order": doc.get("order", 0),
                }
            )

        return documents

    @classmethod
    def get_template_path(cls, template_id: str = "rota_do_sol", document_id: str = "quadro_resumo") -> Path:
        """
        Retorna o caminho completo de um documento específico do template.

        Compatível com chamadas antigas que não passam document_id
        (nesse caso, usa sempre o documento principal 'quadro_resumo').
        """
        documents = cls.get_template_documents(template_id)
        for doc in documents:
            if doc["id"] == document_id:
                return Path(doc["path"])

        raise ValueError(f"Documento '{document_id}' não encontrado para o template '{template_id}'")

    @classmethod
    def list_templates(cls) -> List[Dict]:
        """Lista todos os templates disponíveis (sem detalhes de caminho dos arquivos)."""
        return [
            {
                "id": template_id,
                "name": template_info.get("name"),
                "description": template_info.get("description"),
                "documents": [
                    {"id": d["id"], "name": d["name"], "order": d.get("order", 0)}
                    for d in template_info.get("documents", [])
                ],
            }
            for template_id, template_info in cls.AVAILABLE_TEMPLATES.items()
        ]

    @classmethod
    def get_default_template_id(cls) -> str:
        """Retorna o ID do template padrão"""
        return "rota_do_sol"
