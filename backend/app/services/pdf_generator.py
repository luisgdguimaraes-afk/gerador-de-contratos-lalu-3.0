"""
Serviço para conversão de DOCX para PDF usando LibreOffice (soffice)
"""
import os
import subprocess
import time
from pathlib import Path
from app.services.document_storage import DocumentStorage


class PDFGenerator:
    """Converte documentos DOCX para PDF usando LibreOffice (sem depender do Word)."""
    
    def __init__(self):
        self.storage = DocumentStorage()
    
    def _get_libreoffice_executable(self) -> str:
        """
        Retorna o executável do LibreOffice.
        Por padrão usa 'soffice', mas pode ser sobrescrito com a variável de ambiente LIBREOFFICE_PATH.
        No Windows, tenta encontrar automaticamente em locais comuns.
        """
        # Verificar variável de ambiente primeiro
        env_path = os.getenv("LIBREOFFICE_PATH")
        if env_path:
            return env_path
        
        # Tentar encontrar no PATH
        import shutil
        soffice_path = shutil.which("soffice")
        if soffice_path:
            return soffice_path
        
        # No Windows, tentar locais comuns
        if os.name == 'nt':  # Windows
            common_paths = [
                r"C:\Program Files\LibreOffice\program\soffice.exe",
                r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
            ]
            for path in common_paths:
                if os.path.exists(path):
                    return path
        
        # Fallback: retornar 'soffice' e deixar o subprocess gerar erro se não encontrar
        return "soffice"
    
    async def convert_to_pdf(self, docx_path: str, document_id: str, output_dir: str = None) -> str:
        """
        Converte DOCX para PDF usando LibreOffice em modo headless.
        Retorna o caminho do arquivo PDF gerado.
        
        Args:
            docx_path: Caminho do arquivo DOCX
            document_id: ID do documento (sem extensão)
            output_dir: Diretório de saída (opcional, usa o mesmo do DOCX se não informado)
        """
        if output_dir:
            output_dir_path = Path(output_dir)
        else:
            output_dir_path = Path(docx_path).parent
        
        # PDF esperado com o nome do document_id
        pdf_path = output_dir_path / f"{document_id}.pdf"
        
        # Verificar se o arquivo DOCX existe
        if not os.path.exists(docx_path):
            raise Exception(f"Arquivo DOCX não encontrado: {docx_path}")
        
        # Garantir que o diretório de saída existe
        output_dir_path.mkdir(parents=True, exist_ok=True)
        
        libreoffice_exec = self._get_libreoffice_executable()
        
        # O LibreOffice gera o PDF com o nome baseado no arquivo DOCX original
        # Precisamos detectar o nome real do PDF gerado e renomeá-lo
        docx_path_obj = Path(docx_path).resolve()  # Garantir caminho absoluto
        docx_name_without_ext = docx_path_obj.stem  # Nome sem extensão
        expected_libreoffice_pdf = output_dir_path.resolve() / f"{docx_name_without_ext}.pdf"
        
        # Garantir que o caminho do DOCX é absoluto (necessário no Windows)
        abs_docx_path = str(docx_path_obj)
        abs_output_dir = str(output_dir_path.resolve())
        
        cmd = [
            libreoffice_exec,
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            abs_output_dir,
            abs_docx_path,
        ]
        
        print(f"Convertendo via LibreOffice: {cmd}")
        print(f"PDF esperado pelo LibreOffice: {expected_libreoffice_pdf}")
        print(f"PDF final desejado: {pdf_path}")
        
        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=180,  # 3 minutos
            )
            
            print(f"LibreOffice stdout: {result.stdout}")
            print(f"LibreOffice stderr: {result.stderr}")
            print(f"LibreOffice returncode: {result.returncode}")
            
            if result.returncode != 0:
                raise Exception(
                    f"Erro na conversão via LibreOffice (código {result.returncode}): "
                    f"{result.stderr or result.stdout}"
                )
            
            # O LibreOffice gera o PDF com o nome baseado no DOCX original
            # Aguardar um pouco para garantir que o arquivo foi escrito completamente
            time.sleep(0.5)
            
            # Verificar se o PDF foi criado com o nome esperado
            if not expected_libreoffice_pdf.exists():
                # Tentar encontrar o PDF gerado baseado no nome do DOCX temporário
                # O nome do DOCX temporário deve corresponder ao PDF gerado
                docx_stem = docx_path_obj.stem  # Nome do DOCX sem extensão
                print(f"[PDF_GENERATOR] Procurando PDF com nome baseado em: {docx_stem}")
                
                # Listar todos os PDFs no diretório
                pdf_files = list(output_dir_path.resolve().glob("*.pdf"))
                print(f"[PDF_GENERATOR] PDFs encontrados no diretório: {[f.name for f in pdf_files]}")
                
                # Tentar encontrar PDF que corresponde ao nome do DOCX
                matching_pdf = None
                for pdf_file in pdf_files:
                    if pdf_file.stem == docx_stem:
                        matching_pdf = pdf_file
                        print(f"[PDF_GENERATOR] PDF correspondente encontrado: {matching_pdf}")
                        break
                
                if matching_pdf:
                    expected_libreoffice_pdf = matching_pdf
                elif pdf_files:
                    # Se não encontrou correspondência exata, usar o mais recente
                    expected_libreoffice_pdf = max(pdf_files, key=lambda p: p.stat().st_mtime)
                    print(f"[PDF_GENERATOR] AVISO: Usando PDF mais recente encontrado: {expected_libreoffice_pdf}")
                else:
                    raise Exception(f"PDF não foi gerado pelo LibreOffice. Esperado: {expected_libreoffice_pdf}")
            
            # Verificar se o PDF não está vazio
            if expected_libreoffice_pdf.stat().st_size == 0:
                raise Exception("PDF gerado está vazio.")
            
            # Se o nome do PDF gerado é diferente do esperado, renomear
            pdf_path_resolved = pdf_path.resolve()
            if expected_libreoffice_pdf.resolve() != pdf_path_resolved:
                print(f"[PDF_GENERATOR] Renomeando PDF de {expected_libreoffice_pdf} para {pdf_path_resolved}")
                if pdf_path_resolved.exists():
                    pdf_path_resolved.unlink()  # Remover PDF antigo se existir
                expected_libreoffice_pdf.rename(pdf_path_resolved)
                print(f"[PDF_GENERATOR] PDF renomeado com sucesso")
            else:
                print(f"[PDF_GENERATOR] PDF já está com o nome correto: {pdf_path_resolved}")
            
            # Garantir que o caminho retornado é o correto
            final_pdf_path = pdf_path_resolved
            
            # Verificação final: garantir que o arquivo existe e tem o nome correto
            if not final_pdf_path.exists():
                raise Exception(f"PDF final não encontrado após renomeação: {final_pdf_path}")
            
            print(f"[PDF_GENERATOR] PDF final confirmado: {final_pdf_path.name}")
            
            print(f"PDF gerado com sucesso: {final_pdf_path} (tamanho: {final_pdf_path.stat().st_size} bytes)")
            return str(final_pdf_path)
        
        except subprocess.TimeoutExpired:
            raise Exception("Timeout na conversão para PDF via LibreOffice (processo demorou demais).")
        except FileNotFoundError:
            raise Exception(
                "LibreOffice (soffice) não foi encontrado no sistema.\n\n"
                "Verifique se o LibreOffice está instalado e se o executável 'soffice' "
                "está no PATH, ou defina a variável de ambiente LIBREOFFICE_PATH "
                "com o caminho completo para o executável."
            )
        except Exception as e:
            raise Exception(f"Erro ao converter para PDF via LibreOffice: {str(e)}")
