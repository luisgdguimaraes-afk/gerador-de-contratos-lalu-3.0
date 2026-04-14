"""
Serviço para conversão de DOCX para PDF usando LibreOffice (soffice)
"""
import asyncio
import glob
import os
import subprocess
import time
from pathlib import Path
from typing import Optional

from app.services.document_storage import DocumentStorage


class PDFGenerator:
    """Converte documentos DOCX para PDF usando LibreOffice (sem depender do Word)."""
    
    def __init__(self):
        self.storage = DocumentStorage()
    
    def _find_libreoffice_windows_glob(self) -> Optional[str]:
        """Localiza soffice.exe em instalações LibreOffice 7.x, 24.x, etc."""
        bases = []
        pf = os.environ.get("ProgramFiles")
        pfx86 = os.environ.get("ProgramFiles(x86)")
        if pf:
            bases.append(pf)
        if pfx86:
            bases.append(pfx86)
        if not bases:
            bases = [r"C:\Program Files", r"C:\Program Files (x86)"]
        for base in bases:
            pattern = os.path.join(base, "LibreOffice*", "program", "soffice.exe")
            matches = sorted(glob.glob(pattern), reverse=True)
            if matches:
                return matches[0]
        local = os.environ.get("LOCALAPPDATA")
        if local:
            pattern = os.path.join(local, "Programs", "LibreOffice*", "program", "soffice.exe")
            matches = sorted(glob.glob(pattern), reverse=True)
            if matches:
                return matches[0]
        return None
    
    def _get_libreoffice_executable(self) -> Optional[str]:
        """
        Retorna o executável do LibreOffice, ou None se não existir no sistema.
        Ordem: LIBREOFFICE_PATH → PATH → caminhos comuns no Windows (incl. LibreOffice*).
        """
        env_path = os.getenv("LIBREOFFICE_PATH")
        if env_path:
            env_path = env_path.strip().strip('"')
            if os.path.isfile(env_path):
                return env_path
            candidate = os.path.join(env_path, "soffice.exe")
            if os.path.isfile(candidate):
                return candidate
        
        import shutil
        soffice_path = shutil.which("soffice")
        if soffice_path:
            return soffice_path
        
        if os.name == "nt":
            common_paths = [
                r"C:\Program Files\LibreOffice\program\soffice.exe",
                r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
            ]
            for path in common_paths:
                if os.path.exists(path):
                    return path
            found = self._find_libreoffice_windows_glob()
            if found:
                return found
        
        return None
    
    def _convert_via_docx2pdf(self, docx_path: str, pdf_path: str) -> bool:
        """Fallback no Windows: Microsoft Word via pacote docx2pdf (já em requirements)."""
        try:
            from docx2pdf import convert
            convert(docx_path, pdf_path)
            p = Path(pdf_path)
            return p.exists() and p.stat().st_size > 0
        except Exception as e:
            print(f"[PDF_GENERATOR] docx2pdf (Word) falhou: {e}")
            return False
    
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
        
        docx_path_obj = Path(docx_path).resolve()
        docx_name_without_ext = docx_path_obj.stem
        expected_libreoffice_pdf = output_dir_path.resolve() / f"{docx_name_without_ext}.pdf"
        abs_docx_path = str(docx_path_obj)
        abs_output_dir = str(output_dir_path.resolve())
        pdf_path_resolved = pdf_path.resolve()
        
        libreoffice_exec = self._get_libreoffice_executable()
        
        if libreoffice_exec is None:
            if os.name == "nt":
                ok = await asyncio.to_thread(
                    self._convert_via_docx2pdf, abs_docx_path, str(pdf_path_resolved)
                )
                if ok:
                    print(f"[PDF_GENERATOR] PDF gerado via Microsoft Word (docx2pdf): {pdf_path_resolved}")
                    return str(pdf_path_resolved)
            raise Exception(
                "LibreOffice (soffice) não foi encontrado no sistema.\n\n"
                "Instale o LibreOffice em https://www.libreoffice.org (recomendado) ou defina "
                "LIBREOFFICE_PATH com o caminho completo do executável soffice.exe.\n\n"
                "No Windows, se o Microsoft Word estiver instalado, o sistema também tenta "
                "converter por ele automaticamente."
            )
        
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
            if os.name == "nt":
                ok = await asyncio.to_thread(
                    self._convert_via_docx2pdf, abs_docx_path, str(pdf_path_resolved)
                )
                if ok:
                    print(f"[PDF_GENERATOR] PDF gerado via Microsoft Word (docx2pdf): {pdf_path_resolved}")
                    return str(pdf_path_resolved)
            raise Exception(
                "LibreOffice (soffice) não foi encontrado no sistema.\n\n"
                "Instale o LibreOffice em https://www.libreoffice.org ou defina LIBREOFFICE_PATH "
                "com o caminho completo do soffice.exe.\n\n"
                "No Windows, com Microsoft Word instalado, a conversão também pode funcionar automaticamente."
            )
        except Exception as e:
            raise Exception(f"Erro ao converter para PDF via LibreOffice: {str(e)}")
