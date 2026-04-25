import os
import json
from modelos_de_dados import *

##################################### Funcoes gerais

def guardar_ficheiro(nome_ficheiro, dados):
    with open(nome_ficheiro, "w") as f:
        json.dump(dados, f, indent=4)

def ler_ficheiro(nome_ficheiro):
    with open(nome_ficheiro, "r") as f:
        return json.load(f)

###################################### Clientes

def guardar_cliente(cliente):
    dados = ler_ficheiro("dados/clientes.json")
    dados.append(cliente.__dict__)
    guardar_ficheiro("dados/clientes.json", dados)

def ler_cliente():
    dados = ler_ficheiro("dados/clientes.json")
    return dados

###################################### Planos


def guardar_plano(plano):
    dados = ler_ficheiro("dados/planos.json")
    dados.append(plano.__dict__)
    guardar_ficheiro("dados/planos.json", dados)

def ler_plano():
    dados = ler_ficheiro("dados/planos.json")
    return dados


###################################### Sessoes


def guardar_sessao(sessao):
    dados = ler_ficheiro("dados/sessoes.json")
    dados.append(sessao.__dict__)
    guardar_ficheiro("dados/sessoes.json", dados)

def ler_sessao():
    dados = ler_ficheiro("dados/sessoes.json")
    return dados