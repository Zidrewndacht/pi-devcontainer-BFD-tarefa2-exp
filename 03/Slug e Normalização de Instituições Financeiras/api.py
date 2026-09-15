import requests

API_URL = "https://brasilapi.com.br/api/cvm/corretoras/v1"

def buscar_dados_api():
    """Consome a API da BrasilAPI e retorna uma lista de dicionários com as corretoras."""
    try:
        resposta = requests.get(API_URL, timeout=10)
        resposta.raise_for_status() 
        return resposta.json()
    except requests.RequestException as erro:
        print(f"Erro ao conectar com a API: {erro}")
        return []
