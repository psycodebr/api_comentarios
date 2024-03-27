import psycopg2
from psycopg2 import OperationalError
import sys

# Parâmetros de conexão com o banco de dados PostgreSQL
DB_HOST = 'db'
DB_NAME = 'admin'
DB_USER = 'admin'
DB_PASSWORD = 'admin'

# Função para conectar ao banco de dados PostgreSQL
def connect():
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

# Criação da tabela 'comentarios' com a coluna 'content_id'
def create_table_with_content_id():
    print("Criando tabela 'comentarios' com a coluna 'content_id'...")  
    conn = None
    try:
        conn = connect()
        cursor = conn.cursor()
        # Verifica se a tabela já existe antes de criar
        cursor.execute('''CREATE TABLE IF NOT EXISTS comentarios
                          (content_id SERIAL PRIMARY KEY, texto TEXT, autor TEXT, insert_comment TEXT, email VARCHAR(255), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        cursor.close()
        print("Tabela 'comentarios' criada com sucesso.")  
    except OperationalError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    finally:
        if conn:
            conn.close()

        # Verifica se a coluna 'content_id' já existe na tabela 'comentarios'
        if 'already exists' in str(e):
            print("A coluna 'content_id' já existe na tabela 'comentarios'.")
        else:
            print(f"Erro ao criar a tabela 'comentarios': {e}")

# Função para inserir um comentário no banco de dados
def insert_comment(texto, autor, content_id):
    conn = None
    try:
        conn = connect()
        cursor = conn.cursor()
        # Executa a inserção do comentário na tabela 'comentarios'
        cursor.execute("INSERT INTO comentarios (texto, autor, content_id) VALUES (%s, %s, %s)", (texto, autor, content_id))
        conn.commit()
        cursor.close()
    except OperationalError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    finally:
        if conn:
            conn.close()

# Função para obter todos os comentários do banco de dados
def get_comments():
    conn = None
    try:
        conn = connect()
        cursor = conn.cursor()
        # Executa a consulta para obter todos os comentários da tabela 'comentarios'
        cursor.execute("SELECT * FROM comentarios")
        comentarios = cursor.fetchall()
        cursor.close()
        return comentarios
    except OperationalError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    finally:
        if conn:
            conn.close()

# Função para obter todos os comentários de um determinado conteúdo (content_id)
def get_comments_by_content_id(content_id):
    conn = None
    try:
        conn = connect()
        cursor = conn.cursor()
        # Executa a consulta para obter os comentários com o content_id especificado
        cursor.execute("SELECT * FROM comentarios WHERE content_id = %s", (content_id,))
        comentarios = cursor.fetchall()
        cursor.close()
        return comentarios
    except OperationalError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    finally:
        if conn:
            conn.close()

# Verifica se o script está sendo executado a partir da linha de comando
if __name__ == '__main__':
    # Verifica se o argumento 'create_table' foi passado pela linha de comando
    if len(sys.argv) > 1 and sys.argv[1] == 'create_table':
        create_table_with_content_id()

# Função para execução de migrações do banco de dados
def migrate():
    """
    Executa migrações do banco de dados.
    """
    print("Executando migrações...")
    create_table_with_content_id()
