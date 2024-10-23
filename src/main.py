"""
Projeto AV para a disciplina de Desenvolvimento Rápido de Aplicações em Python, na Faculdade Estácio de Sá do Recife
referente ao período 2024.02 do curso de Análise e Desenvolvimento de Sistemas.
"""

import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# Implementando banco de dados SQLite.
conn = sqlite3.connect("alunos.db")
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    av1 REAL NOT NULL,
    av2 REAL NOT NULL,
    media REAL NOT NULL,
    situacao TEXT NOT NULL
    )
''')
conn.commit()


def calcular_media(av1, av2):  # Calcula a Média e define a situação do aluno.
    media = (av1 + av2) / 2
    situacao = "Aprovado" if media >= 6 else "Reprovado"
    return media, situacao


def cadastro_aluno():   # Cadastra as informações do aluno no banco de dados sqlite.
    nome = entry_nome.get()
    try:
        av1 = float(entry_av1.get())
        av2 = float(entry_av2.get())
    except ValueError:
        messagebox.showerror("Erro", "As notas devem ser numéricas.")
        return

    if not nome or not nome.isalpha():
        messagebox.showerror("Erro", "O nome deve ser registrado somente com letras.")
        return
    elif av1 < 0 or av1 > 10 or av2 < 0 or av2 > 10:
        messagebox.showerror("Erro", "As notas devem ser entre 0 e 10.")
        return

    media, situacao = calcular_media(av1, av2)

    cursor.execute('INSERT INTO alunos (nome, av1, av2, media, situacao) VALUES (?, ?, ?, ?, ?)',
                   (nome, av1, av2, media, situacao))
    conn.commit()

    messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso.")
    att_alunos()
    limpar()


def excluir_aluno():  # Exclui as informações de algum aluno.
    try:
        selected_item = treeview.selection()[0]
    except IndexError:
        messagebox.showerror("Erro", "Selecione um aluno para excluir.")
        return

    aluno_id = treeview.item(selected_item)['values'][0]

    cursor.execute('DELETE FROM alunos WHERE id = ?', (aluno_id,))
    conn.commit()

    messagebox.showinfo("Sucesso", "Aluno excluído com sucesso.")
    att_alunos()


def limpar():  # Limpa os campos do formulário após entrada dos dados.
    entry_nome.delete(0, tk.END)
    entry_av1.delete(0, tk.END)
    entry_av2.delete(0, tk.END)


def att_alunos():  # Atualiza a lista de alunos.
    for linha in treeview.get_children():
        treeview.delete(linha)

    cursor.execute('SELECT id, nome, av1, av2, media, situacao FROM alunos')
    for linha in cursor.fetchall():
        treeview.insert('', tk.END, values=linha)


# Interface gráfica utilizando Tkinter.
app = tk.Tk()
app.title("Sistema de Cadastro e Consulta de Notas de Alunos")
app.configure(bg="#f0f0f0")

# Labels e entradas para cadastro.
frame_form = tk.Frame(app, bg="#f0f0f0")
frame_form.pack(padx=10, pady=10)

tk.Label(frame_form, text="Nome do Aluno:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
entry_nome = tk.Entry(frame_form, width=25)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Nota AV1:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
entry_av1 = tk.Entry(frame_form, width=25)
entry_av1.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Nota AV2:", bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5)
entry_av2 = tk.Entry(frame_form, width=25)
entry_av2.grid(row=2, column=1, padx=5, pady=5)

# Botões para cadastrar e excluir aluno.
btn_cadastrar = tk.Button(frame_form, text="Cadastrar", command=cadastro_aluno, bg="#4CAF50", fg="white")
btn_cadastrar.grid(row=3, column=1, padx=5, pady=5)

btn_excluir = tk.Button(frame_form, text="Excluir", command=excluir_aluno, bg="#f44336", fg="white")
btn_excluir.grid(row=3, column=2, padx=5, pady=5)

# Lista de alunos cadastrados.
frame_lista = tk.Frame(app, bg="#f0f0f0")
frame_lista.pack(padx=10, pady=10)

treeview = ttk.Treeview(frame_lista, columns=("ID", "Nome", "AV1", "AV2", "Média", "Situação"), show="headings")
treeview.heading("ID", text="ID")
treeview.heading("Nome", text="Nome")
treeview.heading("AV1", text="AV1")
treeview.heading("AV2", text="AV2")
treeview.heading("Média", text="Média")
treeview.heading("Situação", text="Situação")

treeview.pack()  # Exibe os dados.

att_alunos()  # Atualiza a lista de alunos ao iniciar o programa.

app.mainloop()  # Executa a interface gráfica.

conn.close()  # Fecha a conexão com o banco de dados ao sair.
