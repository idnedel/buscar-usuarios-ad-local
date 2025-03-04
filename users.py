import json
from dotenv import load_dotenv
import os
from ldap3 import Server, Connection, ALL, SUBTREE

load_dotenv()

def extrair_usuarios_ad():
    # configurações de conexão com o AD
    AD_SERVER = os.getenv("AD_SERVER")
    AD_USER = os.getenv("AD_USER")
    AD_PASSWORD = os.getenv("AD_PASSWORD")
    BASE_DN = "OU=Grupo Coopershoes,DC=coopershoes,DC=com,DC=br"  # ajustar a estrutura do seu AD conforme necessário

    server = Server(AD_SERVER, get_info=ALL)
    conn = Connection(server, user=AD_USER, password=AD_PASSWORD, auto_bind=True)

    # filtro para buscar usuários
    search_filter = "(objectClass=user)"
    search_attributes = ["displayName", "telephoneNumber", "mail", "distinguishedName", "sAMAccountName"]
    conn.search(search_base=BASE_DN, search_filter=search_filter, search_scope=SUBTREE, attributes=search_attributes)

    usuarios = []
    for entry in conn.entries:
        print(f"DistinguishedName: {entry.distinguishedName.value}")

        user_info = {
            "Display Name": entry.displayName.value if entry.displayName else "N/A",
            "Telephone Number": entry.telephoneNumber.value if entry.telephoneNumber else "N/A",
            "E-mail": entry.mail.value if entry.mail else "N/A",
            "OU": "N/A",
            "sAMAccountName": entry.sAMAccountName.value if entry.sAMAccountName else "N/A"
        }

        # extrair a OU (pasta onde o usuário está cadastrado)
        dn_parts = entry.distinguishedName.value.split(",")
        ou_parts = [part.replace("OU=", "").strip() for part in dn_parts if part.strip().startswith("OU=")]

        if ou_parts:
            user_info["OU"] = ou_parts[0]  # usa a primeira OU se houver várias
        else:
            user_info["OU"] = "N/A"

        # ignorar usuários da OU "Usuarios Bloqueados"
        # remover caso não houver uma OU com este nome
        if user_info["OU"].strip().lower() == "usuarios bloqueados":
            continue

        usuarios.append(user_info)

    # fechar a conexão
    conn.unbind()

    # salvar os resultados em um arquivo JSON
    with open("usuarios_ad.json", "w", encoding="utf-8") as json_file:
        json.dump(usuarios, json_file, indent=4, ensure_ascii=False)

    print("Arquivo 'usuarios_ad.json' atualizado com sucesso!")

if __name__ == "__main__":
    extrair_usuarios_ad()
