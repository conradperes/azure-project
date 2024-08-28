import os
import logging
import json
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.cosmos import CosmosClient
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Configurar o acesso ao Key Vault
    key_vault_uri = os.environ["KEY_VAULT_URI"]
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_uri, credential=credential)
    connection_string = client.get_secret("CosmosDBConnectionString").value

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