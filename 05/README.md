# GeoAtlas Brasil

Aplicação de terminal desenvolvida para o Trabalho 5 de bibliotecas externas em Python. O programa consulta municípios pela API de Localidades do IBGE, obtém coordenadas com `geopy`, armazena os resultados em SQLite e apresenta os dados com `rich`.

## Funcionalidades

- sincronização dos municípios de uma UF;
- cache local de coordenadas;
- busca por município e UF;
- cálculo de distância em quilômetros e milhas;
- classificação de municípios vizinhos;
- busca dentro de um raio;
- listagem e filtro dos dados salvos;
- fallback pelas coordenadas da capital;
- mapa ASCII;
- exportação CSV e JSON;
- processamento em lote;
- painel de estatísticas;
- configuração por JSON ou variáveis de ambiente;
- logging e testes automatizados.

## Instalação no Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

Se o PowerShell bloquear a ativação:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Instalação no Linux ou macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

## Arquivo em lote

Cada linha contém o nome do município e a UF separados por ponto e vírgula:

```text
Curitiba;PR
Londrina;PR
Maringá;PR
```

O projeto inclui um exemplo em `dados/exemplo_batch.txt`.

## Configuração

Os valores padrão ficam em `config.json`. É possível substituí-los por variáveis de ambiente com o prefixo `TAREFA5_`:

```powershell
$env:TAREFA5_UF_PADRAO="PR"
$env:TAREFA5_TIMEOUT="30"
python main.py
```

## Testes

```powershell
python -m pip install -r requirements-dev.txt
python -m ruff check .
python -m ruff format --check .
python -m compileall .
python -m coverage run --branch --source=. --omit=".venv/*,tests/*" -m unittest discover -s tests -v
python -m coverage report --fail-under=100
```

Os testes automatizados usam respostas simuladas. A validação final também deve incluir uma consulta real ao IBGE e ao Nominatim.

## Limite do Nominatim

O serviço público do Nominatim limita a frequência de consultas. O GeoAtlas Brasil realiza as geocodificações em sequência, aguarda entre as requisições e reutiliza dados salvos. A primeira sincronização de uma UF com muitos municípios pode levar vários minutos.
