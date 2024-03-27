#!/bin/bash

# Definir o PYTHONPATH para incluir o diretório raiz do projeto
export PYTHONPATH=/Users/amzlabs/projeto-globo/api_comentarios/src

# Aguardar até que o serviço PostgreSQL esteja pronto
until PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -U "$DB_USER" -c '\q'; do
  >&2 echo "Postgres está indisponível - aguardando..."
  sleep 1
done

# Conceder todas as permissões ao usuário admin
echo "Concedendo todas as permissões ao usuário admin..."
PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c \
  "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;"
echo "Permissões concedidas."

# Verificar se a tabela 'comentarios' existe antes de criar
echo "Verificando se a tabela 'comentarios' existe..."
if PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c \
  "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'comentarios');" | grep -q "(t)"; then
  echo "Tabela 'comentarios' já existe."
else
  echo "Tabela 'comentarios' não existe. Criando..."
  PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c \
  "CREATE TABLE IF NOT EXISTS comentarios (
      content_id SERIAL,
      texto TEXT,
      insert_comment TEXT,
      email VARCHAR(255),
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      autor VARCHAR(255)
  );"
  echo "Tabela 'comentarios' criada."
fi

# Remover SERIAL PRIMARY KEY da coluna 'content_id'
echo "Removendo SERIAL PRIMARY KEY da coluna 'content_id'..."
if PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c \
  "ALTER TABLE comentarios DROP CONSTRAINT IF EXISTS comentarios_pkey;
   ALTER TABLE comentarios ALTER COLUMN content_id DROP DEFAULT;
   ALTER TABLE comentarios ALTER COLUMN content_id DROP NOT NULL;"; then
  echo "SERIAL PRIMARY KEY removido com sucesso da coluna 'content_id'."
else
  echo "Falha ao remover SERIAL PRIMARY KEY da coluna 'content_id'."
fi

# Executar migrações do banco de dados
echo "Executando migrações..."
python3 src/api/database.py migrate

# Iniciar a aplicação Flask
echo "Iniciando a aplicação Flask..."
python3 src/main.py
