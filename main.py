import tkinter as tk
from tkinter import messagebox, ttk
import gestor_de_dados as gd
from modelos_de_dados import Cliente, PlanoTreino, SessaoTreino
import random


def gerar_id(lista):
    if not lista:
        return 1
    return max(item["id"] for item in lista) + 1


def cliente_existe(id_cliente):
    clientes = gd.ler_cliente()
    return any(c["id"] == id_cliente for c in clientes)


def obter_clientes_combo():
    clientes = gd.ler_cliente()
    return [f"{c['nome']} ({c['id']})" for c in clientes]


# ---------------------- INICIO ----------------------

class InicioFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        tk.Label(self, text="Gestor de Ginásio", font=("Times New Roman", 42)).pack(pady=20)

        tk.Button(self, text="Clientes", width=20,
                  command=lambda: app.show_frame("Clientes")).pack(pady=5)

        tk.Button(self, text="Planos", width=20,
                  command=lambda: app.show_frame("Planos")).pack(pady=5)

        tk.Button(self, text="Sessões", width=20,
                  command=lambda: app.show_frame("Sessoes")).pack(pady=5)

        tk.Button(self, text="Estatísticas", width=20,
                  command=lambda: app.show_frame("Estatisticas")).pack(pady=5)


# ---------------------- CLIENTES ----------------------

class ClientesFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="Clientes", font=("Arial", 16)).grid(row=0, column=0, pady=10)

        style = ttk.Style()
        style.configure("Treeview", rowheight=25, borderwidth=1, relief="solid")
        style.configure("Treeview.Heading", borderwidth=1, relief="solid")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.lista = ttk.Treeview(self, columns=("ID", "Nome", "Idade", "Peso", "Objetivo"), show="headings")

        self.lista.heading("ID", text="ID")
        self.lista.heading("Nome", text="Nome")
        self.lista.heading("Idade", text="Idade")
        self.lista.heading("Peso", text="Peso")
        self.lista.heading("Objetivo", text="Objetivo")

        self.lista.column("ID", width=40, anchor="center")
        self.lista.column("Nome", width=120, anchor="center")
        self.lista.column("Idade", width=60, anchor="center")
        self.lista.column("Peso", width=60, anchor="center")
        self.lista.column("Objetivo", width=120, anchor="center")

        self.lista.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        form = tk.Frame(self)
        form.grid(row=2, column=0, pady=10)

        tk.Label(form, text="Nome").grid(row=0, column=0)
        self.nome = tk.Entry(form)
        self.nome.grid(row=0, column=1)

        tk.Label(form, text="Idade").grid(row=1, column=0)
        self.idade = tk.Entry(form)
        self.idade.grid(row=1, column=1)

        tk.Label(form, text="Peso").grid(row=2, column=0)
        self.peso = tk.Entry(form)
        self.peso.grid(row=2, column=1)

        tk.Label(form, text="Objetivo").grid(row=3, column=0)
        self.objetivo = tk.Entry(form)
        self.objetivo.grid(row=3, column=1)

        botoes = tk.Frame(self, bg="#B3E5FC")
        botoes.grid(row=3, column=0, sticky="ew", padx=20, pady=10)

        botoes.grid_columnconfigure(0, weight=1)

        tk.Button(botoes, text="Voltar", command=lambda: app.show_frame("Inicio")).grid(row=0, column=0, sticky="w")
        tk.Button(botoes, text="Adicionar", command=self.adicionar).grid(row=0, column=1)
        tk.Button(botoes, text="Apagar Cliente", command=self.apagar).grid(row=0, column=2, sticky="e")

        self.atualizar()

    def adicionar(self):
        try:
            idade = int(self.idade.get())
            peso = float(self.peso.get())
        except:
            messagebox.showerror("Erro", "Valores inválidos")
            return

        nome = self.nome.get().strip()
        objetivo = self.objetivo.get().strip()

        if not nome or not objetivo:
            messagebox.showerror("Erro", "Campos vazios")
            return

        clientes = gd.ler_cliente()
        novo_id = gerar_id(clientes)

        cliente = Cliente(novo_id, nome, idade, peso, objetivo)
        gd.guardar_cliente(cliente)

        self.nome.delete(0, tk.END)
        self.idade.delete(0, tk.END)
        self.peso.delete(0, tk.END)
        self.objetivo.delete(0, tk.END)

        self.atualizar()

    def apagar(self):
        selecionado = self.lista.selection()

        if not selecionado:
            messagebox.showerror("Erro", "Nenhum cliente selecionado")
            return

        item = self.lista.item(selecionado)
        id_cliente = item["values"][0]

        clientes = gd.ler_cliente()
        clientes = [c for c in clientes if c["id"] != id_cliente]

        gd.guardar_ficheiro("dados/clientes.json", clientes)

        self.atualizar()

    def atualizar(self):
        for item in self.lista.get_children():
            self.lista.delete(item)

        for c in gd.ler_cliente():
            self.lista.insert("", "end", values=(
                c["id"],
                c["nome"],
                c["idade"],
                c["peso"],
                c["objetivo"]
            ))

    def adicionar(self):
        try:
            idade = int(self.idade.get())
            peso = float(self.peso.get())
        except:
            messagebox.showerror("Erro", "Valores inválidos")
            return

        nome = self.nome.get().strip()
        objetivo = self.objetivo.get().strip()

        if not nome or not objetivo:
            messagebox.showerror("Erro", "Campos vazios")
            return

        clientes = gd.ler_cliente()
        novo_id = gerar_id(clientes)

        cliente = Cliente(novo_id, nome, idade, peso, objetivo)
        gd.guardar_cliente(cliente)

        self.nome.delete(0, tk.END)
        self.idade.delete(0, tk.END)
        self.peso.delete(0, tk.END)
        self.objetivo.delete(0, tk.END)

        self.atualizar()

    def apagar(self):
        selecionado = self.lista.selection()

        if not selecionado:
            messagebox.showerror("Erro", "Nenhum cliente selecionado")
            return

        item = self.lista.item(selecionado)
        id_cliente = item["values"][0]

        clientes = gd.ler_cliente()
        clientes = [c for c in clientes if c["id"] != id_cliente]

        gd.guardar_ficheiro("dados/clientes.json", clientes)

        self.atualizar()

    def atualizar(self):
        for item in self.lista.get_children():
            self.lista.delete(item)

        for c in gd.ler_cliente():
            self.lista.insert("", "end", values=(
                c["id"],
                c["nome"],
                c["idade"],
                c["peso"],
                c["objetivo"]
            ))


# ---------------------- PLANOS ----------------------

class PlanosFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="Planos", font=("Arial", 16)).grid(row=0, column=0, pady=10)

        style = ttk.Style()
        style.configure("Treeview", rowheight=25, borderwidth=1, relief="solid")
        style.configure("Treeview.Heading", borderwidth=1, relief="solid")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.lista = ttk.Treeview(self, columns=("ID", "Cliente", "Objetivo", "Exercícios", "Dias"), show="headings")

        self.lista.heading("ID", text="ID")
        self.lista.heading("Cliente", text="Cliente")
        self.lista.heading("Objetivo", text="Objetivo")
        self.lista.heading("Exercícios", text="Exercícios")
        self.lista.heading("Dias", text="Dias")

        self.lista.column("ID", width=40, anchor="center")
        self.lista.column("Cliente", width=80, anchor="center")
        self.lista.column("Objetivo", width=120, anchor="center")
        self.lista.column("Exercícios", width=200, anchor="center")
        self.lista.column("Dias", width=60, anchor="center")

        self.lista.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        form = tk.Frame(self)
        form.grid(row=2, column=0, pady=10)

        tk.Label(form, text="Cliente").grid(row=0, column=0)
        self.entry_cliente = ttk.Combobox(form, values=obter_clientes_combo())
        self.entry_cliente.grid(row=0, column=1)
        self.entry_cliente.set("Selecionar cliente")

        tk.Label(form, text="Objetivo").grid(row=1, column=0)
        self.objetivo = tk.Entry(form)
        self.objetivo.grid(row=1, column=1)

        tk.Label(form, text="Dias/semana").grid(row=2, column=0)
        self.dias = tk.Entry(form)
        self.dias.grid(row=2, column=1)

        botoes = tk.Frame(self, bg="#B3E5FC")
        botoes.grid(row=3, column=0, sticky="ew", padx=20, pady=10)

        botoes.grid_columnconfigure(0, weight=1)

        tk.Button(botoes, text="Voltar", command=lambda: app.show_frame("Inicio")).grid(row=0, column=0, sticky="w")
        tk.Button(botoes, text="Gerar Plano", command=self.gerar).grid(row=0, column=1)
        tk.Button(botoes, text="Apagar Plano", command=self.apagar).grid(row=0, column=2, sticky="e")

        self.atualizar()

    def escolher_categoria(self, objetivo):
        objetivo = objetivo.lower()

        if objetivo == "ganhar massa":
            return ["forca"]
        elif objetivo == "perder peso":
            return ["cardio"]
        else:
            return ["forca", "cardio", "core"]


    def gerar_exercicios(self, objetivo, dias):
        EXERCICIOS = {
            "forca": ["Supino", "Agachamento", "Flexões"],
            "cardio": ["Corrida", "Bicicleta", "Corda"],
            "core": ["Abdominais", "Prancha"]
        }

        categorias = self.escolher_categoria(objetivo)

        pool = []
        for c in categorias:
            pool.extend(EXERCICIOS[c])

        quantidade = min(2 + dias // 2, len(pool))

        return random.sample(pool, quantidade)


    def gerar(self):
        try:
            texto = self.entry_cliente.get()
            id_cliente = int(texto.split("(")[-1].replace(")", ""))
            dias = int(self.dias.get())
        except:
            messagebox.showerror("Erro", "Valores inválidos")
            return

        if not cliente_existe(id_cliente):
            messagebox.showerror("Erro", "Cliente não existe")
            return

        objetivo = self.objetivo.get()

        if objetivo == "Selecionar objetivo":
            messagebox.showerror("Erro", "Seleciona um objetivo")
            return

        lista = self.gerar_exercicios(objetivo, dias)

        planos = gd.ler_plano()
        novo_id = gerar_id(planos)

        plano = PlanoTreino(novo_id, id_cliente, objetivo, lista, dias)
        gd.guardar_plano(plano)

        self.objetivo.set("Selecionar objetivo")
        self.dias.delete(0, tk.END)

        self.atualizar()

    def apagar(self):
        selecionado = self.lista.selection()

        if not selecionado:
            messagebox.showerror("Erro", "Nenhum plano selecionado")
            return

        item = self.lista.item(selecionado)
        id_plano = item["values"][0]

        planos = gd.ler_plano()
        planos = [p for p in planos if p["id"] != id_plano]

        gd.guardar_ficheiro("dados/planos.json", planos)

        self.atualizar()

    def atualizar(self):
        for item in self.lista.get_children():
            self.lista.delete(item)

        for p in gd.ler_plano():
            self.lista.insert("", "end", values=(
                p["id"],
                p["id_cliente"],
                p["objetivo"],
                 (p["lista_exercicios"]),
                 p["dias_semana"]
                ))
                
# ---------------------- SESSÕES ----------------------

class SessoesFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        tk.Label(self, text="Sessões", font=("Arial", 16)).pack(pady=10)

        self.lista = tk.Listbox(self)
        self.lista.pack(fill="both", expand=True, padx=20, pady=10)

        self.id_cliente = ttk.Combobox(self, values=obter_clientes_combo())
        self.id_cliente.pack()
        self.id_cliente.set("Selecionar cliente")

        self.data = tk.Entry(self)
        self.data.pack()
        self.data.insert(0, "YYYY-MM-DD")

        self.duracao = tk.Entry(self)
        self.duracao.pack()
        self.duracao.insert(0, "Duração")

        tk.Button(self, text="Adicionar Sessão", command=self.adicionar).pack(pady=5)
        tk.Button(self, text="Voltar", command=lambda: app.show_frame("Inicio")).pack()

        self.atualizar()

    def adicionar(self):
        try:
            texto = self.id_cliente.get()
            id_cliente = int(texto.split("(")[-1].replace(")", ""))
            duracao = float(self.duracao.get())
        except:
            messagebox.showerror("Erro", "Valores inválidos")
            return

        if not cliente_existe(id_cliente):
            messagebox.showerror("Erro", "Cliente não existe")
            return

        data = self.data.get()

        sessoes = gd.ler_sessao()
        novo_id = gerar_id(sessoes)

        sessao = SessaoTreino(novo_id, id_cliente, data, duracao)
        gd.guardar_sessao(sessao)

        self.atualizar()

    def atualizar(self):
        self.lista.delete(0, tk.END)
        for s in gd.ler_sessao():
            self.lista.insert(tk.END, f"{s['id']} - Cliente {s['id_cliente']}")


# ---------------------- ESTATÍSTICAS ----------------------

class EstatisticasFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        tk.Label(self, text="Estatísticas", font=("Arial", 16)).pack(pady=10)

        self.label = tk.Label(self, text="")
        self.label.pack(pady=10)

        tk.Button(self, text="Atualizar", command=self.calcular).pack(pady=5)
        tk.Button(self, text="Voltar", command=lambda: app.show_frame("Inicio")).pack()

    def calcular(self):
        sessoes = gd.ler_sessao()

        contagem = {}
        for s in sessoes:
            cid = s["id_cliente"]
            contagem[cid] = contagem.get(cid, 0) + 1

        if not contagem:
            self.label.config(text="Sem dados")
            return

        top = max(contagem, key=contagem.get)
        self.label.config(text=f"Cliente mais ativo: {top} ({contagem[top]} sessões)")


# ---------------------- APP ----------------------

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gestor de Ginásio")
        self.geometry("800x500")

        self.configure(bg="#B3E5FC")

        container = tk.Frame(self, bg="#B3E5FC")
        container.pack(fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F, name in [
            (InicioFrame, "Inicio"),
            (ClientesFrame, "Clientes"),
            (PlanosFrame, "Planos"),
            (SessoesFrame, "Sessoes"),
            (EstatisticasFrame, "Estatisticas")
        ]:
            frame = F(container, self)
            frame.configure(bg="#B3E5FC")
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Inicio")

    def show_frame(self, nome):
        self.frames[nome].tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()