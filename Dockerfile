FROM python:3.9-slim

WORKDIR /app

# Instala dependências do sistema (opcional, para OCR)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do projeto
COPY . .

# Expõe a porta 8000
EXPOSE 8000

# Comando para rodar o serviço
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]