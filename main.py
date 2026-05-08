import tkinter as tk
from tkinter import messagebox, ttk
import gestor_de_dados as gd
from modelos_de_dados import Cliente, PlanoTreino, SessaoTreino
import random
from datetime import *
from collections import Counter

# ---------- FUNÇÕES AUXILIARES ----------

def gerar_id(lista):
    #Gera um novo ID sequencial baseado no maior ID existente na lista.
    #Se a lista estiver vazia, começa no 1.
    if not lista:
        return 1
    return max(item["id"] for item in lista) + 1


def cliente_existe(id_cliente):
    # Verifica se um cliente com determinado ID existe na base de dados
    clientes = gd.ler_cliente()
    return any(c["id"] == id_cliente for c in clientes)


def obter_clientes_combo():
    # Devolve uma lista formatada com nomes e IDs dos clientes para usar em Combobox
    clientes = gd.ler_cliente()
    return [f"{c['nome']} ({c['id']})" for c in clientes]


# ---------- ECRÃ INICIAL ----------

class InicioFrame(tk.Frame):
    # Menu principal da aplicação com botões para aceder a cada secção
    def __init__(self, parent, app):
        super().__init__(parent)

        # Título grande e estilizado
        tk.Label(
            self,
            text="🏋 Gestor de Ginásio",
            font=("Segoe UI", 34, "bold"),
            bg="#EAF4F4",
            fg="#2F5061"
        ).pack(pady=40)

        # Botões de navegação para cada módulo da app
        ttk.Button(self, text="👥 Clientes", width=25,
                   command=lambda: app.show_frame("Clientes")).pack(pady=8)

        ttk.Button(self, text="📋 Planos", width=25,
                   command=lambda: app.show_frame("Planos")).pack(pady=8)

        ttk.Button(self, text="🏋️ Sessões", width=25,
                   command=lambda: app.show_frame("Sessoes")).pack(pady=8)

        ttk.Button(self, text="📊 Estatísticas", width=25,
                   command=lambda: app.show_frame("Estatisticas")).pack(pady=8)


# ---------- GESTÃO DE CLIENTES ----------

class ClientesFrame(tk.Frame):
    # Interface para visualizar, adicionar e remover clientes
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # Título da secção
        tk.Label(
            self,
            text="👥 Clientes",
            font=("Segoe UI", 22, "bold"),
            bg="#EAF4F4",
            fg="#2F5061"
        ).grid(row=0, column=0, pady=10)

        # Configuração para a grelha se expandir corretamente
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Tabela (Treeview) para mostrar todos os clientes
        self.lista = ttk.Treeview(self, columns=("ID", "Nome", "Idade", "Peso", "Objetivo"), show="headings")

        # Definir cabeçalhos das colunas
        self.lista.heading("ID", text="ID")
        self.lista.heading("Nome", text="Nome")
        self.lista.heading("Idade", text="Idade")
        self.lista.heading("Peso", text="Peso")
        self.lista.heading("Objetivo", text="Objetivo")

        # Definir largura e alinhamento de cada coluna
        self.lista.column("ID", width=40, anchor="center")
        self.lista.column("Nome", width=120, anchor="center")
        self.lista.column("Idade", width=80, anchor="center")
        self.lista.column("Peso", width=80, anchor="center")
        self.lista.column("Objetivo", width=140, anchor="center")

        self.lista.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        # Formulário para adicionar novo cliente
        form = tk.Frame(self, bg="#EAF4F4")
        form.grid(row=2, column=0, pady=10)

        # Campo: Nome
        tk.Label(form, text="Nome", bg="#EAF4F4",
                 font=("Segoe UI", 10, "bold"), fg="#333").grid(row=0, column=0, padx=5, pady=5)
        self.nome = tk.Entry(form)
        self.nome.grid(row=0, column=1, padx=5, pady=5)

        # Campo: Idade (14 a 80 anos)
        tk.Label(form, text="Idade", bg="#EAF4F4",
                 font=("Segoe UI", 10, "bold"), fg="#333").grid(row=1, column=0, padx=5, pady=5)
        self.idade = ttk.Combobox(form, values=[str(i) for i in range(14, 81)])
        self.idade.grid(row=1, column=1, padx=5, pady=5)
        self.idade.set("Idade")

        # Campo: Peso (40 a 150 kg)
        tk.Label(form, text="Peso", bg="#EAF4F4",
                 font=("Segoe UI", 10, "bold"), fg="#333").grid(row=2, column=0, padx=5, pady=5)
        self.peso = ttk.Combobox(form, values=[str(i) for i in range(40, 151)])
        self.peso.grid(row=2, column=1, padx=5, pady=5)
        self.peso.set("Peso")

        # Campo: Objetivo
        tk.Label(form, text="Objetivo", bg="#EAF4F4",
                 font=("Segoe UI", 10, "bold"), fg="#333").grid(row=3, column=0, padx=5, pady=5)
        self.objetivo = ttk.Combobox(form, values=["Ganhar Massa", "Perder Peso"])
        self.objetivo.grid(row=3, column=1, padx=5, pady=5)
        self.objetivo.set("Objetivo")

        # Botões de ação
        botoes = tk.Frame(self, bg="#EAF4F4")
        botoes.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        botoes.grid_columnconfigure(0, weight=1)

        ttk.Button(botoes, text="⬅ Voltar",
                   command=lambda: app.show_frame("Inicio")).grid(row=0, column=0, sticky="w")
        ttk.Button(botoes, text="➕ Adicionar", command=self.adicionar,
                   style="Add.TButton").grid(row=0, column=1, padx=5)
        ttk.Button(botoes, text="🗑 Apagar Cliente", command=self.apagar,
                   style="Delete.TButton").grid(row=0, column=2, padx=5)
        ttk.Button(botoes, text="🔄 Atualizar", command=self.atualizar).grid(row=0, column=3, sticky="e")

        # Carregar dados iniciais
        self.atualizar()

    def adicionar(self):
        # Valida os campos e adiciona um novo cliente à base de dados

        # Validar idade e peso (devem ser números)
        try:
            idade = int(self.idade.get())
            peso = float(self.peso.get())
        except:
            messagebox.showerror("Erro", "Valores inválidos")
            return

        nome = self.nome.get().strip()
        objetivo = self.objetivo.get().strip()

        # Verificar se o objetivo foi selecionado
        if objetivo == "Objetivo":
            messagebox.showerror("Erro", "Seleciona um objetivo")
            return

        # Verificar se o nome não está vazio
        if not nome:
            messagebox.showerror("Erro", "Nome vazio")
            return

        # Criar e guardar o novo cliente
        clientes = gd.ler_cliente()
        novo_id = gerar_id(clientes)
        cliente = Cliente(novo_id, nome, idade, peso, objetivo)
        gd.guardar_cliente(cliente)

        # Limpar campos após adicionar
        self.nome.delete(0, tk.END)
        self.idade.set("Idade")
        self.peso.set("Peso")
        self.objetivo.set("Objetivo")

        self.atualizar()

    def apagar(self):
        # Remove o cliente selecionado da base de dados
        selecionado = self.lista.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Nenhum cliente selecionado")
            return

        # Obter ID do cliente selecionado
        item = self.lista.item(selecionado)
        id_cliente = item["values"][0]

        # Filtrar a lista removendo o cliente com o ID indicado
        clientes = gd.ler_cliente()
        clientes = [c for c in clientes if c["id"] != id_cliente]
        gd.guardar_ficheiro("dados/clientes.json", clientes)

        self.atualizar()

    def atualizar(self):
        # Recarrega a tabela com os dados mais recentes dos clientes
        self.lista.delete(*self.lista.get_children())
        for c in gd.ler_cliente():
            self.lista.insert("", "end", values=(
                c["id"], c["nome"], c["idade"], c["peso"], c["objetivo"]
            ))


# ---------- GESTÃO DE PLANOS DE TREINO ----------

class PlanosFrame(tk.Frame):
    # Interface para gerar, visualizar e apagar planos de treino
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # Título
        tk.Label(self, text="📋 Planos", font=("Segoe UI", 22, "bold"),
                 bg="#EAF4F4", fg="#2F5061").grid(row=0, column=0, pady=10)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Tabela de planos
        self.lista = ttk.Treeview(
            self, columns=("ID", "Cliente", "Objetivo", "Exercícios", "Dias"), show="headings")

        for col, w in [("ID", 40), ("Cliente", 140), ("Objetivo", 120),
                       ("Exercícios", 200), ("Dias", 60)]:
            self.lista.heading(col, text=col)
            self.lista.column(col, width=w, anchor="center")

        self.lista.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        # Formulário para gerar plano
        form = tk.Frame(self, bg="#EAF4F4")
        form.grid(row=2, column=0, pady=10)

        # Selecionar cliente
        tk.Label(form, text="Cliente", bg="#EAF4F4",
                 font=("Segoe UI", 10, "bold"), fg="#333").grid(row=0, column=0, padx=5, pady=5)
        self.entry_cliente = ttk.Combobox(form, state="readonly")
        self.entry_cliente.grid(row=0, column=1, padx=5, pady=5)

        # Selecionar objetivo
        tk.Label(form, text="Objetivo", bg="#EAF4F4",
                 font=("Segoe UI", 10, "bold"), fg="#333").grid(row=1, column=0, padx=5, pady=5)
        self.objetivo = ttk.Combobox(form, values=["Ganhar Massa", "Perder Peso"], state="readonly")
        self.objetivo.grid(row=1, column=1, padx=5, pady=5)
        self.objetivo.current(0)

        # Selecionar número de dias por semana
        tk.Label(form, text="Dias", bg="#EAF4F4",
                 font=("Segoe UI", 10, "bold"), fg="#333").grid(row=2, column=0, padx=5, pady=5)
        self.dias = ttk.Combobox(form, values=["1","2","3","4","5","6","7"], state="readonly")
        self.dias.grid(row=2, column=1, padx=5, pady=5)
        self.dias.current(2)  # Valor padrão: 3 dias

        # Botões
        botoes = tk.Frame(self, bg="#EAF4F4")
        botoes.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        botoes.grid_columnconfigure(0, weight=1)

        ttk.Button(botoes, text="⬅ Voltar",
                   command=lambda: self.app.show_frame("Inicio")).grid(row=0, column=0, sticky="w")
        ttk.Button(botoes, text="➕ Gerar Plano", command=self.gerar,
                   style="Add.TButton").grid(row=0, column=1, padx=5)
        ttk.Button(botoes, text="🗑 Apagar Plano", command=self.apagar,
                   style="Delete.TButton").grid(row=0, column=2, sticky="e", padx=5)
        ttk.Button(botoes, text="🔄 Atualizar", command=self.atualizar).grid(row=0, column=3, padx=5)

        self.atualizar()

    def parse_cliente(self, texto):
        # Extrai o ID do cliente a partir do texto Nome (ID)
        try:
            return int(texto.split("(")[-1].replace(")", "").strip())
        except:
            return None

    def carregar_clientes(self):
        # Carrega os clientes existentes para a Combobox
        clientes = gd.ler_cliente()
        valores = [f"{c['nome']} ({c['id']})" for c in clientes if isinstance(c, dict)]
        self.entry_cliente["values"] = valores
        if valores:
            self.entry_cliente.set(valores[0])
        else:
            self.entry_cliente.set("Sem clientes")

    def limpar_orfaos(self):
        # Remove planos cujo cliente já não existe (dados órfãos)
        clientes = gd.ler_cliente()
        ids_validos = {int(c["id"]) for c in clientes if isinstance(c, dict)}
        planos = gd.ler_plano()
        planos = [p for p in planos if int(p.get("id_cliente")) in ids_validos]
        gd.guardar_ficheiro("dados/planos.json", planos)

    def gerar_exercicios(self, objetivo, dias):
        # Gera uma lista aleatória de exercícios conforme o objetivo e número de dias
        EXERCICIOS = {
            "forca": ["Supino", "Agachamento", "Flexões"],
            "cardio": ["Corrida", "Bicicleta", "Corda"],
            "core": ["Abdominais", "Prancha"]
        }

        objetivo = objetivo.lower()

        # Definir categorias de exercícios conforme o objetivo
        if "massa" in objetivo:
            cats = ["forca"]
        elif "peso" in objetivo:
            cats = ["cardio"]
        else:
            cats = ["forca", "cardio", "core"]

        # Juntar todos os exercícios das categorias escolhidas
        pool = []
        for c in cats:
            pool.extend(EXERCICIOS[c])

        # Selecionar aleatoriamente alguns exercícios
        quantidade = min(2 + int(dias) // 2, len(pool))
        return random.sample(pool, quantidade)

    def atualizar(self):
        # Atualiza a tabela de planos e a lista de clientes
        self.limpar_orfaos()
        self.carregar_clientes()

        self.lista.delete(*self.lista.get_children())
        for p in gd.ler_plano():
            self.lista.insert("", "end", values=(
                p.get("id"), p.get("id_cliente"), p.get("objetivo"),
                ", ".join(p.get("lista_exercicios", [])), p.get("dias_semana"),
            ))

    def gerar(self):
        # Cria um novo plano de treino para o cliente selecionado
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
        # Remove o plano selecionado
        sel = self.lista.selection()
        if not sel:
            return
        id_plano = self.lista.item(sel)["values"][0]
        planos = gd.ler_plano()
        planos = [p for p in planos if p.get("id") != id_plano]
        gd.guardar_ficheiro("dados/planos.json", planos)
        self.atualizar()


# ---------- GESTÃO DE SESSÕES DE TREINO ----------

class SessoesFrame(tk.Frame):
    # Interface para registar e visualizar sessões de treino dos clientes
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # Título
        tk.Label(self, text="🏋️ Sessões", font=("Segoe UI", 22, "bold"),
                 bg="#EAF4F4", fg="#2F5061").grid(row=0, column=0, pady=10)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Tabela de sessões
        self.lista = ttk.Treeview(
            self, columns=("ID", "Cliente", "Data", "Duração"), show="headings")

        for col, w in [("ID", 60), ("Cliente", 120), ("Data", 120), ("Duração", 80)]:
            self.lista.heading(col, text=col)
            self.lista.column(col, width=w, anchor="center")

        self.lista.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        # Formulário para registar sessão
        form = tk.Frame(self, bg="#EAF4F4")
        form.grid(row=2, column=0, pady=10)

        # Selecionar cliente
        tk.Label(form, text="Cliente", bg="#EAF4F4",
                 font=("Segoe UI", 10, "bold"), fg="#333").grid(row=0, column=0, padx=5, pady=5)
        self.id_cliente = ttk.Combobox(form, state="readonly")
        self.id_cliente.grid(row=0, column=1, padx=5, pady=5)

        # Selecionar data (últimos 30 dias + próximos 30 dias)
        tk.Label(form, text="Data", bg="#EAF4F4",
                 font=("Segoe UI", 10, "bold"), fg="#333").grid(row=1, column=0, padx=5, pady=5)
        self.data = ttk.Combobox(form, state="readonly")
        self.data.grid(row=1, column=1, padx=5, pady=5)

        # Selecionar duração em minutos
        tk.Label(form, text="Duração", bg="#EAF4F4",
                 font=("Segoe UI", 10, "bold"), fg="#333").grid(row=2, column=0, padx=5, pady=5)
        self.duracao = ttk.Combobox(form, values=[30,45,60,75,90,120], state="readonly")
        self.duracao.grid(row=2, column=1, padx=5, pady=5)
        self.duracao.current(2)  # Valor padrão: 60 minutos

        # Botões
        botoes = tk.Frame(self, bg="#EAF4F4")
        botoes.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        botoes.grid_columnconfigure(0, weight=1)

        ttk.Button(botoes, text="⬅ Voltar",
                   command=lambda: self.app.show_frame("Inicio")).grid(row=0, column=0, sticky="w")
        ttk.Button(botoes, text="➕ Adicionar", command=self.adicionar,
                   style="Add.TButton").grid(row=0, column=1, padx=5)
        ttk.Button(botoes, text="🗑 Apagar", command=self.apagar,
                   style="Delete.TButton").grid(row=0, column=2, sticky="e", padx=5)
        ttk.Button(botoes, text="🔄 Atualizar", command=self.atualizar).grid(row=0, column=3, padx=5)

        self.atualizar()

    def gerar_datas(self):
        # Gera uma lista de 61 datas (30 dias antes e 30 depois de hoje)
        hoje = date.today()
        return [(hoje + timedelta(days=i)).isoformat() for i in range(-30, 31)]

    def carregar_clientes(self):
        # Carrega os clientes para a Combobox
        clientes = gd.ler_cliente()
        valores = [f"{c['nome']} ({c['id']})" for c in clientes if isinstance(c, dict)]
        self.id_cliente["values"] = valores
        if valores:
            self.id_cliente.set(valores[0])
        else:
            self.id_cliente.set("Sem clientes")

    def carregar_datas(self):
        # Carrega as datas disponíveis para a Combobox
        datas = self.gerar_datas()
        self.data["values"] = datas
        self.data.current(30)  # Data padrão: hoje

    def limpar_orfaos(self):
        # Remove sessões cujo cliente já não existe
        clientes = gd.ler_cliente()
        ids_validos = {int(c["id"]) for c in clientes if isinstance(c, dict)}
        sessoes = gd.ler_sessao()
        sessoes = [s for s in sessoes if int(s.get("id_cliente")) in ids_validos]
        gd.guardar_ficheiro("dados/sessoes.json", sessoes)

    def atualizar(self):
        # Atualiza a tabela de sessões e as comboboxes
        self.limpar_orfaos()
        self.carregar_clientes()
        self.carregar_datas()

        self.lista.delete(*self.lista.get_children())
        for s in gd.ler_sessao():
            self.lista.insert("", "end", values=(
                s.get("id"), s.get("id_cliente"), s.get("data"), s.get("duracao")
            ))

    def adicionar(self):
        # Regista uma nova sessão de treino
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
        # Remove a sessão selecionada
        sel = self.lista.selection()
        if not sel:
            return
        id_sessao = self.lista.item(sel)["values"][0]
        sessoes = gd.ler_sessao()
        sessoes = [s for s in sessoes if s.get("id") != id_sessao]
        gd.guardar_ficheiro("dados/sessoes.json", sessoes)
        self.atualizar()


# ---------- ESTATÍSTICAS E SIMULAÇÃO ----------

class EstatisticasFrame(tk.Frame):
    # Ecrã que mostra estatísticas e permite simular progresso dos clientes
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # Título
        tk.Label(self, text="📊 Estatísticas", font=("Segoe UI", 22, "bold"),
                 bg="#EAF4F4", fg="#2F5061").pack(pady=10)

        # Label onde vão aparecer os resultados
        self.label = tk.Label(self, text="", justify="left",
                              bg="#EAF4F4", font=("Segoe UI", 11), fg="#333")
        self.label.pack(pady=10)

        # Botões
        ttk.Button(self, text="🔄 Atualizar", command=self.calcular).pack(pady=5)
        ttk.Button(self, text="📈 Simular Progresso", command=self.simular_progresso,
                   style="Add.TButton").pack(pady=5)
        ttk.Button(self, text="⬅ Voltar",
                   command=lambda: app.show_frame("Inicio")).pack(pady=5)

    def calcular(self):
        # Calcula e mostra estatísticas: cliente mais/menos ativo, exercício comum, pesos
        clientes = gd.ler_cliente()
        sessoes = gd.ler_sessao()
        planos = gd.ler_plano()

        if not clientes:
            self.label.config(text="Sem dados")
            return
        if not sessoes:
            self.label.config(text="Sem sessões")
            return

        # Contar quantas sessões cada cliente fez
        contagem = Counter([s["id_cliente"] for s in sessoes])
        mais_ativo_id = max(contagem, key=contagem.get)  # Cliente com mais sessões
        menos_ativo_id = min(contagem, key=contagem.get)  # Cliente com menos sessões

        clientes_dict = {c["id"]: c for c in clientes}

        # Descobrir o exercício mais comum em todos os planos
        mais_comum = "N/A"
        exercicios = []
        for p in planos:
            exercicios.extend(p.get("lista_exercicios", []))
        if exercicios:
            mais_comum = Counter(exercicios).most_common(1)[0][0]

        # Construir texto com as estatísticas
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
        # Simula a evolução do peso dos clientes com base no plano e nas sessões.
        # Clientes com objetivo 'Ganhar Massa' aumentam de peso.
        # Clientes com objetivo 'Perder Peso' diminuem de peso.

        clientes = gd.ler_cliente()
        sessoes = gd.ler_sessao()
        planos = gd.ler_plano()

        # Mapear plano por cliente
        plano_por_cliente = {p["id_cliente"]: p for p in planos}

        # Calcular horas totais de treino por cliente
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

                # Ajustar peso conforme objetivo
                if "massa" in objetivo:
                    peso += treino * 0.2 + dias * 0.1
                elif "perder" in objetivo:
                    peso -= treino * 0.2 + dias * 0.1

            # Garantir peso mínimo de 40 kg
            if peso < 40:
                peso = 40

            c["peso"] = round(peso, 1)
            novos_clientes.append(c)

        # Guardar alterações e atualizar ecrã
        gd.guardar_ficheiro("dados/clientes.json", novos_clientes)
        self.calcular()


# ---------- APLICAÇÃO PRINCIPAL ----------

class App(tk.Tk):
    # Classe principal que gere a janela e a navegação entre ecrãs.
    def __init__(self):
        super().__init__()

        # Configuração da janela
        self.title("Gestor de Ginásio")
        self.geometry("900x600")
        self.configure(bg="#EAF4F4")

        # ---------- ESTILOS VISUAIS ----------
        style = ttk.Style()
        style.theme_use("clam")  # Tema 

        # Estilo da tabela
        style.configure("Treeview", background="white", foreground="#222",
                        rowheight=28, fieldbackground="white", borderwidth=0,
                        font=("Arial", 10))
        style.configure("Treeview.Heading", background="#4F6D7A",
                        foreground="white", font=("Arial", 10, "bold"), relief="flat")
        style.map("Treeview", background=[("selected", "#A7D3F2")])

        # Estilo base dos botões
        style.configure("TButton", font=("Arial", 10, "bold"), padding=6)

        # Estilo do botão "Adicionar" (verde)
        style.configure("Add.TButton", font=("Arial", 10, "bold"), padding=6,
                        background="#81C784", foreground="white")
        style.map("Add.TButton", background=[("active", "#66BB6A")])

        # Estilo do botão "Apagar" (vermelho)
        style.configure("Delete.TButton", font=("Arial", 10, "bold"), padding=6,
                        background="#E57373", foreground="white")
        style.map("Delete.TButton", background=[("active", "#EF5350")])

        # Estilo das comboboxes
        style.configure("TCombobox", padding=4)

        # ---------- CONTAINER PARA OS ECRÃS ----------
        container = tk.Frame(self, bg="#EAF4F4")
        container.pack(fill="both", expand=True, padx=15, pady=15)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dicionário para guardar todos os ecrãs
        self.frames = {}

        # Criar e registar cada ecrã da aplicação
        for F, name in [
            (InicioFrame, "Inicio"),
            (ClientesFrame, "Clientes"),
            (PlanosFrame, "Planos"),
            (SessoesFrame, "Sessoes"),
            (EstatisticasFrame, "Estatisticas")
        ]:
            frame = F(container, self)
            frame.configure(bg="#EAF4F4")
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Mostrar ecrã inicial
        self.show_frame("Inicio")

    def show_frame(self, nome):
        # Levanta (mostra) o ecrã com o nome indicado.
        self.frames[nome].tkraise()


# ---------- APP ----------
if __name__ == "__main__":
    app = App()
    app.mainloop()