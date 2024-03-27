from flask import Blueprint, request, jsonify
from database import insert_comment, get_comments_with_email  # Importar função get_comments_with_email

# Criar um Blueprint para o módulo de API de comentários
comments_api = Blueprint('comments_api', __name__)

# Rota para criar um novo comentário
@comments_api.route('/comments', methods=['POST'])
def create_comment():
    data = request.get_json()
    texto = data['texto']
    autor = data['autor']
    content_id = data.get('content_id')
    insert_comment(texto, autor, content_id)  # Inserir o comentário no banco de dados
    return jsonify({'message': 'Comentário criado com sucesso'}), 201

# Rota para obter todos os comentários
@comments_api.route('/comments', methods=['GET'])
def get_comments_route():
    comentarios = get_comments_with_email()
    return jsonify(comentarios), 200  # Retornar os comentários em formato JSON
