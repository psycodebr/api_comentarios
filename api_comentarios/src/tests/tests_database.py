import os
import requests

# Verifica se a variável de ambiente 'PIPELINE_ENV' está definida
pipeline_env = os.getenv('PIPELINE_ENV', None)

# Define o host com base na variável de ambiente 'PIPELINE_ENV'
if pipeline_env:
    app = 'app'
else:
    app = 'localhost'

def test_sql_injection():
    id = 1

    # Itera consecutivamente pelos IDs de conteúdo até que não haja mais conteúdo disponível
    while True:
        # Define a URL de destino para o teste de injeção de SQL
        if app == 'app':
            url = f"http://app:8000/api/comment/list/{id}"
        else:
            url = f"http://localhost:8000/api/comment/list/{id}"

        # Tentativa de injeção de SQL através do parâmetro de consulta
        malicious_input = "' OR 1=1 --"

        # Define os parâmetros da solicitação
        params = {'search': malicious_input}

        # Faz a solicitação GET para obter os comentários com a entrada maliciosa
        response = requests.get(url, params=params)

        # Verifica se a resposta retorna um status de erro ou sucesso
        if response.status_code != 200:
            raise AssertionError(f"Falha na solicitação para o ID {id}: {response.text}")

        # Verifica se a resposta indica uma possível vulnerabilidade de injeção de SQL
        if "Possible SQL injection vulnerability detected" in response.text:
            raise AssertionError(f"Possível vulnerabilidade de injeção de SQL detectada para o ID {id}")

        # Incrementa o ID de conteúdo para o próximo número
        id += 1

        if not response.json():
            print("Não há mais conteúdo disponível. Teste concluído.")
            break
