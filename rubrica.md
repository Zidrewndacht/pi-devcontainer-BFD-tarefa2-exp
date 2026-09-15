# Rubrica de Avaliação — Bibliotecas Externas em Python

> **Destinatário:** agentes avaliadores (correção padronizada).
> **Escopo:** a pasta de um trabalho entregue por uma dupla (ex.: `/workspace/01/`), implementando **um** dos 12 trabalhos da especificação (`tarefas.md`).
> **Saída obrigatória:** arquivo `avaliado.md` na raiz da pasta do trabalho, em **português do Brasil**, com justificativa de cada decisão para o aluno.

---

## 0. Regras gerais (obrigatórias)

### 0.1 Correção simultânea — isolamento total
As 12 avaliações rodam **simultaneamente, por agentes diferentes, no mesmo ambiente**.

- Cada avaliador trabalha **apenas na pasta do seu trabalho** (ex.: `/workspace/01/`). Não abrir nem modificar qualquer outra pasta.
- **Caminhos compartilhados são proibidos**: nada de `/tmp/venv_eval`, nada de `pip install` no Python do sistema, nada de diretório fora da pasta do trabalho. Dois avaliadores escrevendo no mesmo caminho se contaminam mutuamente.
- Na pasta do trabalho, o avaliador só pode criar: `avaliado.md` e a subpasta `_avaliacao/` (sandbox de execução). **Nunca modificar os arquivos do trabalho entregue.**
- Todo venv, cópia de código, artefato e cache de execução fica dentro de `_avaliacao/` (ver Seção 1, Etapa 3).

### 0.2 Prioridade: análise do código
A correção se apoia **primariamente na análise estática do código**. Execução é **opcional** e serve apenas para tirar dúvidas sobre comportamentos que não dá para decidir somente pelo código (Seção 1, Etapa 3). Não é necessário — nem produtivo — executar algo que a análise já provou não funcionar.

### 0.3 Idioma e justificativa (regra central da correção)
A correção deve ser escrita em **português do Brasil** no arquivo `avaliado.md`, na raiz da pasta do trabalho. **Cada pontuação deve ser explicada e justificada para o aluno**:

- Cada ponto tirado, dado ou parcial (0 / 0,5 / 1) precisa indicar **o quê** está certo ou errado, **onde** (arquivo:linha ou comportamento observado) e **o que fazer** para corrigir.
- Cada regra de teto aplicada precisa de explicação em linguagem acessível para o aluno.
- O relatório é **feedback**, não checklist seco: a dupla deve conseguir entender e reparar cada decisão sem adivinhação.
- Seção final obrigatória de "Mensagem para a dupla" (modelo na Seção 6, item 9).

### 0.4 Como usar esta rubrica
1. Identifique qual trabalho (1–12) a dupla implementou (README, `requirements.txt`, biblioteca-tempero efetivamente usada). Use **apenas** a seção 5.X correspondente para verificadores e entradas de teste.
2. Siga o protocolo da **Seção 1** na ordem.
3. Toda pontuação exige **evidência**: citação de código (`arquivo:linhas`) como evidência primária; saída de execução (quando realizada) como evidência complementar. Sem evidência, o critério vale **0**.
4. Seja literal: a especificação define o que deve acontecer; se o código diverge, não complete o raciocínio a favor da dupla.
5. Itens que não puderam ser verificados seguem a **Seção 7 (casos-limite)** — não zere sem registrar o motivo no `avaliado.md`.

---

## 1. Protocolo de avaliação

### Etapa 1 — Mapeamento do projeto
- Liste a estrutura: arquivos `.py`, README, `requirements.txt`, `.gitignore`, presença de `.db`.
- Identifique o **arquivo de entrada** (`grep -rn "if __name__" .`) e os demais módulos.
- Se houver `.db` commitado, inspecione **somente leitura** (isso é análise, não execução):
  ```bash
  sqlite3 <banco>.db ".tables"
  sqlite3 <banco>.db "SELECT COUNT(*) FROM <tabela>;"
  sqlite3 <banco>.db "SELECT * FROM <tabela> LIMIT 5;"
  ```

### Etapa 2 — Análise do código (sempre; é a base da correção)

Greps iniciais:
```bash
grep -rn "if __name__" .
grep -rn "requests.get\|requests.post" .
grep -rn "CREATE TABLE\|INSERT INTO\|SELECT\|sqlite3" .
grep -rn "from rich import\|import rich" .
grep -rn "print(" .
grep -rn "<import da biblioteca-tempero>" .   # ex.: "import dateutil", "from slugify import"
```

Em seguida, **para cada um dos 5 itens obrigatórios**, trace no código e cite (`arquivo:linhas`):

| Ponto da trilha | O que localizar |
|---|---|
| (a) Entrada | como o input do usuário é solicitado e validado (tipos, formatos aceitos) |
| (b) Fonte do dado | API via `requests` / SQLite / biblioteca-tempero / local — conforme exige a especificação para o item |
| (c) Biblioteca-tempero | onde é chamada e como o resultado **influencia** o fluxo (parse, validação, cálculo, formatação) |
| (d) Persistência | onde o dado é gravado/consultado no SQLite e quais campos |
| (e) Apresentação | onde a saída `rich` é montada e quais campos exibe |

**Checklist estático de dependências:** todo import de terceiros no código aparece no `requirements.txt` (import presente sem pacote = aplicação não roda em venv limpo → vê R1); `requests`, `rich` e a biblioteca-tempero presentes com nomes de pacote corretos (Seção 5.X).

**Robustez estática:** validação de entradas (tipo, tamanho, formato) com mensagem informativa; `try/except` (ou verificação de status da resposta) ao redor das chamadas de API; nenhum caminho que chegue a exceção não tratada.

### Etapa 3 — Execução opcional (apenas para tirar dúvidas)

Execute **somente** quando a análise deixar um subcritério em dúvida real:

**Razões legítimas para executar:**
- Item pontuado **0,5** na análise e o comportamento real decide entre 0,5 e 1,0;
- Suspeita de bug em cálculo, filtro ou ordenação que precisa ser confirmada;
- Verificação de artefato gerado (arquivo exportado existe e é legível);
- Confirmação de fluxo fim-a-fim quando o código *parece* correto, mas há ambiguidade.

**NÃO execute (não agrega e desperdiça tempo/ambiente):**
- Quando a análise já **provou** a falha (dependência faltando → R1; sem SQLite → R4; dado hardcoded → R5; ponto de entrada quebrado → R2): aplique o teto e siga em frente;
- Quando o componente exigido está **claramente ausente** do código — não rode o menu para "confirmar" ausência;
- Quando o custo é **desproporcional** à dúvida (ex.: sincronizar centenas de municípios contra o Nominatim com rate limit só para conferir uma coluna de tabela).

**Sandbox obrigatório (evita contaminação — tudo dentro de `_avaliacao/`):**
```bash
TRAB=/workspace/<pasta-do-trabalho>      # a ÚNICA pasta que você toca
mkdir -p "$TRAB/_avaliacao/copia"
# Cópia sandbox: sem venv, sem .git, sem .db pré-existente
(cd "$TRAB" && tar cf - \
  --exclude='./_avaliacao' --exclude='./venv' --exclude='./.venv' \
  --exclude='./.git' --exclude='*.db' .) \
  | (cd "$TRAB/_avaliacao/copia" && tar xf -)
# venv isolado dentro da própria pasta do trabalho (NUNCA em caminho genérico compartilhado)
python3 -m venv "$TRAB/_avaliacao/venv"
"$TRAB/_avaliacao/venv/bin/pip" install --cache-dir "$TRAB/_avaliacao/pip-cache" \
  -r "$TRAB/_avaliacao/copia/requirements.txt"
# Executar na CÓPIA (o app pode criar .db e arquivos; tudo cai em _avaliacao/)
"$TRAB/_avaliacao/venv/bin/python" "$TRAB/_avaliacao/copia/<main>.py"
```

- Use as entradas da seção 5.X do trabalho; registre entrada + saída (corte de ~20 linhas) no `avaliado.md`.
- Se precisar depurar, altere **apenas a cópia sandbox** — nunca o original.
- App travado: `Ctrl+C` após ~30 s e registre (evidência da seção F).

### Etapa 4 — Pontuação
Aplique a grade (Seção 4), subcritérios (Seção 2) e tetos (Seção 3). Toda decisão registra evidência (`arquivo:linhas` e/ou saída de execução) e justificativa em pt-BR.

### Etapa 5 — Gerar `avaliado.md`
Preencha o modelo da **Seção 6** integralmente, em português do Brasil, na raiz da pasta do trabalho.

---

## 2. Escala de pontuação

| Valor | Significado |
|---|---|
| **1,0** | Cumprido integralmente, com evidência. |
| **0,5** | Parcialmente cumprido: existe, mas com falha relevante, campo ausente, comportamento inconsistente ou dúvida não resolvida (justificar). |
| **0** | Ausente, não funcional, ou sem evidência. |

- **Evidência:** primária = citação de código (`arquivo:linhas`); complementar = saída de execução (quando realizada). Sem evidência, o critério vale 0.
- Critérios com peso > 1 pt: frações proporcionais (ex.: 3 pts → 0/1/2/3; 1,5 em caso justo de "metade funcional", com justificativa registrada).
- Arredondamento do total: 2 casas decimais.

### Subcritérios genéricos dos itens obrigatórios (seção E)

Cada item obrigatório (1 a 5 de cada trabalho) vale **10 pts**, distribuídos em:

| Código | Subcritério (2 pts) | O que verificar (base: análise do código) |
|---|---|---|
| **E-a** | Interação | O item solicita ao usuário exatamente o que a especificação descreve (campos, formatos aceitos, opcionais), com validação das entradas. |
| **E-b** | Fonte de dados | O item usa a fonte exigida para ele: API pública via `requests` (sem dados hardcoded passando por resposta de API), SQLite, ou local/biblioteca quando o item não pede API. |
| **E-c** | Biblioteca-tempero | A biblioteca do trabalho é usada de forma **efetiva na lógica central do item** (não apenas importada: o resultado deve influenciar parse/validação/cálculo/formatação). |
| **E-d** | Persistência | O item grava/consulta o SQLite conforme especificado, com os campos exigidos (código de `INSERT`/`SELECT`; `.db` commitado ou sandbox corroboram). |
| **E-e** | Apresentação | A saída é montada com `rich` (Table/Panel/Box/…) contendo **todos** os campos e comportamentos que a especificação exige para o item. |

Pontue os 5 subcritérios **e** confira os "verificadores específicos" da tabela do trabalho (Seção 5.X): se um verificador específico falhar, o subcritério mais afetado cai para 0,5 ou 0 — registre qual e por quê.

---

## 3. Regras de teto (capping) — aplicam-se SEMPRE

| Regra | Condição | Teto |
|---|---|---|
| **R1** | `requirements.txt` ausente; imports de terceiros do código não cobertos por ele; ou (se a execução foi feita) instalação falha no sandbox | **30 pts** no total |
| **R2** | Aplicação não inicia — provado por análise (erro de sintaxe, import inexistente, entry point quebrado) ou pela execução opcional | Seções **E e F** a **50%** do valor; marcar "NÃO INICIA" no relatório |
| **R3** | Biblioteca-tempero importada mas **não usada** na lógica de nenhum item | E-c = 0 em todos os itens **e** teto de **80 pts** |
| **R4** | SQLite ausente ou inoperante (C3 = 0) | Teto de **70 pts** |
| **R5** | Dados externos hardcoded no lugar de API (C4 = 0) | E-b = 0 nos itens que exigem API **e** teto de **75 pts** |

Tetos se combinam: aplica-se o **menor** teto atingido. Registre no `avaliado.md` quais regras dispararam e **explique à dupla por quê**.

---

## 4. Grade de pontuação (total = 100 pts)

### A. Ambiente e dependências — 10 pts

| Cód. | Pts | Critério | Como verificar (análise estática; execução só em dúvida) |
|---|---|---|---|
| A1 | 2 | Projeto documenta/usa `venv` (README com instruções e/ou pasta `venv` no `.gitignore`) e o ambiente é reproduzível via `requirements.txt` | README + `.gitignore`; sandbox confirma se houver execução |
| A2 | 4 | `requirements.txt` funcional por análise: cobre **todos** os imports de terceiros do código, nomes de pacote válidos, sem pinning quebrado. Se restar dúvida (conflito de versões, dependência indireta suspeita), instalar no sandbox resolve | greps de imports × `cat requirements.txt`; sandbox opcional |
| A3 | 2 | Lista `requests`, `rich` e a **biblioteca-tempero do trabalho** com os nomes de pacote corretos (ver 5.X) | `cat requirements.txt` |
| A4 | 2 | `.gitignore` presente incluindo `venv`; banco `.db` e artefatos também ignorados (anotar se não) | `cat .gitignore` |

### B. Estrutura de código — 10 pts

| Cód. | Pts | Critério | Como verificar |
|---|---|---|---|
| B1 | 2 | Código em **múltiplos arquivos `.py`** (mín. 3 módulos não vazios — cada um com ≥1 função/classe —, um deles o ponto de entrada) | `ls`, leitura |
| B2 | 2 | Pelo menos 1 módulo com **funções reutilizáveis** (usadas em mais de um lugar ou com responsabilidade geral: parse, banco, API) | leitura |
| B3 | 2 | Ponto de entrada protegido por `if __name__ == "__main__":` com a lógica principal delegada (não apenas `pass`) | grep + leitura |
| B4 | 2 | Os 3 tipos de import demonstrados: built-in (ex.: `sqlite3`, `json`, `os`), módulo local do projeto, biblioteca via `pip` | grep |
| B5 | 2 | **Dicionários** usados em pelo menos uma etapa do fluxo de dados (ex.: resposta da API, registro a inserir, mapeamento) | leitura |

### C. Lógica e persistência — 10 pts

| Cód. | Pts | Critério | Como verificar |
|---|---|---|---|
| C1 | 2 | Condicionais, loops, operadores lógicos (`and`/`or`/`not`) e aritméticos presentes de forma **significativa** (não decorativos) | leitura |
| C2 | 2 | Lógica fragmentada em funções com responsabilidade definida; sem "função-gigante" (> ~80 linhas fazendo tudo) nem script monolítico | leitura |
| C3 | 3 | SQLite de fato usado: schema (`CREATE TABLE`), `INSERT` no fluxo normal e `SELECT` para exibição — no código; `.db` existente corrobora; sandbox (opcional) confirma registros novos | greps + leitura; `sqlite3` (leitura) se houver banco |
| C4 | 3 | Aquisição de dados externos **exclusivamente** via `requests.get()`/`.post()` contra API pública real + parse da resposta (geralmente `r.json()` → dict); **sem** dataset hardcoded passando por API | grep + trilha do fluxo de dados (item b da Etapa 2) |

### D. Exibição — 5 pts

| Cód. | Pts | Critério | Como verificar |
|---|---|---|---|
| D1 | 3 | `rich` usado para toda apresentação de dados estruturados (Table/Panel/Box/progress/links) no código | grep + leitura |
| D2 | 2 | `print()` simples **não** é usado para saída de dados estruturados (tabelas, listas de dados, painéis). `print`/`input` para navegação de menu e prompts é **aceitável** | grep + leitura |

### E. Itens obrigatórios do trabalho — 50 pts

5 itens × 10 pts (subcritérios E-a…E-e, Seção 2) + verificadores específicos da Seção 5.X.

### F. Robustez — 5 pts

| Cód. | Pts | Critério | Como verificar |
|---|---|---|---|
| F1 | 3 | Os inputs inválidos da lista 5.X (1 pt cada) são tratados **no código**: validação + mensagem informativa, sem caminho para exceção não tratada. Execução opcional confere o comportamento real | leitura (obrigatória); sandbox (opcional) |
| F2 | 2 | Chamadas de API protegidas (`try/except` ou verificação de status) com mensagem amigável e continuidade da aplicação | leitura (obrigatória); sandbox (opcional) |

### G. Tarefas bônus — 10 pts

- Cada bônus **concluído** (do trabalho específico — 5.X — ou dos bônus gerais da Seção 10 da especificação) vale **3,33 pts**, com evidência no código (e demonstração, se a execução foi feita).
- Teto: **10 pts**. Bônus "meio funcional" (código presente mas com falha relevante): 50% do valor, justificado.

### Nota final
- **Total**: soma de A–G, após tetos (Seção 3).
- **Nota em 0–10** = total / 10.
- **Aprovado**: total ≥ 70 pts (7,0).

---

## 5. Roteiros por trabalho (verificadores e entradas)

> **Leitura:** os "verificadores específicos" servem à **análise do código** — confira se o item implementa o comportamento descrito e cite `arquivo:linhas`. A coluna "entrada de teste" é o roteiro da **execução opcional** (Seção 1, Etapa 3): use-a apenas quando houver dúvida a esclarecer.
> A API "sugerida" pode ser substituída por API pública **semanticamente equivalente** (mesmo tipo de dado retornado). Se a dupla mudou de API, registre no `avaliado.md`; isso **não** desconta ponto, desde que C4 se mantenha.
> Entrada marcada com `⊘` é um input de robustez (seção F).

### 5.1 — Trabalho 1: Gestão de Feriados Nacionais

- **Biblioteca-tempero:** `python-dateutil` (import: `dateutil`)
- **API sugerida:** `https://brasilapi.com.br/api/feriados/v1/{ano}`

| Item | Entrada de teste (se executar) | Verificadores específicos (análise do código) |
|---|---|---|
| 1.1 Consultar/armazenar ano | `2025` (executar o item 2× p/ duplicatas) | Código trata duplicatas (reporta inseridos × já existentes); grava **ano, data, nome, tipo, dia da semana**; tabela rich com essas colunas; data processada via `dateutil` |
| 1.2 Status de uma data | `25/12/2026`; `2026-12-25`; `25 de dezembro de 2026`; `15/02/2026` (dom); `17/01/2026` (terça) | Múltiplos formatos aceitos via `dateutil.parser`; classifica feriado (com nome + dias restantes/passados) / fim de semana / dia útil; dias calculados via `dateutil` |
| 1.3 Próximos feriados | `3` | Seleciona os próximos N a partir da data atual (ou data opcional); exibe nome, data, dia da semana, dias restantes |
| 1.4 Dias úteis entre duas datas | `01/02/2026` → `28/02/2026` | Cálculo de dias úteis = dias do intervalo − fins de semana − feriados do banco (verificar a aritmética no código); lista os feriados do período |
| 1.5 Listar armazenados | filtro `2025` | Tabela rich de todos os feriados; filtro por ano implementado |

**Robustez:** ⊘ ano `abc`; ⊘ ano `999` (3 dígitos); ⊘ data `31/02/2026`; ⊘ data vazia.

### 5.2 — Trabalho 2: Telefones Brasileiros

- **Biblioteca-tempero:** `phonenumbers`
- **API sugerida:** `https://brasilapi.com.br/api/ddd/v1/{ddd}`

| Item | Entrada de teste (se executar) | Verificadores específicos (análise do código) |
|---|---|---|
| 2.1 Validar/formatar | `11999998888`; `(21) 3333-4444`; `+55 11 99999-8888` | `phonenumbers.parse`/`is_valid_number`/`is_mobile_number` de fato usados; exibe nacional, internacional, tipo, validade; grava **com timestamp** |
| 2.2 Consultar DDD | `21` | DDD validado via `phonenumbers`; API do DDD; grava DDD, estado, cidades (serializável); tabela rich com estado, qtd. e cidades |
| 2.3 Gerar por região | UF `SP`, qtd. `5` | UF → DDDs via API; números gerados/validados com `phonenumbers` (região correta); flag `ficticio = 1` no banco |
| 2.4 Histórico | filtro `móvel` | Tabela com todas as colunas; filtro por tipo/estado |
| 2.5 Comparar dois números | `(11) 99999-8888` × `+5511999998888`; depois `11999998888` × `2133334444` | Representação canônica via `phonenumbers` (ex.: `E164`) usada para comparar equivalência/distinção |

**Robustez:** ⊘ número `12345`; ⊘ DDD `99`; ⊘ número vazio.

### 5.3 — Trabalho 3: Slug de Instituições Financeiras

- **Biblioteca-tempero:** `python-slugify` (import: `slugify`)
- **API sugerida:** `https://brasilapi.com.br/api/cvm/corretoras/v1`

| Item | Entrada de teste (se executar) | Verificadores específicos (análise do código) |
|---|---|---|
| 3.1 Sincronizar/slugificar | (sem entrada) | Slug gerado por `slugify()` para cada nome; grava **código, nome, slug, CNPJ, status**; reporta total + nº de nomes que precisaram de normalização (lógica de contagem verificável); tabela rich das 10 primeiras |
| 3.2 Buscar por slug | `itau`; depois `zzzqqq` | Busca por substring no slug (SQL `LIKE`); sem correspondência → slugs mais próximos lexicograficamente (verificar a lógica de proximidade) |
| 3.3 Normalizar nome livre | `  BANCO   DO   BRASIL   S.A. ` | Slug ASCII lowercase com hífens, sem espaços; versão "limpa" sem sufixo corporativo (S.A./LTDA) por lógica própria |
| 3.4 Comparar nomes | `XP Investimentos` × `xp investimentos`; depois `Banco do Brasil S.A.` × `XP` | Slugs gerados para ambos e comparados; mensagem de "mesma instituição" somente se idênticos |
| 3.5 Exportar por inicial | `b`; depois `z` | Filtro por inicial do slug; tabela + total; 0 resultados tratado graciosamente |

**Robustez:** ⊘ inicial `1`; ⊘ busca vazia.

### 5.4 — Trabalho 4: QR Code de Endereços

- **Biblioteca-tempero:** `qrcode` (se exportar PNG, `Pillow` deve estar no requirements)
- **API sugerida:** `https://viacep.com.br/ws/{cep}/json/`

| Item | Entrada de teste (se executar) | Verificadores específicos (análise do código) |
|---|---|---|
| 4.1 Consultar CEP + QR | `01310100` e `01310-100` | `qrcode` gera QR **ASCII** (renderização textual); painel/borda rich; tabela com logradouro, bairro, cidade, UF; erro da API tratado (mensagem + retorno) |
| 4.2 QR customizado | `Rua Teste, 123` / `Bairro X` / `Cidade Y` / `SP` | QR gerado a partir dos dados manuais; registro com `origem = 'manual'` |
| 4.3 Histórico | (listar) → ID | Colunas: ID, CEP ou "manual", endereço em 1 linha, data/hora; reexibição do QR pelo ID |
| 4.4 Exportar para arquivo | ID válido | Escrita do arquivo (PNG ou ASCII) com caminho **absoluto** retornado e exibido |
| 4.5 Comparar endereços | `01310100` × `01310200`; depois × `20010000` | Comparação de bairro/cidade/UF com tabela lado a lado e indicação de igualdades/diferenças |

**Robustez:** ⊘ CEP `00000000`; ⊘ CEP com letras.

### 5.5 — Trabalho 5: Geocodificação de Municípios

- **Biblioteca-tempero:** `geopy`
- **APIs sugeridas:** IBGE `https://servicodados.ibge.gov.br/api/v1/localidades/municipios` + Nominatim
- **Nota:** o Nominatim limita a ~1 req/s. Se a execução for feita, **prefira UFs pequenas** (`DF` = 1 município; `RR` = 15) no item 1. Na análise, verifique se o código lida com limitações (delay/erro 429).

| Item | Entrada de teste (se executar) | Verificadores específicos (análise do código) |
|---|---|---|
| 5.1 Sincronizar UF | `DF` (fallback: `RR`) | IBGE lista os municípios; `geopy` obtém lat/lon de cada um; grava **ID IBGE, nome, UF, lat, lon, data**; resumo rich com total, média de lat/lon e tempo da operação |
| 5.2 Buscar coordenadas | `Brasília/DF` (já sincronizado); `Maceió/AL` (ausente) | Busca no SQLite primeiro; se ausente, `geopy` direto + gravação; exibe nome, UF, lat, lon |
| 5.3 Distância entre municípios | `Brasília/DF` × `Boa Vista/RR` | `geopy` (ex.: `distance.distance`) calcula a distância; exibe **km e milhas**; "vizinhos" se < 50 km |
| 5.4 Municípios próximos | `Brasília/DF`, raio `500` | Filtro por raio sobre os dados do banco, **ordenado por distância crescente** |
| 5.5 Listar sincronizados | filtro por UF | Tabela rich; filtro por UF |

**Robustez:** ⊘ UF `XX`; ⊘ município `Xyz/DF`; ⊘ raio `0` ou negativo.

### 5.6 — Trabalho 6: Estatísticas de Nomes

- **Biblioteca-tempero:** `humanize`
- **API:** a especificação não fixa a URL — deve ser API pública de frequência de nomes por década (IBGE/censo ou equivalente). Na análise, verifique que os dados vêm de requisição real via `requests` e que o formato (década × frequência) é coerente.

| Item | Entrada de teste (se executar) | Verificadores específicos (análise do código) |
|---|---|---|
| 6.1 Frequência de um nome | `Joao` | `humanize` usado na frequência (ex.: `intcomma`/`natural`); grava **nome, década, bruta, humanizada**; tabela rich com década, bruta, humanizada e **tendência** (cálculo vs. década anterior) |
| 6.2 Comparar dois nomes | `Joao` × `Maria` | Soma por nome em todas as décadas; totais humanizados; diferença **absoluta e percentual**; gráfico de barras ASCII/rich proporcional |
| 6.3 Ranking de década | (consultar 3 nomes antes) → década `2000` | Top 10 **ordenado por frequência bruta decrescente**, com humanização; usa só nomes já pesquisados no banco |
| 6.4 Resumo de um nome | `Joao` | Total, **década de pico** (correta vs. dados), prevalência "a cada X brasileiros" (X ≈ população/total, plausível para ~215 mi); resumo gravado no SQLite |
| 6.5 Faixa de frequência | `mais de 100 mil` (ou sintaxe equivalente do app) | Nomes da faixa listados; **limites da faixa apresentados de forma natural** via `humanize` |

**Robustez:** ⊘ nome `ZzqqXx99` (não existe); ⊘ década `2024` (sem dados).

### 5.7 — Trabalho 7: Relatório de Câmbio

- **Biblioteca-tempero:** `jinja2`
- **API sugerida:** `https://brasilapi.com.br/api/cambio/v1/cotacao` (ou endpoint de câmbio equivalente)

| Item | Entrada de teste (se executar) | Verificadores específicos (análise do código) |
|---|---|---|
| 7.1 Cotação atual | `USD` | Template **renderizado por jinja2** (`render`/`render_template_string` — não f-string puro); valor de compra/venda + data/hora gravados no SQLite; exibido em painel/markdown rich |
| 7.2 Relatório de variação | `USD`, `N=5` | Se há histórico: data, valor e **variação % vs. registro anterior** (verificar o cálculo no código); se não há: limitação informada explicitamente (ambos aceitáveis) |
| 7.3 Template customizado | `Hoje: {{ compra }} \| Previsão: {{ previsto }}` (adaptar às variáveis do app) | App solicita os valores, renderiza corretamente e grava o template no SQLite como `template_customizado` |
| 7.4 Listar histórico | filtro por moeda | Tabela rich; filtro funciona |
| 7.5 Comparar moedas | `USD` × `EUR` | Template de comparação renderizado ("1 X equivale a Y Z"); exibido em painel rich |

**Robustez:** ⊘ moeda `XYZ` (inexistente na API); ⊘ `N=0` no item 2.

### 5.8 — Trabalho 8: Busca Aproximada em Bancos

- **Biblioteca-tempero:** `thefuzz`
- **API sugerida:** `https://brasilapi.com.br/api/banks/v1`

| Item | Entrada de teste (se executar) | Verificadores específicos (análise do código) |
|---|---|---|
| 8.1 Sincronizar bancos | (sem entrada) | Total ≥ 100 bancos; schema com ISPB, nome, código, nome completo |
| 8.2 Busca por aproximação | `brasil`; depois `BANCO DO BRASL` (typo) | `thefuzz` (ex.: `fuzz.ratio`/`partial`) compara o termo com **todos** os nomes do banco; top 5 com **score 0–100**; score 100 → destacado como "correspondência exata" |
| 8.3 Código com tolerância | `341` (exato); depois `340` (typo) | Exato → score 100 destacado; typo → códigos similares com scores (similaridade aplicada aos códigos) |
| 8.4 Agrupar por similaridade | (sem entrada) | Similaridade par a par entre todos os nomes; grupos de alta similaridade com nome representativo |
| 8.5 Corrigir nome digitado | `banco do braxil` | Nome digitado, sugestão corrigida (esperada: Banco do Brasil) e **nível de confiança** exibidos |

**Robustez:** ⊘ busca vazia; ⊘ código `abc` (não numérico).

### 5.9 — Trabalho 9: Tabela FIPE

- **Biblioteca-tempero:** `num2words`
- **API sugerida:** `https://brasilapi.com.br/api/fipe/preco/v1/{codigoFipe}` (+ marcas/modelos)
- **Nota:** na execução (se feita), use os itens 2 e 3 para **descobrir um código FIPE válido** no próprio app antes de testar os itens 1 e 4. Na análise, verifique se o código aceita o fluxo marcas → modelos → preço.

| Item | Entrada de teste (se executar) | Verificadores específicos (análise do código) |
|---|---|---|
| 9.1 Preço por código | código válido + tipo | Tabela rich: veículo, ano, **preço numérico** e **preço por extenso** via `num2words` (verificar a conversão: 10000 → "dez mil reais"); código inválido → mensagem, sem crash |
| 9.2 Marcas por tipo | `carro` | Tabela: código da marca, nome, qtd. de modelos já consultados (se houver); marcas marcadas como metadados de catálogo no banco |
| 9.3 Modelos por marca | código de marca (do item 2) | Tabela: código, nome, preço médio dos anos consultados (se houver); vínculo à marca no banco |
| 9.4 Comparar dois veículos | 2 códigos válidos | Lado a lado: modelo, ano, preço numérico, **preço por extenso**, **diferença absoluta também por extenso**; indicação de mais caro/mais barato |
| 9.5 Histórico | filtro por marca (ou tipo/faixa) | Tabela com todas as colunas incl. extenso; filtros funcionam |

**Robustez:** ⊘ código `abc123` (inválido → mensagem, sem crash).

### 5.10 — Trabalho 10: Validação de Dados Corporativos

- **Biblioteca-tempero:** `validators`
- **API sugerida:** `https://brasilapi.com.br/api/cnpj/v1/{cnpj}`

| Item | Entrada de teste (se executar) | Verificadores específicos (análise do código) |
|---|---|---|
| 10.1 Validar/consultar CNPJ | `11222333000181` (dígitos válidos); depois ⊘ `11111111000111` (inválido) | `validators` confere o CNPJ **antes** da requisição (verificar a ordem no código); inválido → rejeitado sem chamada; válido → tabela rich com razão social, nome fantasia, situação cadastral; registro com data |
| 10.2 Validar site | `https://www.gov.br`; depois ⊘ `not a url` | `validators.url` (ou equivalente) usado; válida → salva com flag; inválida → recusada; extração do domínio principal |
| 10.3 Validar e-mail | `contato@gov.br` (domínio igual ao site validado no item 2) | `validators.email` usado; **correspondência com site já validado** no SQLite reportada |
| 10.4 Histórico de validações | filtros por tipo e por status | Tabela **unificada** (CNPJ/URL/e-mail); coluna de timestamp; filtros funcionam |
| 10.5 Estatísticas de conformidade | (sem entrada) | Painel rich com: totais válidos por tipo **e percentual de registros com os 3 tipos validados** (verificar a fórmula no código) |

**Robustez:** ⊘ CNPJ `123` (curto); ⊘ e-mail `abc@@dom`; ⊘ URL `http://` (incompleta).

### 5.11 — Trabalho 11: Previsão do Tempo

- **Biblioteca-tempero:** `emoji`
- **API sugerida:** `https://api.open-meteo.com/v1/forecast`

| Item | Entrada de teste (se executar) | Verificadores específicos (análise do código) |
|---|---|---|
| 11.1 Previsão atual | `São Paulo/SP` | Mapeamento código de clima → emoji **via `emoji`** (tabela/dict verificável no código); painel rich: cidade, temperatura, sensação térmica (se disponível), condição textual, emoji |
| 11.2 Próximos dias | `Rio de Janeiro/RJ`, `N=3` | 1 dia por registro no SQLite; tabela: data, mín, máx, condição, emoji |
| 11.3 Comparar duas cidades | `São Paulo/SP` × `Recife/PE` | Lado a lado; indicação de **mais quente**, **mais precipitação** e **diferença de temperatura** (verificar os cálculos) |
| 11.4 Alerta de extrema | `São Paulo/SP`, limites `10` a `20` | Se fora dos limites: alerta visual rich com emoji de alerta + temperatura; **registro no SQLite com status ativo/resolvido** |
| 11.5 Histórico | filtro por cidade e/ou condição | Tabela com todas as colunas incl. emoji; filtros funcionam |

**Robustez:** ⊘ `Xyz/XX` (cidade/UF inexistente → mensagem, sem crash); ⊘ `N=0`.

### 5.12 — Trabalho 12: Cadastros Fictícios

- **Biblioteca-tempero:** `faker`
- **API sugerida:** `https://viacep.com.br/ws/{cep}/json/`

| Item | Entrada de teste (se executar) | Verificadores específicos (análise do código) |
|---|---|---|
| 12.1 Cadastro por CEP | `01310100` | Perfil completo via `faker` (nome, CPF 11 dígitos, RG, telefone, e-mail, nascimento, profissão) + **endereço real do CEP**; painel rich; registro no banco vincula endereço real × dados fictícios (confirmar campos no schema/INSERT) |
| 12.2 Lote por cidade | `São Paulo/SP`, `N=5` | Estratégia de obter CEP válido para a cidade; 5 cadastros; resumo rich: total, distribuição por bairro (se houver), faixa etária |
| 12.3 Buscar por bairro | `Bela Vista` (bairro do CEP 01310-100) | Busca por substring no bairro no banco; tabela: nome, CPF, endereço, telefone; total encontrado |
| 12.4 Exportar | filtro por cidade → salvar em arquivo | Escrita de arquivo legível (formato livre); caminho exibido |
| 12.5 Estatísticas por localidade | (sem entrada) | Painel com múltiplas seções: total, **média de idade**, top 5 profissões, distribuição por domínio de e-mail (verificar os cálculos no código) |

**Robustez:** ⊘ CEP `99999999` (inválido); ⊘ cidade inexistente no item 2.

---

## 6. Modelo de `avaliado.md` (preencher integralmente)

**Onde:** raiz da pasta do trabalho (ex.: `/workspace/01/avaliado.md`).
**Idioma:** português do Brasil, obrigatório.
**Tom:** feedback construtivo ao aluno — cada decisão (ponto dado, ponto tirado, teto aplicado) deve vir acompanhada de explicação e referência concreta (`arquivo:linha` ou comportamento). O aluno deve conseguir corrigir o problema sem adivinhar o que foi apontado.

```markdown
# Avaliação — Trabalho [N]: [Título]

**Dupla:** [identificação]
**Data da avaliação:** [AAAA-MM-DD]
**Método:** [apenas análise estática / análise estática + execução parcial (o que foi executado)]

## 1. Resumo para a dupla
[2–4 frases: o que funciona bem, o principal problema, e a nota geral. Linguagem acessível.]

## 2. Veredito executivo
- Execução verificada? [SIM — o que foi testado / NÃO — apenas análise estática / NÃO EXECUTADA por X]
- API utilizada: [URL(s) — sugerida ou equivalente, com justificativa se alterada]
- Biblioteca-tempero usada efetivamente? [SIM — onde (arquivo:linhas) / NÃO — consequência (teto R3)]
- Regras de teto disparadas: [R1/R2/R3/R4/R5, ou "nenhuma" — explicar cada uma]

## 3. Grade com justificativas
| Seção | Cód. | Critério | Máx. | Pontuado | Justificativa para a dupla (arquivo:linha ou evidência + o que corrigir) |
|---|---|---|---|---|---|
| A | A1 | ... | 2 | ... | ... |
| ... | ... | ... | ... | ... | ... |
| E | 1.1 | Item 1.1 (E-a a E-e) | 10 | ... | ... |
| ... | ... | ... | ... | ... | ... |

> Toda linha com pontuação < máximo ou = 0 deve ter justificativa explicando o motivo e o que a dupla pode fazer para subir o ponto.

## 4. Análise por item obrigatório (1.1 a 1.5)
### Item [X.Y] — [nome]
- **Trilha no código:** entrada → fonte do dado → biblioteca-tempero → SQLite → rich, com `arquivo:linhas` de cada etapa.
- **Verificadores específicos:** [✓/✗ cada um, com justificativa quando ✗]
- **Subcritérios:** E-a __ / E-b __ / E-c __ / E-d __ / E-e __ (justificar cada parcial)
- **Execução (se feita):** entradas usadas + saída relevante (corte ~20 linhas)

(repetir para os 5 itens)

## 5. Banco de dados
- Tabelas e schema encontrado (ou "nenhum — consequência R4"): ...
- Registros (se `.db` commitado ou sandbox executado): contagens e amostra
- Campos exigidos presentes: [✓/✗ por campo relevante]

## 6. Robustez
| Input inválido (da lista 5.X) | Tratamento no código (arquivo:linha) | Verificado por execução? | Pts |
|---|---|---|---|
| ⊘ ... | ... | [sim/não] | ... |

Falha de API: [como está tratada no código; se executada, o que aconteceu]

## 7. Bônus
| Bônus | Implementado? | Evidência (arquivo:linha / demonstração) | Pts |
|---|---|---|---|

## 8. Resultado
- Subtotais: A __ · B __ · C __ · D __ · E __ · F __ · G __
- Tetos aplicados: [regras + explicação]
- **Total: __ / 100 → Nota: __ / 10**
- **Aprovado?** [≥ 70]

## 9. Mensagem para a dupla (obrigatório)
- **O que está bom** (pontos fortes concretos, com referência ao código):
- **O que corrigir primeiro** (priorizado, do mais impactante no total ao menos impactante; cada item com referência ao código e o que fazer):
- **Como a dupla pode conferir a correção** (o que testar/olhar para garantir que cada apontamento foi resolvido):
```

---

## 7. Casos-limite e convenções

1. **API fora do ar** (caso a execução tenha sido feita): E-b pontuado por análise — se o código faz `requests.get/post` real para API pública válida e faz o parse correto, conceda o ponto e registre "API indisponível no momento; verificado por código". E-e: se a exibição não pôde ser observada, 0,5 (código indica rich + campos corretos). **Nunca** desconte da dupla falha de serviço de terceiros; registre na seção 9 do `avaliado.md`.
2. **API alternativa à sugerida**: aceita sem penalidade, desde que pública e semanticamente equivalente (nota da Seção 5). Registre no relatório.
3. **Dados simulados**: aceitável **somente** onde a própria especificação permite (ex.: item 2 do Trabalho 7). Em qualquer outro lugar, simulação no lugar de API = violação de C4/R5 — explicar à dupla.
4. **`.db` commitado**: é evidência **complementar** de E-d, não primária — a evidência primária é o código de `INSERT`/`SELECT`. Se a execução foi feita no sandbox, confere registros **novos**. Banco commitado também é nota de higiene em A4.
5. **Menu com numeração/rótulos diferentes** da especificação: aceitável; o que vale é o comportamento. Confusão severa de navegação = E-a 0,5, justificado.
6. **Excesso de funcionalidade**: não pontue além da grade; mencione na seção 9.
7. **Código que só funciona no ambiente da dupla** (dependência não listada, caminho absoluto, shell específico): falha de A2 e/ou C4 conforme o caso; aplique tetos e explique.
8. **Tabela rich sem dados** por falta de registros: verifique o fluxo de persistência no código; se o caminho está correto mas o banco (commitado ou sandbox) ficou vazio por falha de execução, E-e 0,5 no item afetado, com justificativa.
9. **Subcritério em dúvida não resolvida pela análise**: executar é exatamente para isso — execute (Etapa 3). Se não for possível por motivo legítimo (custo desproporcional, API indisponível), atribua **0,5** e justifique explicitamente no `avaliado.md` ("não executado porque X; análise indica Y, mas não há certeza").
10. **Trabalho não identificado** (a dupla misturou elementos de dois trabalhos): avalie o trabalho cuja biblioteca-tempero e fluxos dominam o código, registre a ambiguidade na seção 2 e informe o impacto na seção 9.
