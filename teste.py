import os
import subprocess
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Função para desencriptar a string de conexão
def decrypt_connection_string(file_path):
    try:
        # Recuperar a senha da variável de ambiente
        passphrase = os.getenv('PASSWORD_CONNECTION_STRING')
        
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
file_path = 'connection_string.enc'
connection_string = decrypt_connection_string(file_path)

if connection_string:
    print(f"A conexão desencriptada é: {connection_string}")
else:
    print("Falha ao desencriptar a conexão.")