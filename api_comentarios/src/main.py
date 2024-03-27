import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify
from api.database import insert_comment, get_comments_by_content_id  # Importando a função get_comments_by_content_id
import psycopg2

app = Flask(__name__)

# Configurações de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Função para conectar ao banco de dados
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="admin",
            user="admin",
            password="admin",
            host="db"
        )
        return conn
    except psycopg2.OperationalError as e:
        logger.error('Erro ao conectar ao banco de dados: %s', str(e))
        raise

@app.route('/api/comment/new', methods=['POST'])
def criar_comentario_api():
    try:
        data = request.json
        email = data['email']
        comentario = data['comment']
        content_id = data['content_id']

        # Inserir dados no banco de dados "admin" a tabela "comentarios"
        insert_comment(comentario, email, content_id)

        logger.info('Novo comentário criado por %s na matéria %s', email, content_id)

        return jsonify({'mensagem': 'Comentário criado com sucesso'}), 201

    except KeyError as e:
        logger.error('Chave faltando nos dados da solicitação: %s', str(e))
        return jsonify({'erro': 'Chave faltando nos dados da solicitação'}), 400

    except Exception as e:
        logger.error('Erro ao criar comentário: %s', str(e))
        return jsonify({'erro': str(e)}), 500

@app.route('/api/comment/list/<int:content_id>', methods=['GET'])
def listar_comentarios(content_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Execute a consulta para recuperar os comentários associados ao content_id
        cursor.execute('SELECT content_id, texto, email, autor FROM comentarios WHERE content_id = %s', (content_id,))
        comentarios = cursor.fetchall()

        # Feche a conexão com o banco de dados
        conn.close()

        lista_comentarios = [{'id': c[0], 'comment': c[1], 'email': c[2], 'autor': c[3]} for c in comentarios]
        return jsonify(lista_comentarios), 200

    except Exception as e:
        logger.error('Erro ao listar comentários: %s', str(e))
        return jsonify({'erro': str(e)}), 500

# Definição de uma rota para verificar a saúde da aplicação
@app.route('/health')
def health_check():
    return jsonify({'status': 'OK'})

# Verifica se este script está sendo executado diretamente pelo Python
if __name__ == '__main__':
    logger.info('Iniciando a aplicação...')
    # Inicia o servidor da aplicação Flask
    app.run(host='0.0.0.0', port=8000, debug=False)
