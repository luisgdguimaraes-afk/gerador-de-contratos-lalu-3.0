"""
Serviço para gerenciamento de armazenamento temporário de documentos
"""
import os
import aiofiles
import time
from pathlib import Path
from typing import Optional
from fastapi import UploadFile


class DocumentStorage:
    """Gerencia o armazenamento temporário de documentos"""
    
    def __init__(self, temp_dir: str = "./temp"):
        self.temp_dir = Path(temp_dir)
        self.output_dir = Path("./output")
        self.temp_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        print(f"DocumentStorage inicializado. Diretório temp: {self.temp_dir.absolute()}")
        print(f"DocumentStorage inicializado. Diretório output: {self.output_dir.absolute()}")
    
    async def save_uploaded_file(self, document_id: str, file: UploadFile) -> str:
        """
        Salva um arquivo enviado e retorna o caminho completo
        """
        file_path = self.temp_dir / f"{document_id}.docx"
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        return str(file_path)
    
    def get_file_path(self, document_id: str) -> str:
        """
        Retorna o caminho do arquivo baseado no document_id
        """
        return str(self.temp_dir / f"{document_id}.docx")
    
    def get_filled_file_path(self, document_id: str) -> str:
        """
        Retorna o caminho do arquivo preenchido (PDF)
        Agora sempre retorna PDF, não DOCX
        """
        # Remover extensão se houver
        if document_id.endswith('.pdf'):
            return str(self.output_dir / document_id)
        if document_id.endswith('.docx'):
            document_id = document_id.replace('.docx', '')
        return str(self.output_dir / f"{document_id}.pdf")
    
    def get_temp_file_path(self, filename: str) -> str:
        """
        Retorna caminho para arquivo temporário
        """
        return str(self.temp_dir / filename)
    
    def get_output_dir(self) -> str:
        """
        Retorna diretório de saída
        """
        return str(self.output_dir)
    
    def get_temp_dir(self) -> str:
        """
        Retorna diretório temporário.
        Útil para gerar arquivos intermediários (ex: PDFs a serem mesclados).
        """
        return str(self.temp_dir)
    
    def cleanup_temp_files(self, max_age_hours: int = 24):
        """
        Remove arquivos temporários antigos
        """
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        for file_path in self.temp_dir.iterdir():
            if file_path.is_file():
                file_age = current_time - file_path.stat().st_mtime
                if file_age > max_age_seconds:
                    file_path.unlink()
    
    def delete_file(self, document_id: str) -> bool:
        """
        Remove um arquivo do armazenamento temporário
        Retorna True se o arquivo foi deletado, False caso contrário
        """
        file_path = self.temp_dir / f"{document_id}.docx"
        filled_path = self.temp_dir / f"{document_id}_filled.docx"
        pdf_path = self.output_dir / f"{document_id}.pdf"
        
        deleted = False
        if file_path.exists():
            file_path.unlink()
            deleted = True
        
        if filled_path.exists():
            filled_path.unlink()
            deleted = True
        
        if pdf_path.exists():
            pdf_path.unlink()
            deleted = True
        
        return deleted
