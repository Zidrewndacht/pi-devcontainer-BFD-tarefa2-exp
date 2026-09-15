import requests

BASE_URL = "https://parallelum.com.br/fipe/api/v1"
TIMEOUT = 3000

def get_marcas(tipo):
    resp = requests.get(f"{BASE_URL}/{tipo}/marcas", timeout=TIMEOUT)
    return resp.json() if resp.status_code == 200 else []

def get_modelos(tipo, cod_marca):
    resp = requests.get(f"{BASE_URL}/{tipo}/marcas/{cod_marca}/modelos", timeout=TIMEOUT)
    return resp.json().get("modelos", []) if resp.status_code == 200 else []

def get_anos(tipo, cod_marca, cod_modelo):
    resp = requests.get(f"{BASE_URL}/{tipo}/marcas/{cod_marca}/modelos/{cod_modelo}/anos", timeout=TIMEOUT)
    return resp.json() if resp.status_code == 200 else []

def get_valor(cod_fipe):
    resp = requests.get(f"{BASE_URL}/veiculos/{cod_fipe}", timeout=TIMEOUT)
    return resp.json() if resp.status_code == 200 else {}