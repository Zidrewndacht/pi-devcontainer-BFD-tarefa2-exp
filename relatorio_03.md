# Relatório de Correção — Trabalho 3: Slug de Instituições Financeiras
**Identificação:** dupla não identificada / diretório `03/Slug e Normalização de Instituições Financeiras` (sem git; 5 arquivos `.py`, `requirements.txt`, `corretoras.db` commitado)
**Data da avaliação:** 2026-09-15

## 1. Veredito executivo
- **Executa? SIM** — via `/tmp/venv03/bin/python main.py` (menu interativo, loop funcional, exit 0 em todos os cenários).
- **API utilizada:** `https://brasilapi.com.br/api/cvm/corretoras/v1` (a sugerida; `api.py:8`, `requests.get` + `timeout=10`, resposta parseada com `.json()` → lista de dicts). HTTP 200 confirmado no momento da avaliação.
- **Biblioteca-tempero efetivamente usada: SIM** — `slugify` (`normalizacao.py:2`), chamado na geração de slugs (itens 1, 3, 4) e no resultado persistido que os itens 2 e 5 consultam.
- **Regras de teto disparadas: nenhuma** (R1: `pip install -r` exit 0 em venv limpo; R2: executa; R3: slugify usado na lógica central; R4: SQLite opera; R5: API real).

## 2. Grade

| Seção | Cód. | Critério | Pts possíveis | Pontuado | Evidência |
|---|---|---|---|---|---|
| A | A1 | Projeto documenta/usa venv **e** ambiente via requirements roda o app | 2 | **0** | `ls -la`: sem README, sem `.gitignore`, sem pasta `venv` |
| A | A2 | `requirements.txt` funcional em venv limpo | 4 | **4** | `pip install -r requirements.txt` → `EXIT_PIP_INSTALL=0`; `pip check` → `No broken requirements found` (exit 0). Obs.: arquivo codificado em **UTF-16 LE** (ver §8) — instalou assim mesmo no pip 26 |
| A | A3 | Lista `requests`, `rich` e `python-slugify` | 2 | **2** | `requirements.txt` contém `requests==2.34.2`, `rich==15.0.0`, `python-slugify==8.0.4` |
| A | A4 | `.gitignore` com venv/db | 2 | **0** | `.gitignore` inexistente; além disso `corretoras.db` (372 linhas) foi commitado (rubrica §7.4: ponto de higiene) |
| B | B1 | ≥3 módulos não vazios, um deles ponto de entrada | 2 | **2** | `main.py` (10 funções), `api.py` (1), `banco.py` (6), `normalizacao.py` (3); entrada = `main.py` |
| B | B2 | Módulo com funções reutilizáveis | 2 | **2** | `banco.py` (6 funções de BD), `api.py` e `normalizacao.py` reutilizados por `main.py` |
| B | B3 | `if __name__ == "__main__":` com lógica delegada | 2 | **2** | `main.py:209: if __name__ == "__main__": main()` |
| B | B4 | 3 tipos de import (built-in, local, pip) | 2 | **2** | built-in: `sys`, `sqlite3`, `re`; local: `from api import…`, `from banco import…`, `from normalizacao import…`; pip: `requests`, `rich`, `slugify` |
| B | B5 | Dicionários no fluxo de dados | 2 | **2** | `main.py:46-52`: `dados_corretora = {"cnpj":…, "codigo":…, "nome":…, "status":…, "slug":…}`; resposta da API = lista de dicts |
| C | C1 | Condicionais, loops, operadores lógicos/aritméticos significativos | 2 | **2** | `if/elif` no menu; `for` em 375 registros; `or` (`main.py:146,160`), `not` (vários); aritmética `posicao - 1`, `posicao + 2`, `max/min` (`banco.py:76-81`) |
| C | C2 | Funções com responsabilidade definida, sem monólito | 2 | **2** | Maior função: `sincronizar()` (~45 linhas); BD isolado em `banco.py`, API em `api.py`, slugs em `normalizacao.py` |
| C | C3 | SQLite de fato usado (schema, INSERT, SELECT; registros no `.db`) | 3 | **3** | DB **nova** (sem o commitado): após sync, `COUNT(*) = 372`; `PRAGMA table_info` → `cnpj, codigo, nome_original, slug, status`; `WHERE slug LIKE '%itau%'` = 5; `LIKE 'b%'` = 43; `LIKE 'z%'` = 0 |
| C | C4 | Dados externos exclusivamente via `requests.get` p/ API real, parse dict, sem hardcoded | 3 | **3** | `api.py:8`: único acesso a dados externos (`requests.get(API_URL, timeout=10)`); `.json()` → dicts; nenhum dataset embutido |
| D | D1 | `rich` para toda apresentação estruturada | 3 | **3** | Painel do título (`Panel.fit`), tabelas rich em sync/busca/export, observadas na execução |
| D | D2 | `print()` simples não usado para dados estruturados | 2 | **2** | Único `print(` fora do rich: `api.py:12` (mensagem de erro da API — não é dado estruturado) |
| E | E-3.1 | Item 1.1 — Sincronizar/slugificar | 10 | **8,5** | §3, item 3.1 (E-e 0,5: coluna CNPJ ausente na tabela) |
| E | E-3.2 | Item 1.2 — Buscar por slug | 10 | **7,0** | §3, item 3.2 (E-b 0,5: "mais próximos lexicograficamente" falha no caso `zzzqqq`; E-c 0,5: slugify não invocado na lógica do item) |
| E | E-3.3 | Item 1.3 — Normalizar nome livre | 10 | **8,5** | §3, item 3.3 (E-e 0,5: "versão limpa" não remove S.A. no input da rubrica) |
| E | E-3.4 | Item 1.4 — Comparar nomes | 10 | **10,0** | §3, item 3.4 (todos os verificadores ✓) |
| E | E-3.5 | Item 1.5 — Exportar por inicial | 10 | **8,5** | §3, item 3.5 (E-c 0,5: slugify não invocado na lógica do item) |
| F | F1 | ≥3 inputs inválidos sem traceback, msg + retorno ao menu | 3 | **3** | ⊘ busca vazia, ⊘ inicial `1`, ⊘ comparação com nome vazio — todos sem traceback, mensagem + menu (1 pt cada) |
| F | F2 | Falha de API tratada, app continua utilizável | 2 | **2** | Rede bloqueada (proxy morto): msg amigável, sem traceback, busca subsequente funciona |
| G | G | Bônus demonstrados | 10 | **0** | Nenhum dos 3 bônus implementado (sem coluna `categoria`, sem índice invertido, sem URLs ricas) |

## 3. Testes dinâmicos por item
Executados em copy de trabalho (`/tmp/eval03work`) com **`corretoras.db` nova** (o `.db` commitado não conta como evidência, §7.4), dentro de `venv03` (limpo, requirements instalados).

### Item 3.1 — Sincronizar/slugificar
- Entradas: menu `1` (sem input).
- Saída (corte):
```
Total sincronizado com sucesso: 375
Nomes que precisaram de normalização: 271
┌ Código ┬ Nome ┬ Slug ┬ Status ┐  (tabela rich, exatamente 10 linhas: 4UM DTVM, ABC BRASIL…, ABERTURA CCVM, ABN AMRO, AÇÃO S.A., …)
```
- Verificadores específicos:
  - ✓ Total sincronizado reportado (375 = nº de itens da API; 372 linhas no banco p/ 3 CNPJs duplicados na API, mesclados por `INSERT OR REPLACE` — verificado).
  - ✓ Contagem de normalização **consistente**: recomputei independentemente (`slugify(nome) != nome.lower().replace(" ","-")`) → **271**, idêntico ao reportado.
  - ✗ Tabela rich das 10 primeiras com **código, nome, slug, CNPJ, status** → colunas exibidas: Código, Nome, Slug, Status — **CNPJ ausente**.
- Subcritérios: E-a **2** (nenhum input exigido, conforme spec) / E-b **2** (API real, 375 itens ao vivo) / E-c **2** (slugify em cada nome) / E-d **2** (372 registros no `.db` novo, campos cnpj/codigo/nome_original/slug/status) / E-e **0,5** (tabela rich presente, 10 linhas, mas sem CNPJ) → **8,5**

### Item 3.2 — Buscar por slug
- Entradas: `2` → `itau`; depois `2` → `zzzqqq`.
- Saída (corte):
```
Resultados para: 'itau'   → 5 linhas (ITAU CORRETORA DE VALORES SA, ITAÚ INVESTMENT SOLUTIONS S.A., ITAU-BBA CTVM S.A., ITAUBANK CCTVM S/A, ITAUVEST S.A. CVM) — todos os slugs contêm 'itau'
Resultados para: 'zzzqqq' → linhas: 4um-dtvm-s-a | abc-brasil-distribuidora-de-titulos-e-valores-mobiliarios-s-a
```
- Verificadores específicos:
  - ✓ `itau` → ≥1 resultado contendo o termo (5).
  - ✗ `zzzqqq` → sem correspondência → **deveria listar os slugs mais próximos lexicograficamente**; como `zzzqqq` é maior que todos os slugs (máximo no banco: `xp-investimentos-cctvm-s-a`), os mais próximos seriam os **últimos** (`xp-investimentos…`, `warren-corretora…`). O app devolveu os **primeiros** em ordem alfabética — bug em `banco.py:62-74` (`posicao` permanece 0 quando nenhum slug ≥ alvo; `return todos[max(0,posicao-1):posicao+2]` vira `todos[0:2]`).
- Subcritérios: E-a **2** / E-b **0,5** (fallback "mais próximos" funcionalmente errado no caso testado) / E-c **0,5** (slugify não é invocado na lógica do item — a busca opera sobre slugs gerados por ele no item 1) / E-d **2** (SELECT no SQLite, 5 registros confirmados no banco) / E-e **2** (tabela rich com todos os campos nos dois casos) → **7,0**

### Item 3.3 — Normalizar nome livre
- Entradas: `4` → `  BANCO   DO   BRASIL   S.A. ` (exatamente como na rubrica).
- Saída (corte):
```
Nome original: BANCO   DO   BRASIL   S.A.
Slug gerado: banco-do-brasil-s-a
Versão limpa (sem sufixos): BANCO DO BRASIL S.A.
```
- Verificadores específicos:
  - ✓ Slug ASCII lowercase com hífens, sem espaços (`banco-do-brasil-s-a`).
  - ✗ Versão "limpa" **sem sufixo corporativo (S.A./LTDA)** → **S.A. NÃO foi removido**. Causa raiz: em `normalizacao.py:10-16` o padrão `r"\bS\.A\.\b"` exige fronteira de palavra **após** o último ponto; com "S.A." seguido de espaço ou fim de linha (casos gerais) não há `\b` → o regex nunca casa. O padrão `r"\bSA\b"` não casa com "S.A.". (Sufixos sem ponto, ex. LTDA, funcionam — `ABERTURA CCVM LTDA` → slug `abertura-ccvm-ltda` etc.)
- Subcritérios: E-a **2** / E-b **2** (item local, sem API) / E-c **2** (slugify gera o slug no fluxo central) / E-e **0,5** (3 campos exibidos com rich color, mas comportamento exigido — limpeza do sufixo — falha no input da rubrica) / E-d **2** (spec não exige persistência neste item) → **8,5**

### Item 3.4 — Comparar nomes
- Entradas: `5` → `XP Investimentos` × `xp investimentos`; depois `5` → `Banco do Brasil S.A.` × `XP`.
- Saída (corte):
```
Os slugs são idênticos! Refere-se à mesma instituição.
Os slugs são diferentes. São instituições distintas.
```
- Verificadores específicos: ✓ 1º par → "mesma instituição" (slugs idênticos, `xp-investimentos`); ✓ 2º par → diferentes (`banco-do-brasil-s-a` vs `xp`).
- Subcritérios: E-a **2** / E-b **2** (item local) / E-c **2** (slugify nos dois nomes) / E-d **2** (sem persistência exigida) / E-e **2** (mensagens rich coloridas corretas nos dois casos) → **10,0**

### Item 3.5 — Exportar por inicial
- Entradas: `6` → `b`; depois `6` → `z`.
- Saída (corte):
```
Slugs Iniciados com a Letra 'B' → tabela rich (BANRISUL, BANTRIAL, BARCLAYS, BATTISTELLA, …)
Total encontrado: 43
Nenhuma instituição inicia com a letra 'Z'.
```
- Verificadores específicos: ✓ Tabela + quantidade total (`b` → 43, **confere com `SELECT COUNT(*) WHERE slug LIKE 'b%'` = 43**); ✓ `z` → 0 resultados tratado graciosamente (sem crash, mensagem amigável, retorno ao menu).
- Subcritérios: E-a **2** / E-b **2** (filtro SQLite) / E-c **0,5** (slugify não invocado na lógica do item — filtra slugs que são produto dele) / E-d **2** (consulta confirmada no banco) / E-e **2** (tabela rich + total; caso vazio tratado) → **8,5**

## 4. Banco de dados
- Tabelas: `instituicoes` (criada por `criar_tabela()` na DB nova de teste).
- Contagem por tabela: `instituicoes` = **372** linhas após o sync (375 itens da API − 3 CNPJs duplicados).
- Campos exigidos presentes: ✓ `cnpj` (PK), ✓ `codigo` (código CVM), ✓ `nome_original`, ✓ `slug`, ✓ `status`.
- Registros novos confirmados pelos fluxos: 5 slugs com `itau`, 43 com inicial `b`, 0 com `z`; slugs com acentos normalizados (ex. `ABC BRASIL DISTRIBUIDORA DE TÍTULOS…` → `abc-brasil-distribuidora-de-titulos…`).
- Nota: o `corretoras.db` commitado (372 linhas) **não** foi usado como evidência (§7.4).

## 5. Robustez
| Input inválido | Comportamento | Traceback? | Pts |
|---|---|---|---|
| ⊘ busca vazia (item 2) | "O termo de busca não pode ser vazio." + retorno ao menu | não | 1 |
| ⊘ inicial `1` (item 5) | "Por favor, digite apenas uma única letra válida." + retorno ao menu | não | 1 |
| ⊘ comparação com nome vazio (item 4) | "Ambos os nomes devem ser preenchidos." + retorno ao menu | não | 1 |
| Falha de API (item 1, proxy `127.0.0.1:9` bloqueando a rede) | "Erro ao conectar com a API: …" + "Falha ao obter dados da API ou lista vazia."; app continua utilizável (busca `itau` funciona em seguida) | não | 2 |

## 6. Bônus
| Bônus | Demonstrado? | Evidência | Pts |
|---|---|---|---|
| Categoria inferida do slug (coluna `categoria` + estatísticas) | Não | `PRAGMA table_info`: só `cnpj, codigo, nome_original, slug, status` | 0 |
| Índice invertido palavra→instituições | Não | nenhuma tabela adicional no schema | 0 |
| URLs fictícias clicáveis (rich links) | Não | nenhum uso de `Link`/URL em `main.py` | 0 |

## 7. Resultado
- Subtotais: A **6**  B **10**  C **10**  D **5**  E **42,5**  F **5**  G **0**
- Tetos aplicados: **nenhum** (R1–R5 não dispararam)
- **Total: 78,5 / 100 → Nota: 7,85 / 10**
- **Aprovado? SIM (≥ 70)**

## 8. Observações qualitativas
- **Pontos fortes:**
  - Arquitetura limpa e bem modulada (API / banco / normalização / entrada), com parametrização SQL (`?`) e `timeout` na API.
  - Contagem de "normalização" auditável e exata (271 reproduzido independentemente).
  - Robustez completa no esperado (3 inputs inválidos + falha de API, zero tracebacks, app sempre utilizável).
  - Slugs corretamente gerados por `python-slugify` (acentos, pontuação, caixa).
- **Problemas principais:**
  1. **`versao_antiga.py` commitado**: versão anterior monolítica com `if __name__` próprio, duplicando toda a lógica antiga (clutter de repositório; não interfere na execução do `main.py`).
  2. **Bug do "mais próximos lexicograficamente"** (`banco.py`): para termo maior que todos os slugs (exatamente o caso de teste `zzzqqq`), devolve os primeiros em ordem alfabética em vez dos últimos.
  3. **Bug da "versão limpa"** (`normalizacao.py`): `r"\bS\.A\.\b"` nunca casa com "S.A." seguido de espaço/fim de linha → o sufixo corporativo mais comum não é removido no teste da própria rubrica.
  4. **Coluna CNPJ ausente** na tabela das 10 primeiras do item 1 (exigida pela rubrica).
  5. Item extra fora da spec (menu 3 — "Listar por status"): funcional e sem prejuízo, mas não pontuado (§7.6).
- **Pendências/limitações de higiene (não penalizadas além do que a grade prevê):**
  - `requirements.txt` codificado em **UTF-16 LE com CRLF**: instalou normalmente no pip 26.2.1 (exit 0), mas é um risco de portabilidade — pip/versões/entornos mais antigos podem falhar a parse. Recomenda-se regravar em UTF-8.
  - Sem README e sem `.gitignore` (perde A1 e A4); `corretoras.db` populado commitado (higiene, §7.4).
  - API BrasilAPI disponível durante toda a avaliação (HTTP 200) — nenhum item dependeu da convenção de API fora do ar (§7.1).
