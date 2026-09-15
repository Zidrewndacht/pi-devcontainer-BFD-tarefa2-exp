# Especificação de Exercício: Bibliotecas Externas em Python

## 1. Requisitos Técnicos Gerais (obrigatórios para todos os trabalhos)

Cada dupla deve produzir uma aplicação executável no terminal que atenda aos seguintes requisitos estruturais:

- **Ambiente virtual**: o projeto deve ser desenvolvido dentro de um `venv`. O diretório do ambiente pode ser incluído no `.gitignore`.
- **Dependências**: todas as bibliotecas de terceiros (incluindo `requests`, `rich` e a biblioteca-tempero atribuída) devem ser listadas em um arquivo `requirements.txt` funcional. Deve ser possível recriar o ambiente com `pip install -r requirements.txt`.
- **Organização modular**: o código deve estar dividido em múltiplos arquivos `.py`. Pelo menos um módulo deve conter funções reutilizáveis, e o ponto de entrada da aplicação deve ser protegido por `if __name__ == "__main__":`.
- **Imports**: o código deve demonstrar import de built-ins, import de arquivos locais (módulos do próprio projeto) e import de bibliotecas remotas instaladas via `pip`.
- **Estruturas de dados**: o uso de **dicionários** é obrigatório em pelo menos uma etapa do fluxo de dados. Listas, tuplas e/ou sets podem ser usados livremente quando convenientes.
- **Lógica de programação**: o código deve empregar condicionais, loops, operadores lógicos e aritméticos de forma significativa.
- **Funções**: a lógica deve ser fragmentada em funções com responsabilidades definidas. Evite scripts monolíticos.
- **Persistência**: todos os trabalhos devem usar **SQLite** para armazenar e consultar dados. O banco pode ser um arquivo `.db` local.
- **APIs HTTP**: a aquisição de dados externos deve ser feita exclusivamente via `requests.get()` (ou `.post()` quando a API exigir) contra APIs públicas. APIs brasileiras são preferenciais, mas não obrigatórias.
- **Exibição**: toda a apresentação de dados no terminal deve usar a biblioteca `rich` (tabelas, painéis, cores, progresso, etc.). Evite `print()` simples para saída final de dados estruturados.
- **Fluxo obrigatório**: o esqueleto lógico esperado é:
  ```
  venv → pip install → requirements.txt
      ↓
  requests.get() → dicionário
      ↓
  normalizar / validar / enriquecer (biblioteca-tempero)
      ↓
  SQLite (salvar / consultar)
      ↓
  rich (exibir no terminal)
  ```

> **Restrição importante**: esta especificação descreve **O QUE** o sistema deve fazer e **COMO** deve se comportar em relação às escolhas do usuário. **NÃO descreve COMO implementar no código**. As decisões de implementação (nomes de funções, estruturas internas, algoritmos, tratamento de exceções, etc.) são de responsabilidade exclusiva da dupla.

---

## Trabalho 1 — Gestão de Feriados Nacionais
**Biblioteca-tempero:** `python-dateutil`  
**API sugerida:** `https://brasilapi.com.br/api/feriados/v1/{ano}`

### Descrição geral
Aplicação terminal que consulta feriados nacionais, armazena localmente e permite operações de calendário. A biblioteca `python-dateutil` deve ser usada para interpretar entradas de data em formatos variados, calcular intervalos e manipular objetos de data.

### Menu inicial e comportamento

1. **Consultar e armazenar feriados de um ano**  
   - Solicita ao usuário um ano (quatro dígitos).  
   - Consulta a API.  
   - Cada feriado retornado deve ser processado pela biblioteca-tempero para garantir um objeto de data consistente.  
   - Armazena em SQLite: ano, data, nome do feriado, tipo e dia da semana.  
   - Deve informar ao usuário quantos feriados foram inseridos e quantos já existiam no banco (evitando duplicatas).  
   - Exibe um resumo em tabela `rich`.

2. **Verificar status de uma data**  
   - Solicita uma data ao usuário. A aplicação deve aceitar múltiplos formatos de entrada (ex: `25/12/2026`, `2026-12-25`, `25 de dezembro de 2026`).  
   - Usa a biblioteca-tempero para interpretar a entrada independentemente do formato.  
   - Consulta o SQLite. Informa se a data é feriado (mostrando o nome), fim de semana ou dia útil.  
   - Se for feriado, calcula e exibe quantos dias faltam (se futuro) ou quantos se passaram (se passado).

3. **Próximos feriados**  
   - Solicita um número `N`.  
   - A partir da data atual (ou de uma data informada opcionalmente pelo usuário), lista os próximos `N` feriados presentes no banco.  
   - Exibe: nome, data, dia da semana e dias restantes. A contagem de dias deve usar a biblioteca-tempero.

4. **Dias úteis entre duas datas**  
   - Solicita data inicial e final (com parse flexível).  
   - Calcula quantos dias úteis existem no intervalo, descontando feriados cadastrados no SQLite e fins de semana.  
   - Exibe o total de dias úteis e, em uma lista secundária, os feriados que ocorreram dentro do período.

5. **Listar feriados armazenados**  
   - Exibe todos os feriados do banco em uma tabela `rich`.  
   - Permite filtrar por ano antes de exibir.

### Tarefas bônus
- Permitir que o usuário cadastre manualmente feriados municipais ou estaduais, que também devem ser considerados no cálculo de dias úteis.
- Gerar uma representação em texto ASCII do calendário do mês atual, destacando os feriados.
- Implementar um "alerta de proximidade" que, ao iniciar a aplicação, informe automaticamente se existe algum feriado nos próximos 7 dias.

---

## Trabalho 2 — Validação e Formatação de Telefones Brasileiros
**Biblioteca-tempero:** `phonenumbers`  
**API sugerida:** `https://brasilapi.com.br/api/ddd/v1/{ddd}`

### Descrição geral
Aplicação que valida, formata e enriquece números de telefone brasileiros. A biblioteca `phonenumbers` deve ser usada para parsear números em diversos formatos, determinar tipo (fixo/móvel), validar e formatar para padrões nacional e internacional.

### Menu inicial e comportamento

1. **Validar e formatar número**  
   - Solicita um número de telefone (com ou sem DDD, com ou sem `+55`, com ou sem máscara).  
   - Usa a biblioteca-tempero para parsear e validar.  
   - Determina se é fixo ou móvel.  
   - Exibe: número formatado no padrão nacional, número formatado no padrão internacional, tipo e status de validade.  
   - Armazena no SQLite com timestamp da consulta.

2. **Consultar DDD**  
   - Solicita um DDD (dois dígitos).  
   - Consulta a API para obter estado e lista de cidades.  
   - Usa a biblioteca-tempero para validar se o DDD informado é plausível no contexto brasileiro.  
   - Armazena no SQLite: DDD, estado, lista de cidades (pode ser serializada).  
   - Exibe em tabela `rich`: estado, quantidade de cidades e as cidades associadas.

3. **Gerar números válidos por região**  
   - Solicita um estado (UF) ou um DDD.  
   - Se informado UF, consulta a API para descobrir os DDDs daquele estado.  
   - Gera uma quantidade informada de números de telefone fictícios, mas semanticamente válidos para aquela região, usando a biblioteca-tempero.  
   - Armazena no SQLite marcando como `ficticio = 1`.  
   - Exibe em tabela `rich`.

4. **Buscar histórico**  
   - Lista todos os números consultados ou gerados armazenados no SQLite.  
   - Permite filtro por tipo (fixo/móvel/fictício) ou por estado.  
   - Exibe em tabela `rich` com todas as colunas relevantes.

5. **Comparar dois números**  
   - Solicita dois números em formatos possivelmente diferentes.  
   - Usa a biblioteca-tempero para extrair a representação canônica de cada um.  
   - Informa se são equivalentes (mesmo número apesar da formatação diferente) ou distintos.

### Tarefas bônus
- Implementar uma "lista de bloqueio" local: se um número estiver cadastrado em uma tabela de reclamações (inseridas manualmente pelo usuário), a aplicação deve alertar ao consultá-lo.
- Calcular um "custo de ligação" simulado: fixo-para-fixo mesmo DDD = gratuito; fixo-para-móvel = tarifa X; DDD diferente = tarifa Y; exibir o custo ao comparar origem e destino.
- Gerar um arquivo de contato no formato vCard (`.vcf`) contendo um número válido gerado, pronto para importação.

---

## Trabalho 3 — Slug e Normalização de Instituições Financeiras
**Biblioteca-tempero:** `python-slugify`  
**API sugerida:** `https://brasilapi.com.br/api/cvm/corretoras/v1`

### Descrição geral
Aplicação que consulta a lista de corretoras de valores, normaliza seus nomes criando slugs amigáveis a URLs e permite buscas e categorizações. A biblioteca `python-slugify` deve ser usada para converter nomes com acentos, espaços e símbolos em strings ASCII lowercase separadas por hífen.

### Menu inicial e comportamento

1. **Sincronizar e slugificar instituições**  
   - Consulta a API de corretoras.  
   - Para cada instituição retornada, gera um slug do nome usando a biblioteca-tempero.  
   - Armazena no SQLite: código, nome original, slug, CNPJ e status.  
   - Informa o total sincronizado e quantos nomes continham caracteres que precisaram de normalização.  
   - Exibe uma tabela `rich` com as 10 primeiras instituições e seus slugs.

2. **Buscar por slug**  
   - Solicita um termo de busca.  
   - Busca no SQLite por slugs que contenham o termo informado.  
   - Exibe resultados em tabela `rich`. Se não houver correspondência exata, lista os slugs mais próximos lexicograficamente que existam no banco.

3. **Normalizar nome inserido**  
   - Solicita um nome digitado livremente pelo usuário (pode conter acentos, espaços duplos, caixa alta/baixa, sufixos como S.A., LTDA).  
   - Usa a biblioteca-tempero para gerar o slug.  
   - Exibe: nome original, slug gerado e uma versão "limpa" sem sufixos corporativos (inferida via lógica própria da dupla).

4. **Comparar nomes**  
   - Solicita dois nomes de institções.  
   - Gera o slug de ambos usando a biblioteca-tempero.  
   - Informa se os slugs são idênticos, sugerindo que se referem à mesma instituição apesar de variações na grafia original.

5. **Exportar lista por inicial**  
   - Solicita uma letra do alfabeto.  
   - Filtra no SQLite instituições cujo slug começa com aquela letra.  
   - Exibe em tabela `rich` e informa a quantidade total encontrada.

### Tarefas bônus
- Agrupar instituições por tipo inferido a partir do slug: se contiver "banco", "corretora", "seguradora", etc., criar uma coluna `categoria` no SQLite e exibir estatísticas por categoria.
- Criar uma tabela de índice invertido no SQLite que mapeie cada palavra do slug para as instituições que a contêm, permitindo busca por qualquer palavra isolada.
- Gerar URLs fictícias no formato `https://exemplo.com/instituicao/{slug}` e exibi-las como links clicáveis no terminal usando recursos do `rich`.

---

## Trabalho 4 — QR Code de Endereços
**Biblioteca-tempero:** `qrcode`  
**API sugerida:** `https://viacep.com.br/ws/{cep}/json/`

### Descrição geral
Aplicação que consulta endereços pelo CEP e gera QR Codes contendo os dados estruturados. A biblioteca `qrcode` deve ser usada para gerar representações de QR Code, preferencialmente em formato ASCII (texto) para exibição direta no terminal, ou como imagem quando solicitado.

### Menu inicial e comportamento

1. **Consultar CEP e gerar QR Code**  
   - Solicita um CEP (com ou sem hífen).  
   - Consulta a API. Se retornar erro, informa ao usuário e retorna ao menu.  
   - Armazena o endereço completo no SQLite.  
   - Usa a biblioteca-tempero para gerar um QR Code ASCII contendo uma string estruturada com logradouro, bairro, cidade e UF.  
   - Exibe o QR Code no terminal usando `rich` (em um painel ou com bordas) e, abaixo, uma tabela com os dados do endereço.

2. **Gerar QR Code customizado**  
   - Solicita logradouro, número, bairro, cidade e UF manualmente.  
   - Gera um QR Code ASCII com esses dados.  
   - Armazena no SQLite marcando como `origem = 'manual'`.  
   - Exibe o QR Code e os dados.

3. **Histórico de QR Codes**  
   - Lista todos os endereços armazenados no SQLite.  
   - Exibe: ID, CEP (ou "manual"), endereço completo em uma linha e data/hora da geração.  
   - Permite que o usuário selecione um registro pelo ID para reexibir o QR Code ASCII correspondente.

4. **Exportar QR Code para arquivo**  
   - Solicita um ID do histórico.  
   - Gera o QR Code e o salva em um arquivo (imagem PNG se a biblioteca-tempero permitir, ou arquivo de texto com a representação ASCII).  
   - Confirma o caminho absoluto do arquivo salvo.

5. **Comparar endereços**  
   - Solicita dois CEPs (ou IDs do histórico).  
   - Consulta/compara se estão no mesmo bairro, mesma cidade ou mesmo UF.  
   - Exibe uma tabela `rich` de comparação lado a lado indicando igualdades e diferenças.

### Tarefas bônus
- Gerar um QR Code que contenha um link de mapa fictício para o endereço consultado (ex: `https://maps.exemplo.com/?q=...`).
- Implementar uma "leitura simulada": o usuário cola um texto que representa o conteúdo de um QR Code lido, e o sistema tenta parsear como endereço, consultar o CEP correspondente e exibir os dados completos.
- Criar um "cartão de visita digital": um QR Code no formato vCard que inclua endereço e um telefone fictício gerado pelo usuário.

---

## Trabalho 5 — Geocodificação de Municípios Brasileiros
**Biblioteca-tempero:** `geopy`  
**API sugerida:** `https://servicodados.ibge.gov.br/api/v1/localidades/municipios` (para obter lista) + geocodificador Nominatim

### Descrição geral
Aplicação que obtém municípios brasileiros via IBGE, geocodifica para latitude e longitude usando `geopy`, e permite cálculos geográficos. A biblioteca `geopy` deve ser usada tanto para obter coordenadas quanto para calcular distâncias entre pontos.

### Menu inicial e comportamento

1. **Sincronizar municípios de uma UF**  
   - Solicita a sigla de um estado (ex: SP, BA).  
   - Consulta o IBGE para listar todos os municípios daquele estado.  
   - Para cada município, usa a biblioteca-tempero para obter latitude e longitude.  
   - Armazena no SQLite: ID IBGE, nome, UF, latitude, longitude e data da consulta.  
   - Exibe um resumo `rich`: total sincronizado, média das latitudes e longitudes, e tempo estimado da operação.

2. **Buscar coordenadas de município**  
   - Solicita nome do município e UF.  
   - Consulta o SQLite. Se não existir, consulta a biblioteca-tempero diretamente e armazena.  
   - Exibe: nome, UF, latitude, longitude. Se disponível, exibe também um link fictício para visualização no mapa.

3. **Calcular distância entre municípios**  
   - Solicita dois pares município/UF.  
   - Busca no SQLite (ou consulta geopy se ausente).  
   - Usa a biblioteca-tempero para calcular a distância em quilômetros entre as coordenadas.  
   - Exibe a distância em km e em milhas. Classifica como "vizinhos" se a distância for menor que 50 km.

4. **Municípios próximos**  
   - Solicita um município/UF e um raio em quilômetros.  
   - Consulta o SQLite por todos os municípios sincronizados da mesma UF (ou de todas as UFs, se houver dados).  
   - Lista aqueles que estão dentro do raio informado, ordenados por distância crescente.  
   - Exibe em tabela `rich`.

5. **Listar municípios sincronizados**  
   - Exibe todos os municípios do banco em tabela `rich`.  
   - Permite filtrar por UF antes de exibir.

### Tarefas bônus
- Implementar um mecanismo de cache que, se a biblioteca-tempero retornar erro por limite de requisições, use coordenadas aproximadas baseadas na capital do estado.
- Gerar um "mapa ASCII" simplificado: uma grade de caracteres no terminal mostrando a posição relativa dos municípios sincronizados de uma UF.
- Exportar os dados sincronizados para um arquivo CSV usando apenas o módulo `csv` built-in.

---

## Trabalho 6 — Estatísticas de Nomes e Frequência
**Biblioteca-tempero:** `humanize`  

### Descrição geral
Aplicação que consulta a frequência histórica de nomes no censo brasileiro (IBGE) e usa `humanize` para apresentar números de forma amigável e natural (ex: "15,2 mil", "1,2 milhão").

### Menu inicial e comportamento

1. **Consultar frequência de um nome**  
   - Solicita um nome.  
   - Consulta a API. A resposta contém frequência por década.  
   - Para cada década, usa a biblioteca-tempero para converter o número bruto em uma representação humanizada.  
   - Armazena no SQLite: nome, década, frequência bruta, frequência humanizada.  
   - Exibe tabela `rich` com: década, frequência bruta, frequência humanizada e tendência (subiu, desceu ou estável em relação à década anterior).

2. **Comparar dois nomes**  
   - Solicita dois nomes.  
   - Consulta ambos, soma a frequência total de cada um em todas as décadas.  
   - Usa a biblioteca-tempero para apresentar os totais de forma humanizada.  
   - Exibe: nome mais popular, diferença absoluta e percentual.  
   - Exibe um gráfico de comparação simples usando caracteres ASCII ou barras proporcionais no `rich`.

3. **Ranking de década**  
   - Solicita uma década (ex: 2000).  
   - Consulta o SQLite por todos os nomes já pesquisados que possuem dados naquela década.  
   - Ordena por frequência bruta e exibe o top 10 em tabela `rich`, com frequências humanizadas.

4. **Resumo de um nome**  
   - Para um nome informado, calcula: frequência total (soma de todas as décadas), década de pico e uma estimativa de prevalência (ex: "a cada X brasileiros, 1 tem esse nome").  
   - Usa a biblioteca-tempero para humanizar todos os números apresentados.  
   - Armazena o resumo no SQLite.

5. **Nomes por faixa de frequência**  
   - Solicita uma faixa (ex: "mais de 100 mil", "entre 10 mil e 50 mil").  
   - Consulta o SQLite e lista nomes que se enquadram na faixa.  
   - Usa a biblioteca-tempero para apresentar os limites da faixa de forma natural.

### Tarefas bônus
- Implementar uma "predição" fictícia: baseado na tendência das três últimas décadas, projetar a frequência estimada para a próxima década e humanizar o resultado.
- Converter a frequência total em "equivalente à população de [cidade brasileira]" usando uma tabela interna de populações aproximadas de cidades.
- Gerar um "certificado de popularidade" em texto puro com bordas ASCII contendo os dados humanizados do nome.

---

## Trabalho 7 — Relatório de Câmbio com Templates
**Biblioteca-tempero:** `jinja2`  
**API sugerida:** `https://brasilapi.com.br/api/cambio/v1/cotacao` (ou endpoint de moedas/câmbio disponível)

### Descrição geral
Aplicação que consulta cotações de moedas e usa `jinja2` para renderizar templates personalizados de exibição e relatório. A biblioteca `jinja2` deve ser usada para separar a lógica de apresentação da lógica de negócio, permitindo layouts de saída configuráveis.

### Menu inicial e comportamento

1. **Consultar cotação atual**  
   - Solicita o par de moedas (ex: USD-BRL) ou apresenta uma lista de pares disponíveis.  
   - Consulta a API.  
   - Armazena no SQLite: moeda, valor de compra, valor de venda, data/hora da consulta.  
   - Usa a biblioteca-tempero para renderizar um template padrão de exibição (ex: uma frase estruturada, um recibo, um painel informativo).  
   - Exibe o resultado renderizado no terminal usando `rich` (em um painel ou como markdown renderizado).

2. **Gerar relatório de variação**  
   - Solicita uma moeda e um número de dias `N`.  
   - Consulta o SQLite por registros históricos daquela moeda. Se não houver histórico suficiente, simula ou informa a limitação.  
   - Usa a biblioteca-tempero para renderizar um template que apresente: data, valor, variação percentual em relação ao registro anterior.  
   - Exibe o relatório renderizado.

3. **Template customizado**  
   - Permite ao usuário digitar um template simples da biblioteca-tempero (ex: `"Hoje: {{ compra }} | Previsão: {{ previsto }}"`).  
   - O sistema solicita os valores das variáveis e renderiza o template.  
   - Armazena o template no SQLite como `template_customizado`.  
   - Exibe o resultado renderizado.

4. **Listar histórico**  
   - Exibe todas as cotações armazenadas no SQLite em tabela `rich`.  
   - Permite filtro por moeda.

5. **Comparar moedas**  
   - Solicita duas moedas.  
   - Consulta ambas.  
   - Usa a biblioteca-tempero para renderizar um template de comparação (ex: "1 {{ moeda1 }} equivale a X {{ moeda2 }}").  
   - Exibe o resultado em painel `rich`.

### Tarefas bônus
- Permitir que o usuário salve templates em arquivos `.txt` no diretório do projeto e o sistema os carregue dinamicamente pelo nome do arquivo.
- Implementar um "conversor de valores": o usuário informa um valor em uma moeda e o sistema renderiza um template mostrando o equivalente em múltiplas outras moedas simultaneamente.
- Criar um template de "alerta de mercado" que, baseado em regras configuráveis (ex: se cotação cair abaixo de X, emitir alerta de compra), renderize uma mensagem de alerta visualmente destacada com `rich`.

---

## Trabalho 8 — Busca Aproximada em Instituições Bancárias
**Biblioteca-tempero:** `thefuzz`  
**API sugerida:** `https://brasilapi.com.br/api/banks/v1`

### Descrição geral
Aplicação que consulta a lista de bancos brasileiros e permite buscas por aproximação de texto usando algoritmos de similaridade. A biblioteca `thefuzz` deve ser usada para calcular scores de similaridade entre strings, possibilitando encontrar registros mesmo com erros de digitação ou variações nominais.

### Menu inicial e comportamento

1. **Sincronizar bancos**  
   - Consulta a API de bancos.  
   - Armazena no SQLite: ISPB, nome, código e nome completo.  
   - Exibe resumo com `rich`: total de bancos sincronizados.

2. **Busca por aproximação**  
   - Solicita um nome (ou fragmento).  
   - Usa a biblioteca-tempero para comparar o termo informado com todos os nomes no SQLite.  
   - Retorna os 5 registros mais similares.  
   - Exibe em tabela `rich`: nome do banco, score de similaridade (0 a 100) e código. Se o score for 100, destaca como "correspondência exata".

3. **Busca por código com tolerância**  
   - Solicita um código numérico (ex: 341).  
   - Se não encontrar exatamente no SQLite, usa a biblioteca-tempero para buscar códigos similares (útil para typos como 340 ou 3410).  
   - Exibe resultados com scores.

4. **Agrupar por similaridade**  
   - Analisa todos os bancos do SQLite e agrupa aqueles cujos nomes apresentam alta similaridade entre si (ex: "BANCO DO BRASIL" e "BCO BRASIL S.A.").  
   - Usa a biblioteca-tempero para calcular a similaridade par a par.  
   - Exibe os grupos sugeridos em tabela `rich`, com o nome representativo de cada grupo.

5. **Corrigir nome digitado**  
   - Solicita um nome digitado com possíveis erros.  
   - Usa a biblioteca-tempero para sugerir o nome correto baseado nos bancos cadastrados.  
   - Exibe: nome digitado, sugestão corrigida e nível de confiança.

### Tarefas bônus
- Implementar "autocorreção simulada": o usuário informa uma lista de nomes digitados à mão (como em um formulário), e o sistema processa todos em lote, sugerindo correções e gerando um relatório de alterações sugeridas.
- Criar um "quiz" de reconhecimento: o sistema mostra um nome intencionalmente distorcido de um banco e o usuário deve adivinhar qual é; o sistema usa a biblioteca-tempero para verificar se o palpite está próximo o suficiente do nome correto.
- Exportar um dicionário de sinônimos: pares de nomes de bancos que apresentam score maior que 90, salvos em um arquivo de texto.


## 1. Requisitos Técnicos Gerais (obrigatórios para todos os trabalhos)

Cada dupla deve produzir uma aplicação executável no terminal que atenda aos seguintes requisitos estruturais:

- **Ambiente virtual**: o projeto deve ser desenvolvido dentro de um `venv`. O diretório do ambiente pode ser incluído no `.gitignore`.
- **Dependências**: todas as bibliotecas de terceiros (incluindo `requests`, `rich` e a biblioteca-tempero atribuída) devem ser listadas em um arquivo `requirements.txt` funcional. Deve ser possível recriar o ambiente com `pip install -r requirements.txt`.
- **Organização modular**: o código deve estar dividido em múltiplos arquivos `.py`. Pelo menos um módulo deve conter funções reutilizáveis, e o ponto de entrada da aplicação deve ser protegido por `if __name__ == "__main__":`.
- **Imports**: o código deve demonstrar import de built-ins, import de arquivos locais (módulos do próprio projeto) e import de bibliotecas remotas instaladas via `pip`.
- **Estruturas de dados**: o uso de **dicionários** é obrigatório em pelo menos uma etapa do fluxo de dados. Listas, tuplas e/ou sets podem ser usados livremente quando convenientes.
- **Lógica de programação**: o código deve empregar condicionais, loops, operadores lógicos e aritméticos de forma significativa.
- **Funções**: a lógica deve ser fragmentada em funções com responsabilidades definidas. Evite scripts monolíticos.
- **Persistência**: todos os trabalhos devem usar **SQLite** para armazenar e consultar dados. O banco pode ser um arquivo `.db` local.
- **APIs HTTP**: a aquisição de dados externos deve ser feita exclusivamente via `requests.get()` (ou `.post()` quando a API exigir) contra APIs públicas. APIs brasileiras são preferenciais, mas não obrigatórias.
- **Exibição**: toda a apresentação de dados no terminal deve usar a biblioteca `rich` (tabelas, painéis, cores, progresso, etc.). Evite `print()` simples para saída final de dados estruturados.
- **Fluxo obrigatório**: o esqueleto lógico esperado é:
  ```
  venv → pip install → requirements.txt
      ↓
  requests.get() → dicionário
      ↓
  normalizar / validar / enriquecer (biblioteca-tempero)
      ↓
  SQLite (salvar / consultar)
      ↓
  rich (exibir no terminal)
  ```

> **Restrição importante**: esta especificação descreve **O QUE** o sistema deve fazer e **COMO** deve se comportar em relação às escolhas do usuário. **NÃO descreve COMO implementar no código**. As decisões de implementação (nomes de funções, estruturas internas, algoritmos, tratamento de exceções, etc.) são de responsabilidade exclusiva da dupla.

---

## Trabalho 9 — Tabela FIPE com Valores por Extenso
**Biblioteca-tempero:** `num2words`  
**API sugerida:** `https://brasilapi.com.br/api/fipe/preco/v1/{codigoFipe}` (e endpoints auxiliares de marcas/modelos)

### Descrição geral
Aplicação que consulta preços de veículos na tabela FIPE e converte os valores numéricos para representação por extenso em português. A biblioteca `num2words` deve ser usada para transformar qualquer valor monetário ou inteiro em texto por extenso.

### Menu inicial e comportamento

1. **Consultar preço por código FIPE**  
   - Solicita o código FIPE (padrão alfanumérico) e o tipo de veículo (carro, moto, caminhão).  
   - Consulta a API. Se o código for inválido ou não retornar dados, informa o usuário e retorna ao menu.  
   - Armazena no SQLite: código FIPE, marca, modelo, ano, preço numérico e preço por extenso.  
   - Exibe em tabela `rich`: veículo, ano, preço numérico e preço por extenso completo.

2. **Listar marcas por tipo**  
   - Solicita o tipo de veículo.  
   - Consulta a API de marcas.  
   - Armazena as marcas no SQLite com uma flag indicando que são metadados de catálogo.  
   - Exibe em tabela `rich`: código da marca, nome e quantidade de modelos já consultados (se houver histórico).

3. **Listar modelos por marca**  
   - Solicita o código de uma marca.  
   - Consulta a API de modelos.  
   - Armazena no SQLite vinculado à marca.  
   - Exibe em tabela `rich`: código do modelo, nome e preço médio dos anos já consultados (se houver).

4. **Comparar preços de dois veículos**  
   - Solicita dois códigos FIPE.  
   - Consulta ambos (ou recupera do SQLite se já existirem).  
   - Exibe comparação lado a lado em `rich`: modelo, ano, preço numérico, preço por extenso e diferença absoluta (também por extenso).  
   - Indica qual é o mais caro e qual é o mais barato.

5. **Histórico de consultas**  
   - Lista todas as consultas de preço armazenadas no SQLite.  
   - Permite filtro por tipo de veículo, por marca ou por faixa de preço.  
   - Exibe em tabela `rich` com todas as colunas, incluindo o preço por extenso.

### Tarefas bônus
- Adicionar uma opção que converta o preço para extenso em inglês também, exibindo ambos os idiomas.
- Gerar um "recibo fictício" em texto puro com bordas ASCII contendo os dados do veículo e o valor por extenso, como se fosse um documento oficial.
- Implementar uma simulação de depreciação: o usuário informa uma porcentagem anual e o sistema projeta o valor do veículo para os próximos 5 anos, convertendo cada valor projetado para extenso.

---

## Trabalho 10 — Validação de Dados Corporativos
**Biblioteca-tempero:** `validators`  
**API sugerida:** `https://brasilapi.com.br/api/cnpj/v1/{cnpj}`

### Descrição geral
Aplicação que consulta dados de empresas pela Receita Federal e valida formatos de dados corporativos antes e após a consulta. A biblioteca `validators` deve ser usada para verificar CNPJ, URLs, endereços de e-mail e outros padrões textuais.

### Menu inicial e comportamento

1. **Validar e consultar CNPJ**  
   - Solicita um CNPJ (com ou sem máscara).  
   - Usa a biblioteca-tempero para validar o formato antes de consultar a API. Se inválido, informa imediatamente sem fazer requisição.  
   - Se válido, consulta a API.  
   - Armazena no SQLite: CNPJ, razão social, nome fantasia, situação cadastral, data de consulta.  
   - Exibe em tabela `rich` todos os campos retornados.

2. **Validar site corporativo**  
   - Solicita uma URL (ex: site da empresa).  
   - Usa a biblioteca-tempero para validar se a URL está bem formada.  
   - Se válida, armazena no SQLite com uma flag indicando que foi validada.  
   - Exibe o resultado da validação e, se possível, extrai o domínio principal.

3. **Validar e-mail de domínio**  
   - Solicita um endereço de e-mail.  
   - Usa a biblioteca-tempero para validar formato.  
   - Se válido, extrai o domínio e verifica se há correspondência com algum site corporativo já validado no SQLite.  
   - Exibe o resultado e a relação encontrada, se houver.

4. **Listar histórico de validações**  
   - Exibe todas as validações realizadas (CNPJs, URLs, e-mails) em uma tabela `rich` unificada.  
   - Permite filtrar por tipo de validação ou por status (válido/inválido).  
   - Inclui uma coluna de timestamp.

5. **Estatísticas de conformidade**  
   - Analisa todos os registros do SQLite.  
   - Calcula: total de CNPJs válidos consultados, total de URLs válidas, total de e-mails válidos, percentual de registros com todos os três tipos de dados validados simultaneamente.  
   - Exibe em um painel `rich` com múltiplas seções de estatísticas.

### Tarefas bônus
- Implementar uma "verificação de consistência": se um CNPJ consultado retornar um site e um e-mail, o sistema deve validar ambos e alertar se o domínio do e-mail não corresponder ao domínio do site.
- Criar um modo de lote: o usuário fornece um arquivo de texto com múltiplos CNPJs (um por linha) e o sistema processa todos, gerando um relatório de validação em tabela `rich`.
- Implementar uma "pontuação de confiabilidade": cada empresa recebe uma nota de 0 a 100 baseada na quantidade e validade dos dados disponíveis (CNPJ ativo, site válido, e-mail válido, telefone presente, etc.).

---

## Trabalho 11 — Previsão do Tempo com Emojis
**Biblioteca-tempero:** `emoji`  
**API sugerida:** `https://api.open-meteo.com/v1/forecast` (API pública global, utilizada para coordenadas de cidades brasileiras)

### Descrição geral
Aplicação que consulta previsão meteorológica para cidades brasileiras e enriquece a apresentação com emojis representativos das condições climáticas. A biblioteca `emoji` deve ser usada para converter códigos de clima em emojis e para inserir emojis em textos descritivos.

### Menu inicial e comportamento

1. **Previsão atual por cidade**  
   - Solicita o nome de uma cidade brasileira e o estado (UF).  
   - Usa coordenadas predefinidas ou consulta-as de forma apropriada.  
   - Consulta a API de previsão do tempo.  
   - Interpreta o código de clima retornado e usa a biblioteca-tempero para mapear para um emoji apropriado.  
   - Armazena no SQLite: cidade, UF, temperatura, condição, emoji, data/hora da consulta.  
   - Exibe em painel `rich`: cidade, temperatura, sensação térmica (se disponível), condição textual e emoji grande.

2. **Previsão dos próximos dias**  
   - Solicita cidade/UF e um número de dias `N` (até o limite suportado pela API).  
   - Consulta a API.  
   - Para cada dia, mapeia o código de clima para emoji usando a biblioteca-tempero.  
   - Armazena cada dia como registro individual no SQLite.  
   - Exibe em tabela `rich`: data, temperatura mínima, máxima, condição e emoji.

3. **Comparar clima entre duas cidades**  
   - Solicita duas cidades com UF.  
   - Consulta ambas.  
   - Exibe comparação lado a lado em `rich`: temperatura atual, condição e emoji de cada cidade.  
   - Indica qual está mais quente, qual tem mais chance de precipitação e a diferença de temperatura.

4. **Alerta de temperatura extrema**  
   - Solicita uma cidade/UF e limites de temperatura (mínima e máxima).  
   - Consulta a previsão atual.  
   - Se a temperatura estiver fora dos limites, exibe um alerta visual em `rich` com emoji de alerta e a temperatura observada.  
   - Armazena o alerta no SQLite com status (ativo/resolvido).

5. **Histórico de consultas**  
   - Lista todas as consultas meteorológicas armazenadas no SQLite.  
   - Permite filtro por cidade, por data ou por condição climática.  
   - Exibe em tabela `rich` com todas as colunas, incluindo o emoji associado.

### Tarefas bônus
- Gerar um "relatório meteorológico em prosa": um parágrafo de texto natural descrevendo a previsão dos próximos dias, intercalado com emojis apropriados, renderizado em um painel `rich`.
- Criar um "calendário do clima" em ASCII para o mês atual: uma grade onde cada dia exibe o emoji da condição climática mais provável, consultando ou simulando dados.
- Implementar um "modo viagem": o usuário informa uma rota de cidades (origem, paradas, destino) e o sistema exibe a previsão para cada ponto da rota em uma timeline vertical com emojis.

---

## Trabalho 12 — Gerador de Cadastros Fictícios por Localidade
**Biblioteca-tempero:** `faker`  
**API sugerida:** `https://viacep.com.br/ws/{cep}/json/`

### Descrição geral
Aplicação que consulta endereços reais pelo CEP e gera perfis de pessoas fictícias que residiriam naquele local. A biblioteca `faker` deve ser usada para criar nomes, documentos, telefones, e-mails e outros dados pessoais contextualizados ao Brasil.

### Menu inicial e comportamento

1. **Gerar cadastro por CEP**  
   - Solicita um CEP (com ou sem hífen).  
   - Consulta a API. Se inválido, informa e retorna.  
   - Usa a biblioteca-tempero para gerar um perfil completo: nome, CPF, RG, telefone, e-mail, data de nascimento, profissão.  
   - Armazena no SQLite vinculando o perfil fictício ao endereço real obtido: CEP, logradouro, bairro, cidade, UF, e todos os dados fictícios gerados.  
   - Exibe em painel `rich` o perfil completo e o endereço em uma tabela estruturada.

2. **Gerar lote para uma cidade**  
   - Solicita o nome de uma cidade e UF.  
   - O sistema deve obter pelo menos um CEP válido para aquela cidade (pode ser via consulta prévia, tabela interna ou outra estratégia).  
   - Gera `N` cadastros fictícios (quantidade informada pelo usuário) todos vinculados à mesma cidade, mas com endereços de CEPs distintos se possível.  
   - Armazena todos no SQLite.  
   - Exibe resumo em `rich`: total gerado, distribuição por bairro (se houver variação) e faixa etária.

3. **Buscar cadastros por bairro**  
   - Solicita um bairro.  
   - Consulta o SQLite por perfis fictícios cujo endereço contenha aquele bairro.  
   - Exibe em tabela `rich`: nome, CPF, endereço completo e telefone.  
   - Informa o total encontrado.

4. **Exportar lista de cadastros**  
   - Lista todos os cadastros armazenados.  
   - Permite filtro por cidade, estado ou faixa etária.  
   - Exibe em tabela `rich`.  
   - Oferece a opção de salvar os dados filtrados em um arquivo de texto estruturado (formato livre, desde que legível) no diretório do projeto.

5. **Estatísticas por localidade**  
   - Analisa todos os cadastros do SQLite.  
   - Agrupa por cidade/UF.  
   - Calcula: total de cadastros, média de idade, distribuição por profissão (top 5), distribuição por domínio de e-mail.  
   - Exibe em painel `rich` com múltiplas seções e tabelas.

### Tarefas bônus
- Implementar geração de CPFs com dígitos verificadores válidos (algoritmo próprio ou via biblioteca-tempero, se suportado) em vez de CPFs puramente aleatórios.
- Criar um "cartão de visita digital" em texto puro com bordas ASCII contendo nome, telefone, e-mail e endereço do perfil selecionado.
- Implementar um "modo censo": o usuário informa uma cidade e o sistema gera uma população fictícia proporcional à população real da cidade (usando uma tabela interna de populações aproximadas), distribuindo idades e profissões de forma pseudo-realista.

---

## 10. Tarefas Bônus Gerais

As tarefas abaixo podem ser aplicadas a **qualquer um dos trabalhos** e servem como desafio adicional para duplas que concluíram o trabalho principal antes do prazo:

- **Exportação de dados**: adicionar uma opção no menu para exportar os dados do SQLite para um arquivo JSON ou CSV, usando apenas bibliotecas built-in.
- **Modo batch**: implementar uma opção que leia um arquivo de entrada (ex: `.txt` com uma lista de CEPs, CNPJs, nomes ou datas) e processe todos os itens em sequência, exibindo um resumo final.
- **Painel de estatísticas**: criar uma tela de dashboard usando `rich` que exiba estatísticas gerais do banco (quantidade de registros, última consulta, distribuição por categoria/ano/estado, etc.) em layout de múltiplas colunas.
- **Configuração via arquivo**: permitir que a aplicação leia configurações (URL base da API, ano padrão, moeda padrão, UF padrão) de um arquivo JSON ou de variáveis de ambiente, sem hardcode.
- **Testes de integração simulados**: criar um módulo separado que, sem usar a API real, simule respostas HTTP e teste se o fluxo de parse → banco → exibição funciona corretamente.
- **Logging**: implementar um sistema de log que registre em arquivo todas as consultas à API, erros e escolhas do menu, com timestamps.

---

*Cada dupla deve escolher um trabalho e implementar de forma independente, respeitando os requisitos técnicos e o comportamento descrito nesta especificação.*
