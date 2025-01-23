import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from db import adicionar_tarefa_db, remover_tarefa_db, obter_detalhes_tarefa

def adicionar_tarefa(entry_nome, btn_data_entrega, entry_criador, entry_descricao, listbox):
    nome = entry_nome.get()
    data_criacao = datetime.now().strftime("%Y-%m-%d")
    data_entrega = btn_data_entrega.cget("text")  # Obtendo a data do texto do botão
    criador = entry_criador.get()
    descricao = entry_descricao.get("1.0", tk.END)  # Usando "1.0" e tk.END para o Text widget
    
    if nome:
        listbox.insert(tk.END, nome)
        adicionar_tarefa_db(nome, data_criacao, data_entrega, criador, descricao)
        entry_nome.delete(0, tk.END)
        btn_data_entrega.config(text="Selecionar Data")
        entry_criador.delete(0, tk.END)
        entry_descricao.delete("1.0", tk.END)  # Usando "1.0" e tk.END para limpar o Text widget
    else:
        messagebox.showwarning("Entrada Inválida", "Por favor, insira um nome válido para a tarefa.")

def remover_tarefa(listbox):
    try:
        selecionado = listbox.curselection()
        nome = listbox.get(selecionado)
        listbox.delete(selecionado)
        remover_tarefa_db(nome)
    except:
        messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione uma tarefa para remover.")

def abrir_detalhes_tarefa(nome):
    detalhes = obter_detalhes_tarefa(nome)
    if detalhes:
        janela_detalhes = tk.Toplevel()
        janela_detalhes.title("Detalhes da Tarefa")
        
        tk.Label(janela_detalhes, text="Nome:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        tk.Label(janela_detalhes, text=detalhes[1]).grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        tk.Label(janela_detalhes, text="Data de Criação:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        tk.Label(janela_detalhes, text=detalhes[2]).grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        
        tk.Label(janela_detalhes, text="Data de Entrega:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        tk.Label(janela_detalhes, text=detalhes[3]).grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)
        
        tk.Label(janela_detalhes, text="Criador:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        tk.Label(janela_detalhes, text=detalhes[4]).grid(row=3, column=1, sticky=tk.W, padx=10, pady=5)
        
        tk.Label(janela_detalhes, text="Descrição:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        descricao_text = tk.Text(janela_detalhes, height=10, width=40)
        descricao_text.grid(row=4, column=1, sticky=tk.W, padx=10, pady=5)
        descricao_text.insert(tk.END, detalhes[5])
        descricao_text.config(state=tk.DISABLED)