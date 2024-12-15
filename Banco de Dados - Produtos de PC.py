import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Criação do banco de dados e tabela
def init_db():
    conn = sqlite3.connect('produtos_computador.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT,
            fabricante TEXT,
            velocidade REAL,
            nucleos INTEGER,
            ram INTEGER,
            fabricante_processador TEXT,
            ssd INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Função para salvar o produto no banco de dados
def save_product():
    codigo = entry_codigo.get()
    fabricante = combo_fabricante.get()
    velocidade = entry_velocidade.get()
    nucleos = combo_nucleos.get()
    ram = combo_ram.get()
    fabricante_processador = combo_fabricante_processador.get()
    ssd = combo_ssd.get()

    conn = sqlite3.connect('produtos_computador.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO produtos (codigo, fabricante, velocidade, nucleos, ram, fabricante_processador, ssd)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (codigo, fabricante, velocidade, nucleos, ram, fabricante_processador, ssd))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Produto salvo com sucesso!")
    load_products()

# Função para carregar e exibir os produtos na tabela
def load_products():
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect('produtos_computador.db')
    c = conn.cursor()
    c.execute('SELECT * FROM produtos')
    products = c.fetchall()
    conn.close()

    for index, product in enumerate(products, start=1):
        tree.insert('', 'end', iid=index, values=(index, *product[1:]))
    

# Função para editar um produto
def edit_product():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selecionar Produto", "Por favor, selecione um produto para editar.")
        return
    
    item_values = tree.item(selected_item)['values']
    entry_codigo.delete(0, tk.END)
    entry_codigo.insert(0, item_values[1])
    combo_fabricante.set(item_values[2])
    entry_velocidade.delete(0, tk.END)
    entry_velocidade.insert(0, item_values[3])
    combo_nucleos.set(item_values[4])
    combo_ram.set(item_values[5])
    combo_fabricante_processador.set(item_values[6])
    combo_ssd.set(item_values[7])

# Função para salvar as edições de um produto
def save_edit():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selecionar Produto", "Por favor, selecione um produto para editar.")
        return
    
    id_produto = tree.item(selected_item)['values'][0]
    codigo = entry_codigo.get()
    fabricante = combo_fabricante.get()
    velocidade = entry_velocidade.get()
    nucleos = combo_nucleos.get()
    ram = combo_ram.get()
    fabricante_processador = combo_fabricante_processador.get()
    ssd = combo_ssd.get()

    conn = sqlite3.connect('produtos_computador.db')
    c = conn.cursor()
    c.execute('''
        UPDATE produtos 
        SET codigo = ?, fabricante = ?, velocidade = ?, nucleos = ?, ram = ?, fabricante_processador = ?, ssd = ?
        WHERE id = ?
    ''', (codigo, fabricante, velocidade, nucleos, ram, fabricante_processador, ssd, id_produto))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
    load_products()

# Função para excluir um produto
def delete_product():
    codigo = entry_codigo.get()
    conn = sqlite3.connect('produtos_computador.db')
    c = conn.cursor()
    c.execute('DELETE FROM produtos WHERE codigo = ?', (codigo,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
    load_products()

# Função para buscar produtos
def search_products():
    search_value = entry_search.get()
    conn = sqlite3.connect('produtos_computador.db')
    c = conn.cursor()
    c.execute('''
        SELECT * FROM produtos WHERE fabricante LIKE ? OR ram LIKE ? OR fabricante_processador LIKE ? OR ssd LIKE ?
    ''', (f'%{search_value}%', f'%{search_value}%', f'%{search_value}%', f'%{search_value}%'))
    results = c.fetchall()
    conn.close()

    for row in tree.get_children():
        tree.delete(row)

    for index, product in enumerate(results, start=1):
        tree.insert('', 'end', iid=index, values=(index, *product[1:]))

# Inicialização do banco de dados
init_db()

# Criação da janela principal
root = tk.Tk()
root.title("Cadastro de Produtos de Computador")
root.geometry("800x600")
root.config(bg="#f0f0f0")

# Frame para entradas
frame_inputs = tk.Frame(root, bg="#f0f0f0")
frame_inputs.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10, expand=True)

# Criando widgets para entradas
label_codigo = tk.Label(frame_inputs, text="Código do Produto:", bg="#f0f0f0")
label_codigo.grid(row=0, column=0, sticky="w", pady=5)
entry_codigo = tk.Entry(frame_inputs)
entry_codigo.grid(row=0, column=1, pady=5)

label_fabricante = tk.Label(frame_inputs, text="Fabricante:", bg="#f0f0f0")
label_fabricante.grid(row=1, column=0, sticky="w", pady=5)
combo_fabricante = ttk.Combobox(frame_inputs, values=["Apple", "Microsoft", "Google", "Lenovo", "Sony", "Dell", "Samsung", "HP", "Asus"])
combo_fabricante.grid(row=1, column=1, pady=5)

label_velocidade = tk.Label(frame_inputs, text="Velocidade do Processador (GHz):", bg="#f0f0f0")
label_velocidade.grid(row=2, column=0, sticky="w", pady=5)
entry_velocidade = tk.Entry(frame_inputs)
entry_velocidade.grid(row=2, column=1, pady=5)

label_nucleos = tk.Label(frame_inputs, text="Núcleos do Processador:", bg="#f0f0f0")
label_nucleos.grid(row=3, column=0, sticky="w", pady=5)
combo_nucleos = ttk.Combobox(frame_inputs, values=[4, 6, 8, 10, 12, 16])
combo_nucleos.grid(row=3, column=1, pady=5)

label_ram = tk.Label(frame_inputs, text="Memória RAM (GB):", bg="#f0f0f0")
label_ram.grid(row=4, column=0, sticky="w", pady=5)
combo_ram = ttk.Combobox(frame_inputs, values=[8, 16, 32])
combo_ram.grid(row=4, column=1, pady=5)

label_fabricante_processador = tk.Label(frame_inputs, text="Fabricante do Processador:", bg="#f0f0f0")
label_fabricante_processador.grid(row=5, column=0, sticky="w", pady=5)
combo_fabricante_processador = ttk.Combobox(frame_inputs, values=["AMD", "Intel"])
combo_fabricante_processador.grid(row=5, column=1, pady=5)

label_ssd = tk.Label(frame_inputs, text="Capacidade do SSD (GB):", bg="#f0f0f0")
label_ssd.grid(row=6, column=0, sticky="w", pady=5)
combo_ssd = ttk.Combobox(frame_inputs, values=[256, 512, 1024])
combo_ssd.grid(row=6, column=1, pady=5)

# Botões
button_save = tk.Button(frame_inputs, text="Adicionar", command=save_product, bg="#4CAF50", fg="white")
button_save.grid(row=7, column=0, pady=10)

button_edit = tk.Button(frame_inputs, text="Editar", command=edit_product, bg="#FFA500", fg="white")
button_edit.grid(row=7, column=1, pady=10)

button_save_edit = tk.Button(frame_inputs, text="Salvar Edição", command=save_edit, bg="#2196F3", fg="white")
button_save_edit.grid(row=8, column=0, columnspan=2, pady=10)

button_delete = tk.Button(frame_inputs, text="Excluir", command=delete_product, bg="#F44336", fg="white")
button_delete.grid(row=9, column=0, columnspan=2, pady=10)

label_search = tk.Label(frame_inputs, text="Buscar:", bg="#f0f0f0")
label_search.grid(row=10, column=0, sticky="w", pady=5)
entry_search = tk.Entry(frame_inputs)
entry_search.grid(row=10, column=1, pady=5)

button_search = tk.Button(frame_inputs, text="Buscar", command=search_products, bg="#2196F3", fg="white")
button_search.grid(row=11, column=0, columnspan=2, pady=10)

# Frame para tabela
frame_table = tk.Frame(root)
frame_table.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10, expand=True)

# Criando a tabela
tree = ttk.Treeview(frame_table, columns=("id", "codigo", "fabricante", "velocidade", "nucleos", "ram", "fabricante_processador", "ssd"), show='headings')
tree.heading("id", text="ID")
tree.column('#0', width=0, minwidth=0, stretch=False)
tree.heading("codigo", text="Código")
tree.heading("fabricante", text="Fabricante")
tree.heading("velocidade", text="Velocidade (GHz)")
tree.heading("nucleos", text="Núcleos")
tree.heading("ram", text="RAM (GB)")
tree.heading("fabricante_processador", text="Fabricante do Processador")
tree.heading("ssd", text="SSD (GB)")

# Estilo da tabela
tree.tag_configure('oddrow', background="#f9f9f9")
tree.tag_configure('evenrow', background="#ffffff")

# Adicionando a barra de rolagem
scrollbar_y = tk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
tree.configure(yscrollcommand=scrollbar_y.set)

scrollbar_x = tk.Scrollbar(frame_table, orient="horizontal", command=tree.xview)
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
tree.configure(xscrollcommand=scrollbar_x.set)

tree.pack(expand=True, fill=tk.BOTH)

# Carregar produtos ao iniciar o aplicativo
load_products()

# Executa a interface gráfica
root.mainloop()
