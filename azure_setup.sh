#!/bin/bash

# Carregar variáveis de ambiente do arquivo .env
source .env

# 1 - Criar Resource Group
az group create --name $RESOURCE_GROUP --location $LOCATION

# 2 - Criar Cosmos DB MongoDB
az cosmosdb create --name $COSMOS_DB_ACCOUNT --resource-group $RESOURCE_GROUP --kind MongoDB
az cosmosdb mongodb database create --account-name $COSMOS_DB_ACCOUNT --name $COSMOS_DB_NAME --resource-group $RESOURCE_GROUP

# 3 - Obter a Connection String do Cosmos DB e armazenar no Key Vault
CONNECTION_STRING=$(az cosmosdb keys list --type connection-strings --name $COSMOS_DB_ACCOUNT --resource-group $RESOURCE_GROUP --query connectionStrings[0].connectionString -o tsv)

# Criar o Key Vault
az keyvault create --name $KEY_VAULT_NAME --resource-group $RESOURCE_GROUP --location $LOCATION

# Armazenar a Connection String no Key Vault
az keyvault secret set --vault-name $KEY_VAULT_NAME --name "CosmosDBConnectionString" --value "$CONNECTION_STRING"

# 4 - Criar a Azure Function App
az functionapp create --resource-group $RESOURCE_GROUP --consumption-plan-location $LOCATION --runtime python --runtime-version 3.8 --functions-version 3 --name $FUNCTION_APP_NAME --storage-account $STORAGE_ACCOUNT_NAME

# Configurar o Azure Function para acessar o Key Vault
az functionapp config appsettings set --name $FUNCTION_APP_NAME --resource-group $RESOURCE_GROUP --settings "KEY_VAULT_URI=https://${KEY_VAULT_NAME}.vault.azure.net/"

# 5 - Fazer a Publicação
func azure functionapp publish $FUNCTION_APP_NAME