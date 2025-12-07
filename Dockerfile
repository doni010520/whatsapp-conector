FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY app.py .
COPY index.html .

# Expor porta
EXPOSE 8010

# Comando para rodar a aplicação
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8010"]
