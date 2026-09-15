import requests

# URL base da API FIPE (versão 2)
BASE_URL = "https://parallelum.com.br/fipe/api/v1"

def get_marcas(tipo):
    """Obtém lista de marcas para o tipo de veículo."""
    try:
        resp = requests.get(f"{BASE_URL}/{tipo}/marcas", timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"Erro ao buscar marcas: {e}")
        return []

def get_modelos(tipo, codigo_marca):
    """Obtém lista de modelos para uma marca."""
    try:
        resp = requests.get(f"{BASE_URL}/{tipo}/marcas/{codigo_marca}/modelos", timeout=10)
        resp.raise_for_status()
        return resp.json().get("modelos", [])
    except requests.RequestException as e:
        print(f"Erro ao buscar modelos: {e}")
        return []

def get_anos(tipo, codigo_marca, codigo_modelo):
    """Obtém lista de anos para um modelo."""
    try:
        resp = requests.get(f"{BASE_URL}/{tipo}/marcas/{codigo_marca}/modelos/{codigo_modelo}/anos", timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"Erro ao buscar anos: {e}")
        return []

def get_valor(tipo, codigo_marca, codigo_modelo, codigo_ano):
    """Obtém valor FIPE para um veículo específico."""
    try:
        resp = requests.get(f"{BASE_URL}/{tipo}/marcas/{codigo_marca}/modelos/{codigo_modelo}/anos/{codigo_ano}", timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"Erro ao buscar valor: {e}")
        return {}

def main():
    print("=== Consulta FIPE ===")
    tipo = input("Tipo de veículo (carros, motos, caminhoes): ").strip().lower()

    # Lista marcas
    marcas = get_marcas(tipo)
    if not marcas:
        return
    for m in marcas:
        print(f"{m['codigo']} - {m['nome']}")
    codigo_marca = input("Digite o código da marca: ").strip()

    # Lista modelos
    modelos = get_modelos(tipo, codigo_marca)
    if not modelos:
        return
    for m in modelos:
        print(f"{m['codigo']} - {m['nome']}")
    codigo_modelo = input("Digite o código do modelo: ").strip()

    # Lista anos
    anos = get_anos(tipo, codigo_marca, codigo_modelo)
    if not anos:
        return
    for a in anos:
        print(f"{a['codigo']} - {a['nome']}")
    codigo_ano = input("Digite o código do ano: ").strip()

    # Busca valor
    valor = get_valor(tipo, codigo_marca, codigo_modelo, codigo_ano)
    if valor:
        print("\n=== Resultado ===")
        print(f"Modelo: {valor.get('Modelo')}")
        print(f"Ano: {valor.get('AnoModelo')}")
        print(f"Combustível: {valor.get('Combustivel')}")
        print(f"Valor FIPE: {valor.get('Valor')}")
        print(f"Código FIPE: {valor.get('CodigoFipe')}")
    else:
        print("Não foi possível obter o valor.")

if __name__ == "__main__":
    main()
