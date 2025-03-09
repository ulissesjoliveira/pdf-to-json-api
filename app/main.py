from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from PyPDF2 import PdfReader
import io
import logging

app = FastAPI()

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFRequest(BaseModel):
    pdf_url: str

@app.post("/convert-pdf")
async def convert_pdf(request: PDFRequest):
    try:
        logger.info(f"Iniciando conversão do PDF: {request.pdf_url}")

        # Validação básica da URL
        if not request.pdf_url.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="URL deve apontar para um PDF")

        # Baixar o PDF
        response = requests.get(request.pdf_url)
        response.raise_for_status()

        # Processar o PDF
        pdf_file = io.BytesIO(response.content)
        pdf = PdfReader(pdf_file)

        # Extrair texto
        text_data = {
            "pages": [
                {"page_number": i + 1, "content": page.extract_text()}
                for i, page in enumerate(pdf.pages)
            ],
            "metadata": {
                "total_pages": len(pdf.pages),
                "author": pdf.metadata.get('/Author', ''),
                "title": pdf.metadata.get('/Title', '')
            }
        }

        logger.info(f"PDF convertido com sucesso: {request.pdf_url}")
        return text_data

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao baixar o PDF: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Erro ao baixar o PDF: {str(e)}")
    except Exception as e:
        logger.error(f"Erro interno: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")