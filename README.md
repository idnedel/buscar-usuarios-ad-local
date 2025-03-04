## buscar-usuarios-ad-local
Programa de busca de usuários cadastrados no Active Directory via Nome, Telefone e E-mail

# Altere os parâmetros do `.env` conforme seu servidor de AD local;

AD_SERVER=ldap://192.168.0.0                  - seu ip do servidor
AD_USER=usuario.cadastrado @ seudominio         - user no AD com visibilidade
AD_PASSWORD=SuaSenha123                       - senha do user

# Ajuste também onde serão feitas as buscas da OUs:

BASE_DN = "OU=pastadeexemplo,DC=seudominio,DC=com,DC=br"  - ajustar a estrutura do seu AD conforme necessário

# Executar

Instale a dependência para atualizar o arquivo .exe com o comando `pip install pyinstaller` no diretório do programa

Depois execute o camando `pyinstaller --onefile --windowed --icon=meu_icone.ico buscar_usuarios.py` para gerar o .exe atualizado

Acesse a pasta `dist` no diretório do programa para executar o .exe e utilizar a aplicação
