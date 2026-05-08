import tkinter as tk
from tkinter import messagebox, ttk
import gestor_de_dados as gd
from modelos_de_dados import Cliente, PlanoTreino, SessaoTreino
import random
from datetime import *
from collections import Counter


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
        self.lista.column("Idade", width=80, anchor="center")
        self.lista.column("Peso", width=80, anchor="center")
        self.lista.column("Objetivo", width=140, anchor="center")

        self.lista.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        form = tk.Frame(self)
        form.grid(row=2, column=0, pady=10)

        tk.Label(form, text="Nome").grid(row=0, column=0)
        self.nome = tk.Entry(form)
        self.nome.grid(row=0, column=1)

        tk.Label(form, text="Idade").grid(row=1, column=0)
        self.idade = ttk.Combobox(form, values=[str(i) for i in range(14, 81)])
        self.idade.grid(row=1, column=1)
        self.idade.set("Idade")

        tk.Label(form, text="Peso").grid(row=2, column=0)
        self.peso = ttk.Combobox(form, values=[str(i) for i in range(40, 151)])
        self.peso.grid(row=2, column=1)
        self.peso.set("Peso")

        tk.Label(form, text="Objetivo").grid(row=3, column=0)
        self.objetivo = ttk.Combobox(form, values=["Ganhar Massa", "Perder Peso"])
        self.objetivo.grid(row=3, column=1)
        self.objetivo.set("Objetivo")

        botoes = tk.Frame(self, bg="#B3E5FC")
        botoes.grid(row=3, column=0, sticky="ew", padx=20, pady=10)

        botoes.grid_columnconfigure(0, weight=1)

        tk.Button(botoes, text="Voltar", command=lambda: app.show_frame("Inicio")).grid(row=0, column=0, sticky="w")
        tk.Button(botoes, text="Adicionar", command=self.adicionar).grid(row=0, column=1)
        tk.Button(botoes, text="Apagar Cliente", command=self.apagar).grid(row=0, column=2)
        tk.Button(botoes, text="Atualizar", command=self.atualizar).grid(row=0, column=3, sticky="e")

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

        if objetivo == "Objetivo":
            messagebox.showerror("Erro", "Seleciona um objetivo")
            return

        if not nome:
            messagebox.showerror("Erro", "Nome vazio")
            return

        clientes = gd.ler_cliente()
        novo_id = gerar_id(clientes)

        cliente = Cliente(novo_id, nome, idade, peso, objetivo)
        gd.guardar_cliente(cliente)

        self.nome.delete(0, tk.END)
        self.idade.set("Idade")
        self.peso.set("Peso")
        self.objetivo.set("Objetivo")

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
        self.lista.delete(*self.lista.get_children())

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

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.lista = ttk.Treeview(
            self,
            columns=("ID", "Cliente", "Objetivo", "Exercícios", "Dias"),
            show="headings"
        )

        for col, w in [
            ("ID", 40),
            ("Cliente", 140),
            ("Objetivo", 120),
            ("Exercícios", 200),
            ("Dias", 60),
        ]:
            self.lista.heading(col, text=col)
            self.lista.column(col, width=w, anchor="center")

        self.lista.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        form = tk.Frame(self)
        form.grid(row=2, column=0, pady=10)

        tk.Label(form, text="Cliente").grid(row=0, column=0)
        self.entry_cliente = ttk.Combobox(form, state="readonly")
        self.entry_cliente.grid(row=0, column=1)

        tk.Label(form, text="Objetivo").grid(row=1, column=0)
        self.objetivo = ttk.Combobox(form, values=["Ganhar Massa", "Perder Peso"], state="readonly")
        self.objetivo.grid(row=1, column=1)
        self.objetivo.current(0)

        tk.Label(form, text="Dias").grid(row=2, column=0)
        self.dias = ttk.Combobox(form, values=["1","2","3","4","5","6","7"], state="readonly")
        self.dias.grid(row=2, column=1)
        self.dias.current(2)

        botoes = tk.Frame(self, bg="#B3E5FC")
        botoes.grid(row=3, column=0, sticky="ew", padx=20, pady=10)

        botoes.grid_columnconfigure(0, weight=1)

        tk.Button(botoes, text="Voltar", command=lambda: self.app.show_frame("Inicio")).grid(row=0, column=0, sticky="w")
        tk.Button(botoes, text="Gerar Plano", command=self.gerar).grid(row=0, column=1)
        tk.Button(botoes, text="Apagar Plano", command=self.apagar).grid(row=0, column=2, sticky="e")
        tk.Button(botoes, text="Atualizar", command=self.atualizar).grid(row=0, column=3)

        self.atualizar()

    def parse_cliente(self, texto):
        try:
            return int(texto.split("(")[-1].replace(")", "").strip())
        except:
            return None

    def carregar_clientes(self):
        clientes = gd.ler_cliente()
        valores = [f"{c['nome']} ({c['id']})" for c in clientes if isinstance(c, dict)]
        self.entry_cliente["values"] = valores
        if valores:
            self.entry_cliente.set(valores[0])
        else:
            self.entry_cliente.set("Sem clientes")

    def limpar_orfaos(self):
        clientes = gd.ler_cliente()
        ids_validos = {int(c["id"]) for c in clientes if isinstance(c, dict)}

        planos = gd.ler_plano()
        planos = [p for p in planos if int(p.get("id_cliente")) in ids_validos]

        gd.guardar_ficheiro("dados/planos.json", planos)

    def gerar_exercicios(self, objetivo, dias):
        EXERCICIOS = {
            "forca": ["Supino", "Agachamento", "Flexões"],
            "cardio": ["Corrida", "Bicicleta", "Corda"],
            "core": ["Abdominais", "Prancha"]
        }

        objetivo = objetivo.lower()

        if "massa" in objetivo:
            cats = ["forca"]
        elif "peso" in objetivo:
            cats = ["cardio"]
        else:
            cats = ["forca", "cardio", "core"]

        pool = []
        for c in cats:
            pool.extend(EXERCICIOS[c])

        quantidade = min(2 + int(dias) // 2, len(pool))
        return random.sample(pool, quantidade)

    def atualizar(self):
        self.limpar_orfaos()
        self.carregar_clientes()

        self.lista.delete(*self.lista.get_children())

        for p in gd.ler_plano():
            self.lista.insert("", "end", values=(
                p.get("id"),
                p.get("id_cliente"),
                p.get("objetivo"),
                ", ".join(p.get("lista_exercicios", [])),
                p.get("dias_semana"),
            ))

    def gerar(self):
        id_cliente = self.parse_cliente(self.entry_cliente.get())
        if id_cliente is None:
            return

        if not cliente_existe(id_cliente):
            self.atualizar()
            return

        dias = int(self.dias.get())
        objetivo = self.objetivo.get()

        lista = self.gerar_exercicios(objetivo, dias)

        planos = gd.ler_plano()
        novo_id = gerar_id(planos)

        plano = PlanoTreino(novo_id, id_cliente, objetivo, lista, dias)
        gd.guardar_plano(plano)

        self.atualizar()

    def apagar(self):
        sel = self.lista.selection()
        if not sel:
            return

        id_plano = self.lista.item(sel)["values"][0]

        planos = gd.ler_plano()
        planos = [p for p in planos if p.get("id") != id_plano]

        gd.guardar_ficheiro("dados/planos.json", planos)
        self.atualizar()
            
# ---------------------- SESSÕES ----------------------

class SessoesFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="Sessões", font=("Arial", 16)).grid(row=0, column=0, pady=10)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.lista = ttk.Treeview(
            self,
            columns=("ID", "Cliente", "Data", "Duração"),
            show="headings"
        )

        for col, w in [
            ("ID", 60),
            ("Cliente", 120),
            ("Data", 120),
            ("Duração", 80),
        ]:
            self.lista.heading(col, text=col)
            self.lista.column(col, width=w, anchor="center")

        self.lista.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        form = tk.Frame(self)
        form.grid(row=2, column=0, pady=10)

        tk.Label(form, text="Cliente").grid(row=0, column=0)
        self.id_cliente = ttk.Combobox(form, state="readonly")
        self.id_cliente.grid(row=0, column=1)

        tk.Label(form, text="Data").grid(row=1, column=0)
        self.data = ttk.Combobox(form, state="readonly")
        self.data.grid(row=1, column=1)

        tk.Label(form, text="Duração").grid(row=2, column=0)
        self.duracao = ttk.Combobox(form, values=[30,45,60,75,90,120], state="readonly")
        self.duracao.grid(row=2, column=1)
        self.duracao.current(2)

        botoes = tk.Frame(self, bg="#B3E5FC")
        botoes.grid(row=3, column=0, sticky="ew", padx=20, pady=10)

        botoes.grid_columnconfigure(0, weight=1)

        tk.Button(botoes, text="Voltar", command=lambda: self.app.show_frame("Inicio")).grid(row=0, column=0, sticky="w")
        tk.Button(botoes, text="Adicionar", command=self.adicionar).grid(row=0, column=1)
        tk.Button(botoes, text="Apagar", command=self.apagar).grid(row=0, column=2, sticky="e")
        tk.Button(botoes, text="Atualizar", command=self.atualizar).grid(row=0, column=3)

        self.atualizar()

    def gerar_datas(self):
        hoje = date.today()
        return [(hoje + timedelta(days=i)).isoformat() for i in range(-30, 31)]

    def carregar_clientes(self):
        clientes = gd.ler_cliente()
        valores = [f"{c['nome']} ({c['id']})" for c in clientes if isinstance(c, dict)]
        self.id_cliente["values"] = valores
        if valores:
            self.id_cliente.set(valores[0])
        else:
            self.id_cliente.set("Sem clientes")

    def carregar_datas(self):
        datas = self.gerar_datas()
        self.data["values"] = datas
        self.data.current(30)

    def limpar_orfaos(self):
        clientes = gd.ler_cliente()
        ids_validos = {int(c["id"]) for c in clientes if isinstance(c, dict)}

        sessoes = gd.ler_sessao()
        sessoes = [s for s in sessoes if int(s.get("id_cliente")) in ids_validos]

        gd.guardar_ficheiro("dados/sessoes.json", sessoes)

    def atualizar(self):
        self.limpar_orfaos()
        self.carregar_clientes()
        self.carregar_datas()

        self.lista.delete(*self.lista.get_children())

        for s in gd.ler_sessao():
            self.lista.insert("", "end", values=(
                s.get("id"),
                s.get("id_cliente"),
                s.get("data"),
                s.get("duracao")
            ))

    def adicionar(self):
        try:
            id_cliente = int(self.id_cliente.get().split("(")[-1].replace(")", ""))
            data = self.data.get()
            duracao = float(self.duracao.get())
        except:
            return

        if not cliente_existe(id_cliente):
            self.atualizar()
            return

        sessoes = gd.ler_sessao()
        novo_id = gerar_id(sessoes)

        gd.guardar_sessao(SessaoTreino(novo_id, id_cliente, data, duracao))
        self.atualizar()

    def apagar(self):
        sel = self.lista.selection()
        if not sel:
            return

        id_sessao = self.lista.item(sel)["values"][0]

        sessoes = gd.ler_sessao()
        sessoes = [s for s in sessoes if s.get("id") != id_sessao]

        gd.guardar_ficheiro("dados/sessoes.json", sessoes)
        self.atualizar()


# ---------------------- ESTATÍSTICAS ----------------------

class EstatisticasFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="Estatísticas", font=("Arial", 16)).pack(pady=10)

        self.label = tk.Label(self, text="", justify="left")
        self.label.pack(pady=10)

        tk.Button(self, text="Atualizar", command=self.calcular).pack(pady=5)
        tk.Button(self, text="Simular Progresso", command=self.simular_progresso).pack(pady=5)
        tk.Button(self, text="Voltar", command=lambda: app.show_frame("Inicio")).pack()

    def calcular(self):
        clientes = gd.ler_cliente()
        sessoes = gd.ler_sessao()
        planos = gd.ler_plano()

        if not clientes:
            self.label.config(text="Sem dados")
            return

        if not sessoes:
            self.label.config(text="Sem sessões")
            return

        contagem = Counter([s["id_cliente"] for s in sessoes])

        mais_ativo_id = max(contagem, key=contagem.get)
        menos_ativo_id = min(contagem, key=contagem.get)

        clientes_dict = {c["id"]: c for c in clientes}

        mais_comum = "N/A"
        exercicios = []
        for p in planos:
            exercicios.extend(p.get("lista_exercicios", []))

        if exercicios:
            mais_comum = Counter(exercicios).most_common(1)[0][0]

        texto = (
            f"Cliente mais ativo: {clientes_dict.get(mais_ativo_id, {}).get('nome', mais_ativo_id)}\n"
            f"Cliente menos ativo: {clientes_dict.get(menos_ativo_id, {}).get('nome', menos_ativo_id)}\n\n"
            f"Exercício mais comum: {mais_comum}\n\n"
            f"--- PESOS ATUAIS ---\n"
        )

        for c in clientes:
            texto += f"{c['nome']}: {c['peso']}kg\n"

        self.label.config(text=texto)

    def simular_progresso(self):
        clientes = gd.ler_cliente()
        sessoes = gd.ler_sessao()
        planos = gd.ler_plano()

        plano_por_cliente = {p["id_cliente"]: p for p in planos}

        atividade = {}

        for s in sessoes:
            cid = s["id_cliente"]
            atividade[cid] = atividade.get(cid, 0) + float(s["duracao"]) / 60

        novos_clientes = []

        for c in clientes:
            cid = c["id"]
            peso = float(c["peso"])
            plano = plano_por_cliente.get(cid)

            if plano:
                objetivo = plano["objetivo"].lower()
                dias = int(plano["dias_semana"])
                treino = atividade.get(cid, 0)

                if "massa" in objetivo:
                    peso += treino * 0.2 + dias * 0.1
                elif "perder" in objetivo:
                    peso -= treino * 0.2 + dias * 0.1

            if peso < 40:
                peso = 40

            c["peso"] = round(peso, 1)
            novos_clientes.append(c)

        gd.guardar_ficheiro("dados/clientes.json", novos_clientes)

        self.calcular()

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