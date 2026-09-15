import requests


def buscar_feriados(ano):
    url = f"https://brasilapi.com.br/api/feriados/v1/{ano}"

    resposta = requests.get(url)

    if resposta.status_code == 200:
        return resposta.json()

    return []