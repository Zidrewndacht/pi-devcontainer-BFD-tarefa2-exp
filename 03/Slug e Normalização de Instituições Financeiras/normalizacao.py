import re
from slugify import slugify

def gerar_slug(nome):
    """Gera o slug amigável usando a biblioteca-tempero python-slugify."""
    return slugify(nome)

def limpar_nome(nome):
    """Remove sufixos corporativos comuns de forma insensível a maiúsculas/minúsculas

    e elimina espaços extras resultantes da limpeza.
    """
    sufixos = [
        r"\bS\.A\.\b",
        r"\bS/A\b",
        r"\bSA\b",
        r"\bLTDA\b",
        r"\bLIMITADA\b"
    ]
    
    nome_limpo = nome
    
    for sufixo in sufixos:
        nome_limpo = re.sub(sufixo, "", nome_limpo, flags=re.IGNORECASE)
    
    nome_limpo = " ".join(nome_limpo.split())
    
    return nome_limpo

def comparar_nomes(nome1, nome2):
    """Gera o slug de ambos e informa se são idênticos."""
    return gerar_slug(nome1) == gerar_slug(nome2)
