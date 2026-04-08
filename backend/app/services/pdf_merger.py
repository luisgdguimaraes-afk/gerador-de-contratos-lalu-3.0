"""
Serviço para mesclar múltiplos PDFs em um único arquivo.

Tenta usar, nesta ordem:
- pdfunite (poppler-utils)
- pdftk
- ghostscript (gs)

Se nenhuma ferramenta estiver disponível, lança um erro explicando
o que precisa ser instalado.
"""
from pathlib import Path
from typing import List
import subprocess
import shutil


class PDFMerger:
    """Serviço para mesclar múltiplos PDFs em um único arquivo"""

    @staticmethod
    def merge_pdfs(pdf_paths: List[str], output_path: str) -> str:
        """
        Mescla múltiplos PDFs em um único arquivo.

        Args:
            pdf_paths: Lista de caminhos dos PDFs a mesclar (em ordem)
            output_path: Caminho do PDF de saída

        Returns:
            Caminho do PDF mesclado
        """
        if not pdf_paths:
            raise ValueError("Lista de PDFs vazia")

        # Normalizar caminhos
        pdf_paths = [str(Path(p).resolve()) for p in pdf_paths]
        output_path = str(Path(output_path).resolve())

        # Se só tem um PDF, apenas copia/renomeia
        if len(pdf_paths) == 1:
            src = Path(pdf_paths[0])
            dst = Path(output_path)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dst)
            return str(dst)

        # Garantir diretório de saída
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # 1) Tentar pdfunite (poppler-utils)
        try:
            cmd = ["pdfunite"] + pdf_paths + [output_path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0 and Path(output_path).exists():
                return output_path
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        # 2) Tentar pdftk
        try:
            cmd = ["pdftk"] + pdf_paths + ["cat", "output", output_path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0 and Path(output_path).exists():
                return output_path
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        # 3) Tentar ghostscript (gs)
        try:
            cmd = [
                "gs",
                "-dBATCH",
                "-dNOPAUSE",
                "-q",
                "-sDEVICE=pdfwrite",
                f"-sOutputFile={output_path}",
            ] + pdf_paths
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0 and Path(output_path).exists():
                return output_path
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        raise RuntimeError(
            "Não foi possível mesclar os PDFs. "
            "Instale pdfunite (poppler-utils), pdftk ou ghostscript para habilitar a mesclagem."
        )

    @staticmethod
    def is_merge_available() -> bool:
        """Verifica se alguma ferramenta de merge está disponível no sistema."""
        for cmd in ["pdfunite", "pdftk", "gs"]:
            try:
                # Para gs, '--help' já é suficiente para verificar presença
                args = [cmd, "--help"] if cmd == "gs" else [cmd, "--version"]
                result = subprocess.run(args, capture_output=True, timeout=5)
                if result.returncode == 0:
                    return True
            except Exception:
                continue
        return False

