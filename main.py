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

        tk.Label(self, text="Clientes", font=("Arial", 16)).pack(pady=10)

        self.lista = tk.Listbox(self)
        self.lista.pack(fill="both", expand=True, padx=20, pady=10)

        form = tk.Frame(self)
        form.pack()

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

        tk.Button(self, text="Adicionar", command=self.adicionar).pack(pady=5)
        tk.Button(self, text="Voltar", command=lambda: app.show_frame("Inicio")).pack()

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

    def atualizar(self):
        self.lista.delete(0, tk.END)
        for c in gd.ler_cliente():
            self.lista.insert(tk.END, f"{c['id']} - {c['nome']}")


# ---------------------- PLANOS ----------------------

class PlanosFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        tk.Label(self, text="Planos", font=("Arial", 16)).pack(pady=10)

        self.lista = tk.Listbox(self)
        self.lista.pack(fill="both", expand=True, padx=20, pady=10)

        self.entry_cliente = ttk.Combobox(self, values=obter_clientes_combo())
        self.entry_cliente.pack()
        self.entry_cliente.set("Selecionar cliente")

        self.objetivo = tk.Entry(self)
        self.objetivo.pack()
        self.objetivo.insert(0, "Objetivo")

        self.dias = tk.Entry(self)
        self.dias.pack()
        self.dias.insert(0, "Dias/semana")

        tk.Button(self, text="Gerar Plano", command=self.gerar).pack(pady=5)
        tk.Button(self, text="Voltar", command=lambda: app.show_frame("Inicio")).pack()

        self.atualizar()

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

        exercicios = ["Supino", "Agachamento", "Corrida", "Bicicleta", "Flexões", "Abdominais"]
        lista = random.sample(exercicios, 3)

        planos = gd.ler_plano()
        novo_id = gerar_id(planos)

        plano = PlanoTreino(novo_id, id_cliente, objetivo, lista, dias)
        gd.guardar_plano(plano)

        self.atualizar()

    def atualizar(self):
        self.lista.delete(0, tk.END)
        for p in gd.ler_plano():
            self.lista.insert(tk.END, f"{p['id']} - Cliente {p['id_cliente']}")


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