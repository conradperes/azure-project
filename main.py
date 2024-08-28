import os
import logging
import json
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.cosmos import CosmosClient
import azure.functions as func
import subprocess

def decrypt_connection_string(file_path, passphrase=None):
    try:
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
        print(f"Erro ao desencriptar o arquivo: {e}")
        return None

# Exemplo de uso



app = func.FunctionApp()

@app.route(route="Myfunction", auth_level=func.AuthLevel.Anonymous)
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    file_path = 'connection_string.enc'
    connection_string = decrypt_connection_string(file_path)

    if connection_string:
        print(f"A conexão desencriptada é: {connection_string}")
    else:
        print("Falha ao desencriptar a conexão.")
    # Configurar o acesso ao Key Vault
    #key_vault_uri = os.environ["KEY_VAULT_URI"]
    #credential = DefaultAzureCredential()
    #client = SecretClient(vault_url=key_vault_uri, credential=credential)
    #connection_string = client.get_secret("CosmosDBConnectionString").value

    # Configurar o acesso ao Cosmos DB
    cosmos_client = CosmosClient.from_connection_string(connection_string)
    database_name = os.environ["COSMOS_DB_NAME"]
    database = cosmos_client.get_database_client(database_name)
    container = database.get_container_client('items')

    # Criar um item JSON e salvá-lo no Cosmos DB
    item = req.get_json()
    container.create_item(body=item)

    return func.HttpResponse(
        "JSON salvo com sucesso no Cosmos DB!",
        status_code=200
    )