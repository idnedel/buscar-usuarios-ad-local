import json
import tkinter as tk
from tkinter import ttk, messagebox
import users
import pyperclip

# atualiza os dados do AD antes de abrir a interface
users.extrair_usuarios_ad()

# buscar usuários no JSON
def buscar_usuario(event=None):
    termo = entry_busca.get().strip().lower()

    if not termo:
        messagebox.showwarning("Atenção", "Digite um nome, telefone ou e-mail para buscar!")
        return

    try:
        with open("usuarios_ad.json", "r", encoding="utf-8") as file:
            usuarios = json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo usuarios_ad.json não encontrado!")
        return

    resultados = []

    for user in usuarios:
        # converter valores None para strings vazias antes da busca
        nome = str(user.get("Display Name", "")).lower()
        telefone = str(user.get("Telephone Number", "")).lower()
        email = str(user.get("E-mail", "")).lower()

        if termo in nome or termo in telefone or termo in email:
            resultados.append(user)

    # limpar resultados anteriores
    tree.delete(*tree.get_children())

    if resultados:
        for user in resultados:
            tree.insert("", "end", values=(
                user["Display Name"],
                user["Telephone Number"],
                user["E-mail"],
                user["OU"]
            ))
    else:
        messagebox.showinfo("Nenhum resultado", "Nenhum usuário encontrado para a busca.")

# função para copiar dados da linha selecionada para a área de transferência
def copiar_para_area_transferencia(event=None):
    selected_item = tree.selection()
    if selected_item:
        item_values = tree.item(selected_item, "values")
        dados = "\t".join(item_values)

        pyperclip.copy(dados)
        mostrar_notificacao("Dados copiados para a área de transferência!")

# mostrar a notificação
def mostrar_notificacao(mensagem):
    notification_label.config(text=mensagem)
    notification_label.pack(pady=5)

    root.after(3000, esconder_notificacao)

def esconder_notificacao():
    notification_label.pack_forget()

# janela principal
root = tk.Tk()
root.title("Buscar Colaborador")
root.geometry("600x400")
root.resizable(True, True)

notification_label = tk.Label(root, font=("Arial", 10), fg="blue", width=20, anchor="w")

tk.Label(root, text="Digite Nome, Ramal ou E-mail:", font=("Arial", 12)).pack(pady=5)
entry_busca = tk.Entry(root, width=50, font=("Arial", 12))
entry_busca.pack(pady=5)

entry_busca.bind("<Return>", buscar_usuario)

btn_buscar = tk.Button(root, text="Buscar", command=buscar_usuario, font=("Arial", 12), bg="blue", fg="white")
btn_buscar.pack(pady=10)

# tabela de resultados
colunas = ("Nome", "Ramal", "E-mail", "Setor")
tree = ttk.Treeview(root, columns=colunas, show="headings")

for coluna in colunas:
    tree.heading(coluna, text=coluna)
    tree.column(coluna, width=150)

tree.pack(expand=True, fill="both", padx=10, pady=10)

# configurar evento de tecla para copiar com Ctrl + C
root.bind("<Control-c>", copiar_para_area_transferencia)

# iniciar o programa
root.mainloop()