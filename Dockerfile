# Use uma imagem base do Python
FROM python:3.9-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie o arquivo de requisitos (caso exista um) para dentro do container
COPY requirements.txt .

# Instale as dependências do arquivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copie todos os arquivos do diretório local para o diretório de trabalho no container
COPY . .

# Exponha a porta em que a aplicação Flask vai rodar
EXPOSE 5000

# Defina a variável de ambiente para o Flask
ENV FLASK_APP=app.py

# Comando para rodar a aplicação Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
