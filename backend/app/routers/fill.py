"""
Rota para preencher documentos de contrato e gerar PDF final.

Agora suporta múltiplos documentos (ex: Quadro Resumo + Condições Gerais),
mesclando tudo em um único PDF para download.
"""
import os
import uuid
from typing import Dict, Any, Optional, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.document_filler import DocumentFiller
from app.services.document_storage import DocumentStorage
from app.services.template_service import TemplateService
from app.services.pdf_generator import PDFGenerator

router = APIRouter()
filler = DocumentFiller()
storage = DocumentStorage()
pdf_generator = PDFGenerator()


class FillTemplateRequest(BaseModel):
    template_id: Optional[str] = "rota_do_sol"
    fields: Dict[str, Any]  # field_id -> value
    buyer_type: Optional[str] = None  # "PF" ou "PJ" - se None, será detectado automaticamente


@router.post("/fill")
async def fill_template(request: FillTemplateRequest):
    """
    Preenche todos os documentos do template com os dados fornecidos
    e converte cada um para um PDF separado.
    """
    import traceback

    try:
        import sys
        print(f"[FILL] ========== INÍCIO DA REQUISIÇÃO ==========", flush=True)
        print(f"[FILL] Recebendo requisição para preencher template: {request.template_id}", flush=True)
        print(f"[FILL] Campos recebidos: {len(request.fields)} campos", flush=True)

        # Detectar ou usar buyer_type fornecido (mantido para logs e compatibilidade)
        buyer_type = request.buyer_type
        if not buyer_type:
            buyer_type = filler._detect_buyer_type(request.fields) or "PF"
        print(f"[FILL] Tipo de comprador detectado: {buyer_type}", flush=True)

        # Gerar ID único base para todos os documentos relacionados
        document_id = str(uuid.uuid4())
        print(f"[FILL] ID base do documento: {document_id}", flush=True)

        # Obter lista de documentos configurados para o template
        template_docs = TemplateService.get_template_documents(request.template_id)
        print(f"[FILL] {len(template_docs)} documentos encontrados para o template: {[d['id'] for d in template_docs]}", flush=True)
        import sys
        sys.stdout.flush()

        documents_info: List[Dict[str, str]] = []
        errors: List[str] = []

        print(f"[FILL] Iniciando loop para processar {len(template_docs)} documentos...", flush=True)
        sys.stdout.flush()

        for idx, doc_info in enumerate(template_docs, 1):
            doc_id = doc_info["id"]
            template_path = doc_info["path"]
            temp_docx_path = None
            
            try:
                print(f"[FILL] ===== Processando documento {idx}/{len(template_docs)}: '{doc_id}' =====", flush=True)
                print(f"[FILL] Caminho do template: {template_path}", flush=True)
                
                # Verificar se o arquivo template existe
                if not os.path.exists(template_path):
                    error_msg = f"Template não encontrado: {template_path}"
                    print(f"[FILL] ERRO: {error_msg}")
                    errors.append(f"Documento '{doc_id}': {error_msg}")
                    continue  # Pular este documento e continuar com o próximo

                # Preencher DOCX em memória
                print(f"[FILL] Preenchendo DOCX em memória...")
                filled_doc = filler.fill_document_from_path(str(template_path), request.fields)
                print(f"[FILL] DOCX preenchido com sucesso")

                # Salvar DOCX temporário
                temp_docx_name = f"{document_id}_{doc_id}.docx"
                temp_docx_path = storage.get_temp_file_path(temp_docx_name)
                os.makedirs(os.path.dirname(temp_docx_path), exist_ok=True)
                filled_doc.save(temp_docx_path)
                print(f"[FILL] DOCX temporário salvo em: {temp_docx_path}")

                if not os.path.exists(temp_docx_path):
                    error_msg = f"Arquivo DOCX não foi salvo corretamente: {temp_docx_path}"
                    print(f"[FILL] ERRO: {error_msg}")
                    errors.append(f"Documento '{doc_id}': {error_msg}")
                    continue

                # Converter DOCX para PDF diretamente no diretório de saída
                final_download_id = f"{document_id}_{doc_id}"
                print(f"[FILL] Convertendo '{doc_id}' para PDF com ID: {final_download_id}")
                print(f"[FILL] Diretório de saída: {storage.get_output_dir()}")
                
                final_pdf_path = await pdf_generator.convert_to_pdf(
                    temp_docx_path,
                    final_download_id,  # ID sem extensão .pdf (o método já adiciona)
                    storage.get_output_dir(),  # Salvar direto no output, não em temp
                )
                print(f"[FILL] PDF final de '{doc_id}' gerado em: {final_pdf_path}")
                print(f"[FILL] Nome do arquivo PDF: {os.path.basename(final_pdf_path)}")
                
                # Verificar se o PDF foi criado corretamente
                if not os.path.exists(final_pdf_path):
                    error_msg = f"PDF não foi gerado corretamente: {final_pdf_path}"
                    print(f"[FILL] ERRO: {error_msg}")
                    errors.append(f"Documento '{doc_id}': {error_msg}")
                    continue
                
                # Verificar se o nome do arquivo está correto
                expected_filename = f"{final_download_id}.pdf"
                actual_filename = os.path.basename(final_pdf_path)
                if actual_filename != expected_filename:
                    print(f"[FILL] AVISO: Nome do arquivo diferente do esperado!")
                    print(f"[FILL] Esperado: {expected_filename}")
                    print(f"[FILL] Atual: {actual_filename}")
                    # Tentar renomear para o nome correto
                    correct_path = os.path.join(os.path.dirname(final_pdf_path), expected_filename)
                    if os.path.exists(correct_path):
                        os.remove(correct_path)
                    os.rename(final_pdf_path, correct_path)
                    final_pdf_path = correct_path
                    print(f"[FILL] Arquivo renomeado para: {final_pdf_path}")

                documents_info.append(
                    {
                        "id": doc_id,
                        "name": doc_info["name"],
                        "download_id": final_download_id,
                    }
                )
                print(f"[FILL] OK - Documento '{doc_id}' processado com sucesso! Total processados: {len(documents_info)}", flush=True)
                print(f"[FILL] Arquivo PDF final: {final_pdf_path}", flush=True)
                print(f"[FILL] Download ID: {final_download_id}", flush=True)
                
            except Exception as doc_error:
                error_trace = traceback.format_exc()
                error_msg = f"Erro ao processar documento '{doc_id}': {str(doc_error)}"
                print(f"[FILL] ERRO: {error_msg}", flush=True)
                print(f"[FILL] Traceback completo:\n{error_trace}", flush=True)
                errors.append(error_msg)
                # Continuar processando os outros documentos mesmo se este falhar
                continue
            finally:
                # Sempre tentar remover o DOCX temporário
                if temp_docx_path and os.path.exists(temp_docx_path):
                    try:
                        os.remove(temp_docx_path)
                        print(f"[FILL] DOCX temporário removido: {temp_docx_path}")
                    except Exception as e:
                        print(f"[FILL] AVISO: Não foi possível remover DOCX temporário: {e}")

        if not documents_info:
            error_summary = "\n".join(errors) if errors else "Nenhum erro específico registrado"
            raise Exception(f"Nenhum documento foi gerado para o template informado.\nErros encontrados:\n{error_summary}")
        
        if errors:
            print(f"[FILL] AVISO: {len(errors)} erro(s) ocorreram durante o processamento, mas {len(documents_info)} documento(s) foram gerados com sucesso.")
            for error in errors:
                print(f"[FILL]   - {error}")

        # Mantém compatibilidade com o frontend atual, que espera 'filled_document_id'
        # filled_document_id agora aponta para o primeiro documento (ex: quadro_resumo)
        primary_download_id = documents_info[0]["download_id"]

        print(f"[FILL] ========== FIM DA REQUISIÇÃO ==========", flush=True)
        print(f"[FILL] Total de documentos gerados: {len(documents_info)}", flush=True)
        print(f"[FILL] Documentos: {[d['id'] for d in documents_info]}", flush=True)
        print(f"[FILL] Download IDs: {[d['download_id'] for d in documents_info]}", flush=True)

        return {
            "success": True,
            "filled_document_id": primary_download_id,
            "message": "Contratos gerados com sucesso em PDF.",
            "format": "pdf",
            "documents_count": len(documents_info),
            "documents": documents_info,
        }

    except ValueError as e:
        error_trace = traceback.format_exc()
        print(f"Erro ValueError: {str(e)}")
        print(f"Traceback: {error_trace}")
        raise HTTPException(status_code=404, detail=str(e))
    except FileNotFoundError as e:
        error_trace = traceback.format_exc()
        print(f"Erro FileNotFoundError: {str(e)}")
        print(f"Traceback: {error_trace}")
        raise HTTPException(status_code=500, detail=f"Template não encontrado: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Erro ao gerar contrato: {str(e)}")
        print(f"Traceback completo: {error_trace}")
        raise HTTPException(status_code=500, detail=f"Erro ao gerar contrato: {str(e)}")
