import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# Nome do arquivo de banco de dados JSON
DB_FILE = 'produtos_computador.json'

# Inicialização do banco de dados (Cria o arquivo se não existir)
def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

# Função para carregar dados do arquivo JSON
def data_load():
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Função para salvar dados no arquivo JSON
def data_save(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

# Função para salvar o produto
def save_product():
    codigo = entry_codigo.get()
    
    if not codigo:
        messagebox.showwarning("Aviso", "O código do produto é obrigatório.")
        return

    novo_produto = {
        "codigo": codigo,
        "fabricante": combo_fabricante.get(),
        "velocidade": entry_velocidade.get(),
        "nucleos": combo_nucleos.get(),
        "ram": combo_ram.get(),
        "fabricante_processador": combo_fabricante_processador.get(),
        "ssd": combo_ssd.get()
    }

    produtos = data_load()
    
    # Verifica se o código já existe
    if any(p['codigo'] == codigo for p in produtos):
        messagebox.showerror("Erro", "Já existe um produto com este código.")
        return

    produtos.append(novo_produto)
    data_save(produtos)
    
    messagebox.showinfo("Sucesso", "Produto salvo com sucesso!")
    clear_entries()
    load_products()

# Função para carregar e exibir os produtos na tabela
def load_products(filter_data=None):
    for row in tree.get_children():
        tree.delete(row)

    produtos = filter_data if filter_data is not None else data_load()

    for p in produtos:
        tree.insert('', 'end', values=(
            p.get('codigo'), 
            p.get('fabricante'), 
            p.get('velocidade'), 
            p.get('nucleos'), 
            p.get('ram'), 
            p.get('fabricante_processador'), 
            p.get('ssd')
        ))

# Função para preencher os campos ao selecionar na tabela
def edit_product():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selecionar", "Selecione um produto na tabela.")
        return
    
    item_values = tree.item(selected_item)['values']
    
    entry_codigo.delete(0, tk.END)
    entry_codigo.insert(0, item_values[0])
    combo_fabricante.set(item_values[1])
    entry_velocidade.delete(0, tk.END)
    entry_velocidade.insert(0, item_values[2])
    combo_nucleos.set(item_values[3])
    combo_ram.set(item_values[4])
    combo_fabricante_processador.set(item_values[5])
    combo_ssd.set(item_values[6])

# Função para salvar as edições
def save_edit():
    codigo_original = entry_codigo.get()
    produtos = data_load()
    
    encontrado = False
    for p in produtos:
        if p['codigo'] == codigo_original:
            p['fabricante'] = combo_fabricante.get()
            p['velocidade'] = entry_velocidade.get()
            p['nucleos'] = combo_nucleos.get()
            p['ram'] = combo_ram.get()
            p['fabricante_processador'] = combo_fabricante_processador.get()
            p['ssd'] = combo_ssd.get()
            encontrado = True
            break
    
    if encontrado:
        data_save(produtos)
        messagebox.showinfo("Sucesso", "Produto atualizado!")
        load_products()
    else:
        messagebox.showerror("Erro", "Produto não encontrado para edição.")

# Função para excluir um produto
def delete_product():
    codigo = entry_codigo.get()
    produtos = data_load()
    
    novos_produtos = [p for p in produtos if p['codigo'] != codigo]
    
    if len(novos_produtos) < len(produtos):
        data_save(novos_produtos)
        messagebox.showinfo("Sucesso", "Produto excluído!")
        clear_entries()
        load_products()
    else:
        messagebox.showwarning("Erro", "Selecione um produto válido pelo código.")

# Função para buscar produtos
def search_products():
    search_value = entry_search.get().lower()
    produtos = data_load()
    
    resultados = [
        p for p in produtos if 
        search_value in str(p.get('fabricante')).lower() or 
        search_value in str(p.get('ram')).lower() or 
        search_value in str(p.get('fabricante_processador')).lower() or 
        search_value in str(p.get('codigo')).lower()
    ]
    
    load_products(resultados)

def clear_entries():
    entry_codigo.delete(0, tk.END)
    entry_velocidade.delete(0, tk.END)
    combo_fabricante.set('')
    combo_nucleos.set('')
    combo_ram.set('')
    combo_fabricante_processador.set('')
    combo_ssd.set('')

# Inicialização
init_db()

root = tk.Tk()
root.title("Gerenciador de Produtos de PC")
root.geometry("1000x600")
root.config(bg="#f0f0f0")

# Interface (Mesma estrutura anterior, removendo ID da Treeview)
frame_inputs = tk.Frame(root, bg="#f0f0f0")
frame_inputs.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

label_codigo = tk.Label(frame_inputs, text="Código (Chave):", bg="#f0f0f0").grid(row=0, column=0, sticky="w")
entry_codigo = tk.Entry(frame_inputs)
entry_codigo.grid(row=0, column=1, pady=5)

label_fabricante = tk.Label(frame_inputs, text="Fabricante:", bg="#f0f0f0").grid(row=1, column=0, sticky="w")
combo_fabricante = ttk.Combobox(frame_inputs, values=["Apple", "Lenovo", "Dell", "Sony", "Microsoft", "Samsung", "Google", "HP", "Asus"])
combo_fabricante.grid(row=1, column=1, pady=5)

label_velocidade = tk.Label(frame_inputs, text="Velocidade (GHz):", bg="#f0f0f0").grid(row=2, column=0, sticky="w")
entry_velocidade = tk.Entry(frame_inputs)
entry_velocidade.grid(row=2, column=1, pady=5)

label_nucleos = tk.Label(frame_inputs, text="Núcleos:", bg="#f0f0f0").grid(row=3, column=0, sticky="w")
combo_nucleos = ttk.Combobox(frame_inputs, values=[4, 6, 8, 12, 16])
combo_nucleos.grid(row=3, column=1, pady=5)

label_ram = tk.Label(frame_inputs, text="RAM (GB):", bg="#f0f0f0").grid(row=4, column=0, sticky="w")
combo_ram = ttk.Combobox(frame_inputs, values=[8, 16, 32, 64])
combo_ram.grid(row=4, column=1, pady=5)

label_proc = tk.Label(frame_inputs, text="Processador:", bg="#f0f0f0").grid(row=5, column=0, sticky="w")
combo_fabricante_processador = ttk.Combobox(frame_inputs, values=["AMD", "Intel", "Apple Silicon"])
combo_fabricante_processador.grid(row=5, column=1, pady=5)

label_ssd = tk.Label(frame_inputs, text="SSD (GB):", bg="#f0f0f0").grid(row=6, column=0, sticky="w")
combo_ssd = ttk.Combobox(frame_inputs, values=[256, 512, 1024, 2048])
combo_ssd.grid(row=6, column=1, pady=5)

# Botões
tk.Button(frame_inputs, text="Adicionar", command=save_product, bg="#4CAF50", fg="white", width=15).grid(row=7, column=0, pady=5)
tk.Button(frame_inputs, text="Editar Selecionado", command=edit_product, bg="#FFA500", fg="white", width=15).grid(row=7, column=1, pady=5)
tk.Button(frame_inputs, text="Salvar Alteração", command=save_edit, bg="#2196F3", fg="white", width=32).grid(row=8, column=0, columnspan=2, pady=5)
tk.Button(frame_inputs, text="Excluir por Código", command=delete_product, bg="#F44336", fg="white", width=32).grid(row=9, column=0, columnspan=2, pady=5)

tk.Label(frame_inputs, text="Buscar:", bg="#f0f0f0").grid(row=10, column=0, sticky="w", pady=(20,0))
entry_search = tk.Entry(frame_inputs)
entry_search.grid(row=10, column=1, pady=(20,0))
tk.Button(frame_inputs, text="Filtrar", command=search_products, bg="#2196F3", fg="white", width=32).grid(row=11, column=0, columnspan=2, pady=5)

# Tabela (Sem coluna ID)
frame_table = tk.Frame(root)
frame_table.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10, expand=True)

tree = ttk.Treeview(frame_table, columns=("codigo", "fabricante", "velocidade", "nucleos", "ram", "fabricante_processador", "ssd"), show='headings')
tree.heading("codigo", text="Código")
tree.heading("fabricante", text="Fabricante")
tree.heading("velocidade", text="Velocidade")
tree.heading("nucleos", text="Núcleos")
tree.heading("ram", text="RAM")
tree.heading("fabricante_processador", text="Processador")
tree.heading("ssd", text="SSD")

# Ajuste de largura das colunas
for col in tree["columns"]:
    tree.column(col, width=100)

scrollbar_y = tk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar_y.set)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
tree.pack(expand=True, fill=tk.BOTH)

load_products()
root.mainloop()
