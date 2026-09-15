from dateutil.parser import parse
from datetime import datetime
from datetime import timedelta


def gerar_intervalo(inicio, fim):
    datas = []

    atual = inicio

    while atual <= fim:
        datas.append(atual)
        atual += timedelta(days=1)

    return datas


def eh_dia_util(data):
    return data.weekday() < 5

def dias_restantes(data):
    hoje = datetime.today().date()
    return (data.date() - hoje).days


def dias_diferenca(data):
    hoje = datetime.today().date()
    return (data.date() - hoje).days


def fim_de_semana(data):
    return data.weekday() >= 5


def converter_data(data_str):
    return parse(data_str, dayfirst=True)


def dia_da_semana(data):
    dias = [
        "Segunda-feira",
        "Terça-feira",
        "Quarta-feira",
        "Quinta-feira",
        "Sexta-feira",
        "Sábado",
        "Domingo"
    ]

    return dias[data.weekday()]