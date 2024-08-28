# Azure Python Project

Este projeto automatiza a criação de recursos no Azure, como o Cosmos DB, Key Vault e Azure Function, utilizando a Azure CLI.

## Configuração

1. Clone este repositório:
    ```bash
    git clone <URL do repositório>
    cd azure-project



Explicação do Projeto

Este projeto é uma aplicação baseada em Azure que demonstra a integração entre diferentes serviços do Azure: Azure Cosmos DB (com API MongoDB), Azure Key Vault e Azure Functions. O objetivo do projeto é criar uma aplicação serverless que possa armazenar e recuperar dados JSON simples em um banco de dados Cosmos DB, utilizando Azure Functions para lógica de aplicação e Azure Key Vault para gerenciar segredos, como a string de conexão do Cosmos DB.

Diagrama de Arquitetura

Abaixo está o diagrama de arquitetura que ilustra como os diferentes componentes do Azure interagem entre si:


	+-------------------+       +-----------------+
	|                   |       |                 |
	|  Azure Key Vault  |       | Azure Cosmos DB |
	|                   |<----->|   MongoDB API   |
	+-------------------+       +-----------------+
	        ^
	        |
	        v
	+-------------------+       +-----------------------+
	|                   |       |                       |
	|  Azure Function   |<----->| Azure Storage Account |
	|                   |       |                       |
	+-------------------+       +-----------------------+
	        ^
	        |
	        v
	  HTTP Request
	(Insomnia/Postman)


Configuração do Projeto

1. Pré-requisitos

	•	Azure CLI instalado e configurado.
	•	Python 3.8+ instalado.
	•	Visual Studio Code ou qualquer outro editor de texto.
	•	Conta no Azure.

2. Configuração das Variáveis de Ambiente

Crie um arquivo .env na raiz do projeto e adicione as seguintes variáveis:

	RESOURCE_GROUP="myResourceGroup"
	LOCATION="brazilsouth"
	COSMOS_DB_ACCOUNT="conradcosmosdbaccount"
	COSMOS_DB_NAME="mycosmosdb"
	KEY_VAULT_NAME="conradkeyvault123"
	FUNCTION_APP_NAME="myfunctionapp"
	STORAGE_ACCOUNT_NAME="mystorageaccount"


3. Executar o Script de Configuração

Execute o script azure_setup.sh para criar todos os recursos necessários no Azure:


	bash azure_setup.sh


4. Publicação da Azure Function

Após configurar o ambiente e os recursos, publique a Azure Function:

	func azure functionapp publish $FUNCTION_APP_NAME




Testando a Aplicação

1. Utilizando o Insomnia/Postman

Você pode testar a aplicação enviando uma requisição HTTP POST para a Azure Function. Abaixo está um exemplo de como configurar o Insomnia/Postman:

	•	URL: https://<FUNCTION_APP_NAME>.azurewebsites.net/api/<FUNCTION_ENDPOINT>
	•	Método: POST
	•	Body: JSON


        {
            "name": "John Doe",
            "email": "johndoe@example.com",
            "age": 30
        }

2. Resultado Esperado

A Azure Function processará a requisição, salvará os dados JSON no Cosmos DB, e retornará uma mensagem de sucesso.

"JSON salvo com sucesso no Cosmos DB!"

Estrutura do Projeto

	azure-project/
	│
	├── main.py              # Código da Azure Function
	├── README.md            # Documentação do projeto
	├── .env                 # Variáveis de ambiente
	└── azure_setup.sh       # Script para configuração no Azure



Considerações Finais

Este projeto serve como exemplo básico de como utilizar e integrar diferentes serviços do Azure para criar uma aplicação serverless. Ele pode ser expandido e adaptado para diferentes cenários conforme a necessidade.




