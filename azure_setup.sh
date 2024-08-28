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
#az keyvault create --name $KEY_VAULT_NAME --resource-group $RESOURCE_GROUP --location $LOCATION

# Obter o ID da assinatura
#subscription_id=$(az account show --query id --output tsv)

# Obter o ID do usuário atual (ou identidade gerenciada)
#assignee_id=$(az ad signed-in-user show --query objectId --output tsv)

# Criar a atribuição de função
#az role assignment create \
#  --role "Key Vault Secrets Officer" \
#  --assignee $assignee_id \
#  --scope /subscriptions/$subscription_id/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.KeyVault/vaults/$KEY_VAULT_NAME

# Armazenar a Connection String no Key Vault
#az keyvault secret set --vault-name $KEY_VAULT_NAME --name "CosmosDBConnectionString" --value "$CONNECTION_STRING"

# 4 - Criar a Storage Account
az storage account create \
    --name $STORAGE_ACCOUNT_NAME \
    --location $LOCATION \
    --resource-group $RESOURCE_GROUP \
    --sku Standard_LRS \
    --kind StorageV2

# Configurar ambiente Python
deactivate
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5 - Criar a Azure Function App
az functionapp create \
    --resource-group $RESOURCE_GROUP \
    --consumption-plan-location $LOCATION \
    --runtime python \
    --runtime-version 3.8 \
    --functions-version 4 \
    --name $FUNCTION_APP_NAME \
    --storage-account $STORAGE_ACCOUNT_NAME \
    --os-type Linux

# 6 - Criar uma nova função HTTP Trigger
func new --name Myfunction --template "HTTP trigger" --authlevel "anonymous"

# Verificar se a função foi criada
az functionapp show --name $FUNCTION_APP_NAME --resource-group $RESOURCE_GROUP

# Configurar o Azure Function para acessar o Key Vault
#az functionapp config appsettings set --name $FUNCTION_APP_NAME --resource-group $RESOURCE_GROUP --settings "APPINSIGHTS_INSTRUMENTATIONKEY=your-instrumentation-keyfj

echo "mongodb://conradbbacccount2:iztUU2HQtpxm4WJjlK16lgexPyfY3eQTKoKRXPK9reamk2eeoXga12uLCK6HhNAaZ9O522jk9274ACDb9AIwPg%3D%3D@conradbbacccount2.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@conradbbacccount2@" > connection_string.txt

openssl enc -aes-256-cbc -salt -in connection_string.txt -out connection_string.enc -a

rm connection_string.txt


# 7 - Fazer a Publicação
func azure functionapp publish $FUNCTION_APP_NAME