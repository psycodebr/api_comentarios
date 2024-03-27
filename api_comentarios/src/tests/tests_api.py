import subprocess
import json
import os

# Verifica se a variável de ambiente 'PIPELINE_ENV' está definida
pipeline_env = os.getenv('PIPELINE_ENV', None)

# Define o host com base na variável de ambiente 'PIPELINE_ENV'
if pipeline_env:
    app = 'app'
else:
    app = 'localhost'

def test_create_comment():
    # Dados de exemplo para o teste
    data = [
        {"email": "alice@example.com", "comment": "first post!", "content_id": 1},
        {"email": "alice@example.com", "comment": "ok, now I am gonna say something more useful", "content_id": 1},
        {"email": "bob@example.com", "comment": "I agree", "content_id": 1},
        {"email": "bob@example.com", "comment": "I guess this is a good thing", "content_id": 2},
        {"email": "charlie@example.com", "comment": "Indeed, dear Bob, I believe so as well", "content_id": 2},
        {"email": "eve@example.com", "comment": "Nah, you both are wrong", "content_id": 2}
    ]

    # Realiza uma solicitação POST para criar um novo comentário para cada conjunto de dados
    for comment_data in data:
        # Monta o comando curl para enviar a solicitação POST
        curl_command = [
            'curl',
            '-X', 'POST',
            '-H', 'Content-Type: application/json',
            '-d', json.dumps(comment_data),
            f'http://{app}:8000/api/comment/new'
        ]

        # Executa o comando curl
        result = subprocess.run(curl_command, capture_output=True, text=True)

        # Verifica se a execução do comando foi bem-sucedida
        assert result.returncode == 0, f"Erro ao executar o comando curl: {result.stderr}"

        # Converte a saída do comando para um dicionário
        response_data = json.loads(result.stdout)

        # Verifica se a resposta está correta
        assert 'mensagem' in response_data, "Chave 'mensagem' não encontrada na resposta"
        assert response_data['mensagem'] == 'Comentário criado com sucesso', f"Mensagem de retorno inesperada: {response_data['mensagem']}"
