import re
import unicodedata


UFS = {
    "AC": "Acre",
    "AL": "Alagoas",
    "AP": "Amapá",
    "AM": "Amazonas",
    "BA": "Bahia",
    "CE": "Ceará",
    "DF": "Distrito Federal",
    "ES": "Espírito Santo",
    "GO": "Goiás",
    "MA": "Maranhão",
    "MT": "Mato Grosso",
    "MS": "Mato Grosso do Sul",
    "MG": "Minas Gerais",
    "PA": "Pará",
    "PB": "Paraíba",
    "PR": "Paraná",
    "PE": "Pernambuco",
    "PI": "Piauí",
    "RJ": "Rio de Janeiro",
    "RN": "Rio Grande do Norte",
    "RS": "Rio Grande do Sul",
    "RO": "Rondônia",
    "RR": "Roraima",
    "SC": "Santa Catarina",
    "SP": "São Paulo",
    "SE": "Sergipe",
    "TO": "Tocantins",
}


def normalizar_nome(nome: str) -> str:
    sem_acentos = unicodedata.normalize("NFKD", nome)
    texto = "".join(
        caractere for caractere in sem_acentos if not unicodedata.combining(caractere)
    )
    return re.sub(r"\s+", " ", texto.strip().casefold())


def validar_uf(uf: str) -> str:
    sigla = uf.strip().upper()
    if sigla not in UFS:
        raise ValueError("Informe uma sigla de UF válida.")
    return sigla


def validar_nome(nome: str) -> str:
    texto = re.sub(r"\s+", " ", nome.strip())
    if len(texto) < 2 or not any(caractere.isalpha() for caractere in texto):
        raise ValueError("Informe um nome de município válido.")
    return texto


def validar_raio(valor: str) -> float:
    try:
        raio = float(valor.replace(",", "."))
    except ValueError as erro:
        raise ValueError("Informe um raio numérico válido.") from erro
    if raio <= 0 or raio > 5000:
        raise ValueError("O raio deve ser maior que zero e menor ou igual a 5.000 km.")
    return raio
