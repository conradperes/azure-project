import os
import logging
import json
from pymongo import MongoClient
import azure.functions as func
import subprocess
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Função para desencriptar a string de conexão
def decrypt_connection_string(file_path):
    try:
        # Recuperar a senha da variável de ambiente
        passphrase = os.getenv('PASSWORD_CONNECTION_STRING')
        logging.info(f"senha={passphrase}")
        # Construir o comando openssl
        command = ['openssl', 'enc', '-aes-256-cbc', '-d', '-a', '-in', file_path]
        
        # Se uma senha foi utilizada para encriptação, passe-a como input para o comando
        if passphrase:
            command.extend(['-pass', f'pass:{passphrase}'])
        
        # Executar o comando e capturar a saída
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # A saída conterá a string desencriptada
        connection_string = result.stdout.strip()
        return connection_string
    
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao desencriptar o arquivo: {e}")
        return None

app = func.FunctionApp()

@app.route(route="decrypt-and-save-json", auth_level=func.AuthLevel.ANONYMOUS)
def decrypt_and_save_json(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Desencriptar a string de conexão
    file_path = 'connection_string.enc'
    connection_string = decrypt_connection_string(file_path)
    logging.info(f"connection_string={connection_string}")
    if not connection_string:
        return func.HttpResponse("Falha ao desencriptar a conexão.", status_code=500)
    
    # Conectar ao MongoDB do Cosmos DB usando pymongo
    client = MongoClient(connection_string)
    database_name = os.environ["COSMOS_DB_NAME"]
    database = client[database_name]
    collection = database['items']

    # Criar um item JSON e salvá-lo na coleção
    item = req.get_json()
    collection.insert_one(item)
    logging.info("JSON salvo com sucesso no Cosmos DB!")

    return func.HttpResponse("JSON salvo com sucesso no Cosmos DB!", status_code=200)

# Outras funções de rota...