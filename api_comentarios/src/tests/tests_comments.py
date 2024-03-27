import subprocess
import os

# Verifica se a variável de ambiente 'PIPELINE_ENV' está definida
pipeline_env = os.getenv('PIPELINE_ENV', None)

# Define o host com base na variável de ambiente 'PIPELINE_ENV'
if pipeline_env:
    app = 'app'
else:
    app = 'localhost'

def test_listagem_comentarios_por_id():
    content_id = 1
    while True:
        # Executa o comando curl para obter a lista de comentários por content_id
        curl_command = f"curl -s http://{app}:8000/api/comment/list/{content_id}"
        
        # Faz a chamada do curl e obtém a saída
        result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)

        # Verifica se houve erros ao executar o comando curl
        if result.returncode != 0:
            raise AssertionError(f"Erro ao executar o comando curl: {result.stderr}")

        # Imprime a saída do curl
        print(f"Comentários para o content_id {content_id}:")
        print(result.stdout)

        # Incrementa o content_id para o próximo teste
        content_id += 1

        # Verifica se chegou ao fim dos comentários
        if content_id > 10:  # Altere o número de "content_id" conforme o numero de matérias
            print("Todos os comentários foram listados com sucesso.")
            break
        