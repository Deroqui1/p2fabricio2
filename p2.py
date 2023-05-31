import tkinter as tk
import sqlite3


conn = sqlite3.connect("almoxarifado.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS itens (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, quantidade INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, senha TEXT)")


def cadastrar_item():
    nome = entry_nome.get()
    quantidade = int(entry_quantidade.get())

    cursor.execute("INSERT INTO itens (nome, quantidade) VALUES (?, ?)", (nome, quantidade))
    conn.commit()

    entry_nome.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)


def listar_itens():
    cursor.execute("SELECT * FROM itens")
    items = cursor.fetchall()

    texto_itens.delete("1.0", tk.END)  

    for item in items:
        texto_itens.insert(tk.END, f"ID: {item[0]}, Nome: {item[1]}, Quantidade: {item[2]}\n")


def cadastrar_usuario():
    nome = entry_nome_usuario.get()
    senha = entry_senha.get()

    cursor.execute("INSERT INTO usuarios (nome, senha) VALUES (?, ?)", (nome, senha))
    conn.commit()

    entry_nome_usuario.delete(0, tk.END)
    entry_senha.delete(0, tk.END)


def listar_usuarios():
    cursor.execute("SELECT id, nome FROM usuarios")
    usuarios = cursor.fetchall()

    texto_usuarios.delete("1.0", tk.END) 

    for usuario in usuarios:
        texto_usuarios.insert(tk.END, f"ID: {usuario[0]}, Nome: {usuario[1]}\n")


def logar_usuario():
    nome = entry_nome_usuario.get()
    senha = entry_senha.get()

    cursor.execute("SELECT * FROM usuarios WHERE nome=? AND senha=?", (nome, senha))
    usuario = cursor.fetchone()

    if usuario is not None:
        mensagem = f"Login bem-sucedido para o usuário: {usuario[1]}"
        if usuario[1] == "admin":
            button_alterar_senha.config(state=tk.NORMAL)
            button_apagar_usuario.config(state=tk.NORMAL)
        else:
            button_alterar_senha.config(state=tk.DISABLED)
            button_apagar_usuario.config(state=tk.DISABLED)
    else:
        mensagem = "Usuário ou senha inválidos"
        button_alterar_senha.config(state=tk.DISABLED)
        button_apagar_usuario.config(state=tk.DISABLED)

    label_mensagem.config(text=mensagem)

    entry_nome_usuario.delete(0, tk.END)
    entry_senha.delete(0, tk.END)

def alterar_senha():
    nome = entry_nome_usuario.get()
    senha_antiga = entry_senha.get()
    nova_senha = entry_nova_senha.get()

    cursor.execute("UPDATE usuarios SET senha=? WHERE nome=? AND senha=?", (nova_senha, nome, senha_antiga))
    conn.commit()

    entry_nome_usuario.delete(0, tk.END)
    entry_senha.delete(0, tk.END)
    entry_nova_senha.delete(0, tk.END)

    label_mensagem.config(text="Senha alterada com sucesso")

def apagar_usuario():
    nome = entry_nome_usuario.get()

    cursor.execute("DELETE FROM usuarios WHERE nome=?", (nome,))
    conn.commit()

    entry_nome_usuario.delete(0, tk.END)
    entry_senha.delete(0, tk.END)

    label_mensagem.config(text="Usuário apagado com sucesso")


window = tk.Tk()
window.title("Almoxarifado")


label_nome = tk.Label(window, text="Nome:")
label_nome.pack()
entry_nome = tk.Entry(window)
entry_nome.pack()

label_quantidade = tk.Label(window, text="Quantidade:")
label_quantidade.pack()
entry_quantidade = tk.Entry(window)
entry_quantidade.pack()

button_cadastrar_item = tk.Button(window, text="Cadastrar Item", command=cadastrar_item)
button_cadastrar_item.pack()

button_listar_itens = tk.Button(window, text="Listar Itens", command=listar_itens)
button_listar_itens.pack()

label_nome_usuario = tk.Label(window, text="Nome:")
label_nome_usuario.pack()
entry_nome_usuario = tk.Entry(window)
entry_nome_usuario.pack()

label_senha = tk.Label(window, text="Senha:")
label_senha.pack()
entry_senha = tk.Entry(window, show="*")
entry_senha.pack()

button_cadastrar_usuario = tk.Button(window, text="Cadastrar Usuário", command=cadastrar_usuario)
button_cadastrar_usuario.pack()

button_listar_usuarios = tk.Button(window, text="Listar Usuários", command=listar_usuarios)
button_listar_usuarios.pack()

button_logar_usuario = tk.Button(window, text="Logar Usuário", command=logar_usuario)
button_logar_usuario.pack()

label_mensagem = tk.Label(window, text="")
label_mensagem.pack()

button_alterar_senha = tk.Button(window, text="Alterar Senha", command=alterar_senha, state=tk.DISABLED)
button_alterar_senha.pack()

button_apagar_usuario = tk.Button(window, text="Apagar Usuário", command=apagar_usuario, state=tk.DISABLED)
button_apagar_usuario.pack()

label_nova_senha = tk.Label(window, text="Nova Senha:")
label_nova_senha.pack()
entry_nova_senha = tk.Entry(window, show="*")
entry_nova_senha.pack()

label_usuarios = tk.Label(window, text="Usuários:")
label_usuarios.pack()
texto_usuarios = tk.Text(window, width=50, height=10)
texto_usuarios.pack()

label_itens = tk.Label(window, text="Itens:")
label_itens.pack()
texto_itens = tk.Text(window, width=50, height=10)
texto_itens.pack()


def fechar_janela():
    conn.close()
    window.destroy()

window.protocol("WM_DELETE_WINDOW", fechar_janela)

window.mainloop()
