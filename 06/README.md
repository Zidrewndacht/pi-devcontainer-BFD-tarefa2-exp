# IBGE Nomes Analytics

> Uma ferramenta de linha de comando (CLI) para explorar o histórico, as tendências e a popularidade dos nomes próprios no Brasil.

O **IBGE Nomes Analytics** consome a API oficial do Censo Demográfico do IBGE, processa os dados históricos década a década e os apresenta em uma interface de terminal moderna e elegante. Além disso, conta com persistência local em **SQLite3** para criar rankings e consultas personalizadas offline.

---

##  O que o app faz?

* Análise de Tendência: Tabela detalhada década a década com indicadores visuais de subida ou descida de popularidade.
* Modo Comparativo: Gráficos de barras diretamente no terminal para comparar a força de dois nomes, calculando a diferença real e percentual entre eles.
* Cálculo de Prevalência: Descubra a raridade do nome (ex: *A cada 5.000 brasileiros, 1 se chama Victor*).
* Inteligência Offline: Armazenamento automático em banco de dados local para criar rankings personalizados de décadas e buscas por faixas de frequência.

---

## Pré-requisitos & Tecnologias

Para rodar este projeto, você precisará apenas do **Python 3** instalado em sua máquina. 

O ecossistema do projeto utiliza as seguintes bibliotecas:
* **[Rich](https://rich.readthedocs.io/):** Interface visual no terminal (tabelas, cores, menus e gráficos).
* **[Requests](https://requests.readthedocs.io/):** Comunicação com a API do IBGE.
* **[Humanize](https://python-humanize.readthedocs.io/):** Formatação de números grandes para leitura simplificada.
* **[SQLite3](https://docs.python.org/3/library/sqlite3.html):** Banco de dados relacional embutido.
