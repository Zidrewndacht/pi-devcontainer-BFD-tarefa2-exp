from models import Municipio


def gerar_mapa(municipios: list[Municipio], largura: int = 60, altura: int = 20) -> str:
    if not municipios:
        raise ValueError("Não há municípios sincronizados para gerar o mapa.")
    latitudes = [municipio.latitude for municipio in municipios]
    longitudes = [municipio.longitude for municipio in municipios]
    menor_latitude, maior_latitude = min(latitudes), max(latitudes)
    menor_longitude, maior_longitude = min(longitudes), max(longitudes)
    intervalo_latitude = maior_latitude - menor_latitude or 1
    intervalo_longitude = maior_longitude - menor_longitude or 1
    grade = [[" " for _ in range(largura)] for _ in range(altura)]
    for municipio in municipios:
        x = round(
            (municipio.longitude - menor_longitude)
            / intervalo_longitude
            * (largura - 1)
        )
        y = round(
            (maior_latitude - municipio.latitude) / intervalo_latitude * (altura - 1)
        )
        grade[y][x] = "#" if grade[y][x] != " " else "*"
    borda = "+" + "-" * largura + "+"
    linhas = [borda]
    linhas.extend("|" + "".join(linha) + "|" for linha in grade)
    linhas.append(borda)
    linhas.append("* município  # dois ou mais municípios na mesma posição")
    linhas.append(
        f"Latitude: {menor_latitude:.4f} a {maior_latitude:.4f} | "
        f"Longitude: {menor_longitude:.4f} a {maior_longitude:.4f}"
    )
    return "\n".join(linhas)
