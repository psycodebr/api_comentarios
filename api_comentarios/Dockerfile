# Imagem oficial do Python
FROM python:3.8-slim

# Define as variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    postgresql-client

# Instala as dependências do Python
COPY src/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia o conteúdo do diretório atual para o contêiner em /app
COPY . /app/

# Copia o script de entrada para o contêiner
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# Define o script de entrada como executável
RUN chmod +x /usr/local/bin/entrypoint.sh

# Expõe a porta 8000
EXPOSE 8000

# Executa a aplicação
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
