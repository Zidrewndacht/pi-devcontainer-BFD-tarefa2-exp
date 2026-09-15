# Relatório de Correção — Trabalho 8: Busca Aproximada em Instituições Bancárias
**Identificação:** dupla / diretório `./08` (main.py, api.py, database.py, matcher.py)
**Data da avaliação:** 2026-02-19

## 1. Veredito executivo
- Executa? **SIM** — `python main.py` no venv limpo roda o menu completo sem erros.
- API utilizada: `https://brasilapi.com.br/api/banks/v1` (a sugerida, sem alteração) — tráfego real confirmado (474 registros).
- Biblioteca-tempero efetivamente usada: **SIM** — `thefuzz.fuzz` (token_set_ratio, ratio, token_sort_ratio) em `matcher.py`, núcleo dos itens 2, 3, 4 e 5.
- Regras de teto disparadas: **nenhuma** (R1–R5 não se aplicam: requirements instala em venv limpo, app inicia, thefuzz é usado, SQLite opera, API real).

## 2. Grade
| Seção | Cód. | Critério | Pts possíveis | Pontuado | Evidência |
|---|---|---|---|---|---|
| A | A1 | venv documentado + ambiente roda | 2 | 0,5 | README.md contém apenas "# Busca_Bancos / Atividade_Curso" — sem instruções de venv; app roda via requirements, mas 1ª metade do critério ausente |
| A | A2 | requirements instala em venv limpo | 4 | 4 | `pip install -r ./08/requirements.txt` exit 0; `pip check` → "No broken requirements found" (exit 0); versões exatas: requests 2.31.0, rich 13.7.0, thefuzz 0.22.1 |
| A | A3 | requests, rich e thefuzz listados | 2 | 2 | `cat requirements.txt` → `requests==2.31.0`, `rich==13.7.0`, `thefuzz==0.22.1` (nomes corretos p/ Tr. 8) |
| A | A4 | .gitignore com venv | 2 | 0 | `ls -la ./08` → sem .gitignore (também sem .db commitado) |
| B | B1 | ≥3 módulos .py não vazios | 2 | 2 | 4 arquivos: api.py (1 fun.), database.py (3), matcher.py (3), main.py (7); entrada = main.py |
| B | B2 | módulo com funções reutilizáveis | 2 | 2 | `database.py`/`matcher.py`/`api.py` consumidos por main.py (import api, database, matcher — main.py:9-11) |
| B | B3 | `if __name__ == "__main__"` delegando | 2 | 2 | main.py:147 `if __name__ == "__main__": main()`; main() delega a acao_* |
| B | B4 | 3 tipos de import | 2 | 2 | built-in: `sqlite3`, `warnings`; local: `api`, `database`, `matcher`; pip: `requests`, `rich`, `thefuzz` |
| B | B5 | dicionários no fluxo | 2 | 2 | `dict(row)` (database.py:46), `banco.copy()` (matcher.py:23), `b.get(...)` (database.py:28), `response.json()` → lista de dicts (api.py:10) |
| C | C1 | condicionais/loops/logica/aritmética | 2 | 2 | `while True`, `for banco in bancos`, `or`/`and`/`not`, `i + 1`, `r["score"] > 40`, `len(grupo_atual) > 1` |
| C | C2 | funções com responsabilidade | 2 | 2 | máx. ~40 linhas por função; sem monólito (wc: main 148, matcher 73, database 46, api 12) |
| C | C3 | SQLite schema + INSERT + SELECT | 3 | 3 | schema `bancos(ispb TEXT, name TEXT, code INTEGER, fullName TEXT)`; `executemany INSERT`; `SELECT` via row_factory; 474 registros novos confirmados via `sqlite3` |
| C | C4 | dados externos só via requests | 3 | 3 | api.py:8 `requests.get(URL_API, timeout=10)` + `raise_for_status()` + `r.json()`; sem dataset hardcoded; 474 itens vieram da rede no teste |
| D | D1 | rich para dados estruturados | 3 | 3 | Table (resultados, códigos, grupos), Panel (menu, corretor), `console.status` spinner |
| D | D2 | print simples sem dado estruturado | 2 | 2 | único `print(` fora do console: api.py:12 (mensagem de erro de 1 linha, não estruturada) |
| E | E-8.1a..e | Item 1: Sincronizar | 10 | 10 | ver §3 |
| E | E-8.2a..e | Item 2: Busca por aproximação | 10 | 10 | ver §3 |
| E | E-8.3a..e | Item 3: Código com tolerância | 10 | 7 | ver §3 (E-c 0,5; E-e 0,5) |
| E | E-8.4a..e | Item 4: Agrupar | 10 | 10 | ver §3 |
| E | E-8.5a..e | Item 5: Corrigir nome | 10 | 10 | ver §3 |
| F | F1 | 3 inputs inválidos | 3 | 2,5 | ver §5 (vazio nome = 0,5) |
| F | F2 | falha de API tratada | 2 | 2 | ver §5 (proxy bloqueado) |
| G | — | Bônus (específicos e gerais) | 10 | 0 | menu tem só itens 1-5+0; sem exportação, batch, dashboard, config, testes ou logging (Seção 10); nenhum bônus do Tr. 8 |

## 3. Testes dinâmicos por item
Ambiente: venv limpo `/tmp/venv_eval` (criado com `--without-pip` + get-pip, por falta de `ensurepip` no container); projeto copiado para /tmp/eval8; `bancos.db` não existia antes da execução (registros abaixo são novos).

### Item 1.1 — Sincronizar bancos (entrada: opção 1)
- Saída:
```
Escolha uma opção [1/2/3/4/5/0] (0): ✓ Sucesso! 474 bancos sincronizados no banco local.
```
- Verificadores: total ≥ 100 ✓ (474); schema ISPB/nome/código/nome completo ✓ (`sqlite3 bancos.db "SELECT * FROM bancos WHERE code=341"` → `60701190|ITAÚ UNIBANCO S.A.|341|ITAÚ UNIBANCO S.A.`); resumo rich ✓ (Console com markup + spinner `console.status`).
- Subcritérios: E-a 2 / E-b 2 / E-c 2 (item de ingestão; thefuzz não é exigido aqui e é usado efetivamente nos itens 2–5, logo R3 não dispara) / E-d 2 / E-e 2

### Item 1.2 — Busca por aproximação (`brasil`; depois `BANCO DO BRASL`)
- Saída (1ª):
```
│ 1      │ BCO DO BRASIL S.A.                       │   100 │      EXATA      │
│ 136    │ UNICRED DO BRASIL                        │   100 │      EXATA      │
│ 747    │ BCO RABOBANK INTL BRASIL S.A.            │   100 │      EXATA      │
│ 350    │ COOPERATIVA DE CRÉDITO POPULAR DO BRASIL │   100 │      EXATA      │
│ 752    │ BCO BNP PARIBAS BRASIL S A               │   100 │      EXATA      │
```
- Saída (2ª, typo):
```
│ 1      │ BCO DO BRASIL S.A.       │  77 │  Parcial │
│ 63     │ BANCO BRADESCARD         │  73 │  Parcial │
│ 505    │ BCO UBS BRASIL           │  71 │  Parcial │
```
- Verificadores: top 5 com score 0–100 ✓; typo → "BCO DO BRASIL S.A." (Banco do Brasil) em 1º com score alto (77) ✓; score 100 → destacado como correspondência exata ✓ ("EXATA" em verde negrito; rótulo "EXATA" ≈ "correspondência exata" — comportamento presente).
- Subcritérios: E-a 2 / E-b 2 / E-c 2 / E-d 2 / E-e 2. Observação qualitativa: `token_set_ratio` atribui 100 a qualquer nome contendo o termo ("brasil" → 5 "EXATAs"), o que é um viés do algoritmo escolhido, não falha dos verificadores.

### Item 1.3 — Código com tolerância (`341`; depois `340`)
- Saída (341):
```
│ 341 │ ITAÚ UNIBANCO S.A.      │ 100% │
│ 41  │ BCO DO ESTADO DO RS S.A. │ 80% │
```
- Saída (340):
```
│ 40  │ BCO CARGILL S.A.          │ 80% │
│ 430 │ CCR SEARA                 │ 67% │
│ 407 │ SEFER INVESTIMENTOS...    │ 67% │
│ 330 │ BANCO BARI S.A.           │ 67% │
│ 534 │ EWALLY IP S.A.            │ 67% │
```
- Verificadores: exato → score 100 presente, **mas sem destaque visual** na tabela de códigos (coluna sem cor/etiqueta p/ 100, ao contrário do item 2) ✗→parcial; typo → códigos similares com scores ✓. **Problema funcional**: o caso canônico da especificação ("útil para typos como 340") não funciona bem — `fuzz.ratio('340','341') = 67`, e o código correto 341 **não aparece no top 5** (prejudicado por prefixos curtos como "40" = 80).
- Subcritérios: E-a 2 / E-b 2 / **E-c 0,5** / E-d 2 / **E-e 0,5**

### Item 1.4 — Agrupar por similaridade (sem entrada)
- Saída (corte):
```
│ BCO DO BRASIL S.A. │ • 1 - BCO DO BRASIL S.A. / • 76 - BCO KDB BRASIL S.A.
│ BANCO BARI S.A.    │ • 330 - BANCO BARI S.A. / • 334 - BANCO BESA S.A.
│ BCO. J.SAFRA S.A.  │ • 74 - BCO. J.SAFRA S.A. / • 422 - BCO SAFRA S.A.
```
- Verificadores: ≥1 grupo com ≥2 nomes similares ✓ (dezenas de grupos); nome representativo por grupo ✓; similaridade par a par via thefuzz ✓ (token_sort_ratio ≥ 85).
- Subcritérios: E-a 2 / E-b 2 / E-c 2 / E-d 2 / E-e 2. Observação qualitativa: falsos positivos esperados do corte 85 (ex.: BCO B3 × BCO BBI, CIELO × CELCOIN) — limite de qualidade, não de verificador.

### Item 1.5 — Corrigir nome digitado (`banco do braxil`)
- Saída:
```
│ Texto digitado: banco do braxil
│ Sugestão corrigida: BCO DO BRASIL S.A. (Banco do Brasil S.A.)
│ Nível de Confiança: 75%
```
- Verificadores: nome digitado ✓, sugestão ✓ (institução esperada "Banco do Brasil" — nome exato vem da API), nível de confiança ✓, painel rich ✓.
- Subcritérios: E-a 2 / E-b 2 / E-c 2 / E-d 2 / E-e 2

## 4. Banco de dados
- Tabelas: `bancos`
- Schema: `CREATE TABLE bancos (ispb TEXT, name TEXT, code INTEGER, fullName TEXT)`
- Contagem: **474** (corresponde ao total da API; banco criado durante a execução, sem dados prévios)
- Campos exigidos: ISPB ✓ nome ✓ código ✓ nome completo ✓ (ex.: `60701190|ITAÚ UNIBANCO S.A.|341|ITAÚ UNIBANCO S.A.`)
- Nota: 8 registros com `code IS NULL` (Selic, Bacen etc. — dados da API); app trata com "N/A" e skip, sem crash.

## 5. Robustez
| Input inválido | Comportamento | Traceback? | Pts |
|---|---|---|---|
| ⊘ Busca vazia (item 2, termo "") | Sem crash e retorno ao menu, **mas exibe tabela com 5 linhas todas score 0** em vez de mensagem "digite um termo" (saída enganosa) | Não | 0,5 |
| ⊘ Código `abc` | "Nenhum código similar foi encontrado." + menu | Não | 1,0 |
| ⊘ Código vazio (3º input, complementando lista 5.8 com 2 itens) | "Nenhum código similar foi encontrado." + menu | Não | 1,0 |
| ⊘ Falha de API (F2, rede bloqueada via proxy 127.0.0.1:9) | "Erro ao acessar a API: ...ProxyError..." + "❌ Falha ao sincronizar dados."; app continua utilizável e encerra sem erro | Não | 2,0 (F2) |

## 6. Bônus
| Bônus | Demonstrado? | Evidência | Pts |
|---|---|---|---|
| Autocorreção em lote (Tr. 8) | Não | menu só tem opções 1–5 e 0 | 0 |
| Quiz (Tr. 8) | Não | idem | 0 |
| Dicionário de sinônimos (Tr. 8) | Não | idem | 0 |
| Bônus gerais (Seção 10: export, batch, dashboard, config, testes, logging) | Não | nenhum módulo correspondente no diretório | 0 |

## 7. Resultado
- Subtotais: A **6,5**  B **10**  C **10**  D **5**  E **47**  F **4,5**  G **0**
- Tetos aplicados: **nenhum** (R1–R5 não dispararam)
- **Total: 83,0 / 100 → Nota: 8,3 / 10**
- **Aprovado? SIM** (≥ 70)

## 8. Observações qualitativas
- **Pontos fortes:**
  - Arquitetura limpa em 4 módulos com responsabilidades bem divididas (API / banco / similaridade / UI) — modelo de referência da aula.
  - `thefuzz` integrado de verdade ao fluxo (scores ordenados, filtros por corte, agrupa por pares).
  - Tratar de forma amigável: banco vazio, API fora do ar, resultados vazios — tudo sem traceback.
  - `pip check` limpo e pins exatos nos requirements.
- **Problemas principais:**
  1. **Busca por código (8.3)**: o exemplo canônico da spec falha — digitar `340` não traz `341` no top 5 (fuzz.ratio favorece prefixos: "40"=80 > "341"=67). Sugestão: comparar com distância de Hamming/numérica para códigos.
  2. **Sem destaque de "correspondência exata" na tabela de códigos** (100% sem cor/etiqueta), exigido pelo verificador 8.3.
  3. **Busca vazia** exibe tabela com scores 0 em vez de mensagem de aviso.
  4. `token_set_ratio` marca 100/"EXATA" para qualquer nome contendo o termo (ex.: "brasil" → 5 exatas) — viés de rótulo.
  5. Sem .gitignore (venv/.db não ignorados) e README praticamente vazio (sem instruções de setup) → A1 parcial, A4 zero.
- **Pendências/limitações não testadas:** nenhuma — API disponível durante toda a avaliação; todos os itens e os testes de robustez foram executados dinamicamente.
