import tkinter as tk
from tkinter import font as tkFont
from tkcalendar import Calendar
from tkinter import ttk
import sqlite3

# Funções de banco de dados
def init_db():
    conn = sqlite3.connect('tarefas.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tarefas
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nome TEXT NOT NULL,
                  data_entrega TEXT,
                  criador TEXT,
                  descricao TEXT)''')
    conn.commit()
    conn.close()

def obter_tarefas_db():
    conn = sqlite3.connect('tarefas.db')
    c = conn.cursor()
    c.execute("SELECT nome FROM tarefas")
    tarefas = c.fetchall()
    conn.close()
    return [tarefa[0] for tarefa in tarefas]

def adicionar_tarefa_db(nome, data_entrega, criador, descricao):
    conn = sqlite3.connect('tarefas.db')
    c = conn.cursor()
    c.execute("INSERT INTO tarefas (nome, data_entrega, criador, descricao) VALUES (?, ?, ?, ?)",
              (nome, data_entrega, criador, descricao))
    conn.commit()
    conn.close()

def remover_tarefa_db(nome):
    conn = sqlite3.connect('tarefas.db')
    c = conn.cursor()
    c.execute("DELETE FROM tarefas WHERE nome = ?", (nome,))
    conn.commit()
    conn.close()

# Função para carregar tarefas do banco de dados
def carregar_tarefas():
    tarefas = obter_tarefas_db()
    for tarefa in tarefas:
        adicionar_item_canvas(tarefa)

# Função para abrir o calendário e obter a data selecionada
def selecionar_data(btn_data_entrega):
    def obter_data():
        selected_date = cal.selection_get().strftime('%d/%m/%Y')
        btn_data_entrega.config(text=selected_date)
        top.destroy()
    
    top = tk.Toplevel(root)
    cal = Calendar(top, selectmode='day', date_pattern='dd/mm/yyyy')
    cal.pack(pady=20)
    tk.Button(top, text="Selecionar", command=obter_data).pack()

# Função para fechar a janela
def fechar_janela():
    root.destroy()

# Função para minimizar a janela
def minimizar_janela():
    root.iconify()

# Função para abrir uma nova janela para adicionar tarefas
def abrir_janela_adicionar_tarefa():
    nova_janela = tk.Toplevel(root)
    nova_janela.title("Adicionar Tarefa")
    nova_janela.geometry("400x400")
    nova_janela.configure(bg='#1E1E1E')

    # Frame centralizado na nova janela
    central_frame = ttk.Frame(nova_janela)
    central_frame.place(relx=0.5, rely=0.5, anchor='center')

    # Campos de entrada para nova tarefa
    ttk.Label(central_frame, text="Nome:", background="#1E1E1E", foreground="white").grid(row=0, column=0, padx=5, pady=5)
    entry_nome = ttk.Entry(central_frame, width=30)
    entry_nome.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(central_frame, text="Data de Entrega:", background="#1E1E1E", foreground="white").grid(row=1, column=0, padx=5, pady=5)
    btn_data_entrega = tk.Button(central_frame, text="Selecionar Data", font=button_font, bg="#4D4D4D", fg="white", command=lambda: selecionar_data(btn_data_entrega))
    btn_data_entrega.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(central_frame, text="Criador:", background="#1E1E1E", foreground="white").grid(row=2, column=0, padx=5, pady=5)
    entry_criador = ttk.Entry(central_frame, width=30)
    entry_criador.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(central_frame, text="Descrição:", background="#1E1E1E", foreground="white").grid(row=3, column=0, padx=5, pady=5)
    entry_descricao = tk.Text(central_frame, width=30, height=5, bg="#4D4D4D", fg="white", font=default_font)
    entry_descricao.grid(row=3, column=1, padx=5, pady=5)

    # Botão para adicionar tarefa
    add_button = tk.Button(central_frame, text="Adicionar Tarefa", font=button_font, bg="#4D4D4D", fg="white", command=lambda: [adicionar_tarefa(entry_nome, btn_data_entrega, entry_criador, entry_descricao), adicionar_item_canvas(entry_nome.get())])
    add_button.grid(row=4, columnspan=2, pady=10)

# Função para adicionar tarefa ao banco de dados e ao Canvas
def adicionar_tarefa(entry_nome, btn_data_entrega, entry_criador, entry_descricao):
    nome = entry_nome.get()
    data_entrega = btn_data_entrega.cget("text")
    criador = entry_criador.get()
    descricao = entry_descricao.get("1.0", tk.END)
    adicionar_tarefa_db(nome, data_entrega, criador, descricao)

# Função para abrir os detalhes da tarefa
def abrir_detalhes_tarefa(tarefa):
    detalhes_janela = tk.Toplevel(root)
    detalhes_janela.title("Detalhes da Tarefa")
    detalhes_janela.geometry("400x400")
    detalhes_janela.configure(bg='#1E1E1E')

    conn = sqlite3.connect('tarefas.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tarefas WHERE nome = ?", (tarefa,))
    tarefa_detalhes = c.fetchone()
    conn.close()

    if tarefa_detalhes:
        # Desempacotar todos os valores retornados pela consulta
        id_tarefa, nome, data_entrega, criador, descricao = tarefa_detalhes

        ttk.Label(detalhes_janela, text="Nome:", background="#1E1E1E", foreground="white").grid(row=0, column=0, padx=5, pady=5)
        nome_entry = ttk.Entry(detalhes_janela, width=30)
        nome_entry.grid(row=0, column=1, padx=5, pady=5)
        nome_entry.insert(0, nome)
        nome_entry.config(state='readonly')

        ttk.Label(detalhes_janela, text="Data de Entrega:", background="#1E1E1E", foreground="white").grid(row=1, column=0, padx=5, pady=5)
        data_entrega_entry = ttk.Entry(detalhes_janela, width=30)
        data_entrega_entry.grid(row=1, column=1, padx=5, pady=5)
        data_entrega_entry.insert(0, data_entrega)
        data_entrega_entry.config(state='readonly')

        ttk.Label(detalhes_janela, text="Criador:", background="#1E1E1E", foreground="white").grid(row=2, column=0, padx=5, pady=5)
        criador_entry = ttk.Entry(detalhes_janela, width=30)
        criador_entry.grid(row=2, column=1, padx=5, pady=5)
        criador_entry.insert(0, criador)
        criador_entry.config(state='readonly')

        ttk.Label(detalhes_janela, text="Descrição:", background="#1E1E1E", foreground="white").grid(row=3, column=0, padx=5, pady=5)
        descricao_text = tk.Text(detalhes_janela, width=30, height=5, bg="#4D4D4D", fg="white", font=default_font)
        descricao_text.grid(row=3, column=1, padx=5, pady=5)
        descricao_text.insert("1.0", descricao)
        descricao_text.config(state='disabled')

# Função para adicionar item ao Canvas
def adicionar_item_canvas(tarefa):
    y = len(listbox_items) * 50 + 2  # Espaçamento entre itens (30 para item + 10 para linha + 10 para espaçamento) + 2 para o topo
    text_id = listbox_canvas.create_text(10, y, anchor='nw', text=tarefa, fill="white", font=default_font)
    details_button_id = listbox_canvas.create_window(410, y, anchor='nw', window=tk.Button(root, text="ℹ️", font=button_font, bg="#4D4D4D", fg="white", command=lambda t=tarefa: abrir_detalhes_tarefa(t)))
    delete_button_id = listbox_canvas.create_window(460, y, anchor='nw', window=tk.Button(root, text="❌", font=button_font, bg="#FF4D4D", fg="white", command=lambda t=tarefa: remover_item_canvas(t, text_id, details_button_id, delete_button_id, line_id)))
    line_id = listbox_canvas.create_line(0, y + 30, 500, y + 30, fill="#2e2e2e")  # Linha de divisão
    listbox_items.append((text_id, details_button_id, delete_button_id, line_id))

# Função para remover item do Canvas
def remover_item_canvas(tarefa, text_id, details_button_id, delete_button_id, line_id):
    listbox_canvas.delete(text_id)
    listbox_canvas.delete(details_button_id)
    listbox_canvas.delete(delete_button_id)
    listbox_canvas.delete(line_id)
    listbox_items.remove((text_id, details_button_id, delete_button_id, line_id))
    remover_tarefa_db(tarefa)  # Função para remover do banco de dados

# Criação da janela principal
root = tk.Tk()
root.title("Gerenciador de Tarefas")
root.geometry("500x500")
root.overrideredirect(True)  # Ocultar a barra de título padrão

# Definir a cor de fundo da janela principal para um tom mais escuro
root.configure(bg='#1E1E1E')

# Inicialização do banco de dados
init_db()

# Definir uma fonte padrão estilosa
default_font = tkFont.Font(family="Helvetica", size=12)
button_font = tkFont.Font(family="Helvetica", size=12, weight="bold")

# Definir um tema escuro
style = ttk.Style(root)
style.theme_use('clam')
style.configure("TFrame", background="#2E2E2E")
style.configure("TLabel", background="#2E2E2E", foreground="white", font=default_font)
style.configure("TButton", background="#4D4D4D", foreground="white", font=button_font)
style.configure("TEntry", fieldbackground="#4D4D4D", background="#4D4D4D", foreground="white")
style.configure("TText", fieldbackground="#4D4D4D", background="#4D4D4D", foreground="white")
style.configure("TListbox", background="#4D4D4D", foreground="white", font=default_font)
style.configure("TScrollbar", background="#4D4D4D", foreground="white")

# Criar uma barra de título personalizada
title_bar = tk.Frame(root, bg="black", relief="raised", bd=0)
title_bar.place(relx=0, rely=0, relwidth=1, height=30)

# Adicionar título na barra de título personalizada
title_label = tk.Label(title_bar, text="Gerenciador de Tarefas", bg="black", fg="white", font=button_font)
title_label.pack(side="left", padx=10)

# Adicionar botões de minimizar e fechar na barra de título personalizada
close_button = tk.Button(title_bar, text="X", command=fechar_janela, bg="black", fg="white", bd=0, font=button_font)
close_button.pack(side="right", padx=5)
minimize_button = tk.Button(title_bar, text="_", command=minimizar_janela, bg="black", fg="white", bd=0, font=button_font)
minimize_button.pack(side="right")

# Permitir que a barra de título personalizada seja arrastável
def start_move(event):
    root.x = event.x
    root.y = event.y

def stop_move(event):
    root.x = None
    root.y = None

def on_motion(event):
    delta_x = event.x - root.x
    delta_y = event.y - root.y
    new_x = root.winfo_x() + delta_x
    new_y = root.winfo_y() + delta_y
    root.geometry(f"+{new_x}+{new_y}")

title_bar.bind("<Button-1>", start_move)
title_bar.bind("<ButtonRelease-1>", stop_move)
title_bar.bind("<B1-Motion>", on_motion)

# Canvas para desenhar itens
listbox_canvas = tk.Canvas(root, bg="#1E1E1E", highlightthickness=0)
listbox_canvas.place(relx=0, rely=0.1, relwidth=1, relheight=0.8)

# Botão para abrir a janela de adicionar tarefas
add_task_button = tk.Button(root, text="Adicionar Tarefas", font=button_font, bg="#4D4D4D", fg="white", command=abrir_janela_adicionar_tarefa)
add_task_button.place(relx=0.5, rely=0.92, anchor='center')

# Lista para armazenar IDs dos itens
listbox_items = []

# Carregar tarefas do banco de dados
carregar_tarefas()

# Iniciar o loop principal da aplicação
root.mainloop()