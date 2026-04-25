class Cliente:
    def __init__(self, id, nome, idade, peso, objetivo):
        self.id = id
        self.nome = nome
        self.idade = idade
        self.peso = peso
        self.objetivo = objetivo


class PlanoTreino:
    def __init__(self, id, id_cliente, objetivo, lista_exercicios, dias_semana):
        self.id = id
        self.id_cliente = id_cliente
        self.objetivo = objetivo
        self.lista_exercicios = lista_exercicios
        self.dias_semana = dias_semana


class SessaoTreino:
    def __init__(self, id, id_cliente, data, duracao):
        self.id = id
        self.id_cliente = id_cliente
        self.data = data
        self.duracao = duracao