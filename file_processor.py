import io
import logging
from fastapi import UploadFile, HTTPException
from config import pypdf

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_text_from_file(file: UploadFile) -> str:
    logging.info(f"Iniciando extração do arquivo: {file.filename}")
    file_extension = file.filename.split('.')[-1].lower()
    
    if file_extension == 'txt':
        try:
            return file.file.read().decode("utf-8")
        except UnicodeDecodeError:
            file.file.seek(0)
            return file.file.read().decode("iso-8859-1")

    elif file_extension == 'pdf':
        if pypdf is None:
            raise HTTPException(status_code=500, detail="Biblioteca 'pypdf' não instalada para processar PDFs.")
        
        try:
            pdf_bytes = file.file.read()
            pdf_file = io.BytesIO(pdf_bytes)
            
            reader = pypdf.PdfReader(pdf_file)
            
            text_parts = [page.extract_text() for page in reader.pages]
            text = "\n".join(filter(None, text_parts))
            
            return text
        except Exception as e:
            logging.error(f"Erro ao processar PDF: {e}")
            raise HTTPException(status_code=400, detail=f"Erro ao processar PDF: {e}")

    else:
        raise HTTPException(status_code=400, detail="Formato de arquivo não suportado. Use .txt ou .pdf.")
