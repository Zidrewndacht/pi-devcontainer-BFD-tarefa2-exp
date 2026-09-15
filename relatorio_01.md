# Relatório de Correção — Trabalho 1: Gestão de Feriados Nacionais
**Identificação:** pasta `01/` (sem dupla/commit informados)
**Data da avaliação:** 2026-09-15 (data do sistema do ambiente de avaliação)

## 1. Veredito executivo
- **Executa? SIM** — `main.py` inicia, menu funcional, API acessível.
- **API utilizada:** `https://brasilapi.com.br/api/feriados/v1/{ano}` (a sugerida, sem alteração).
- **Biblioteca-tempero efetivamente usada: SIM** — `dateutil.parser.parse` em `dates.py` (`converter_data`), usada no parse de entradas e datas da API (itens 1–4). **Porém com bug grave:** `dayfirst=True` aplicado a datas ISO (`YYYY-MM-DD`) da API troca mês/dia quando ambos ≤ 12, corrompendo 11 de 28 registros gravados.
- **Regras de teto disparadas: nenhuma** (R1–R5 não se aplicam: requirements OK, app executa, dateutil é usada na lógica, SQLite opera, API real).

## 2. Grade

| Seção | Cód. | Critério | Pts possíveis | Pontuado | Evidência |
|---|---|---|---|---|---|
| A | A1 | venv documentado + ambiente via requirements roda a aplicação | 2 | 2 | `.gitignore` contém `/venv`; app executado em venv limpo criado com `pip install -r requirements.txt` (seções 3–5) |
| A | A2 | `pip install -r` exit 0 em venv limpo, runtime completo | 4 | 4 | `pip install` exit 0; `pip check` → "No broken requirements found" (exit 0); app importou requests/rich/dateutil sem falha |
| A | A3 | requirements lista `requests`, `rich` e `python-dateutil` | 2 | 2 | `requests==2.34.2`, `rich==15.0.0`, `python-dateutil==2.9.0.post0` (+ transitive) |
| A | A4 | `.gitignore` com venv (obrigatório) e .db (bom ponto) | 2 | 1,5 | `.gitignore` = só `/venv`; o `feriados.db` criado em runtime não é ignorado |
| B | B1 | ≥ 3 módulos .py não vazios + ponto de entrada | 2 | 2 | 6 módulos: `api.py`(11l), `database.py`(203l), `dates.py`(49l), `display.py`(143l), `main.py`(6l), `menu.py`(310l) |
| B | B2 | Módulo com funções reutilizáveis | 2 | 2 | `database.py` (conectar/CRUD usado em todo o menu), `dates.py` (parse/intervalo), `api.py` |
| B | B3 | `if __name__ == "__main__":` com delegação | 2 | 2 | `main.py:5-7`: `criar_tabela(); iniciar()` |
| B | B4 | 3 tipos de import | 2 | 2 | built-in: `sqlite3`, `datetime`; local: `from database import ...`; pip: `requests`, `rich`, `dateutil` |
| B | B5 | Dicionários no fluxo de dados | 2 | 2 | `menu.py` item 1: `feriado["date"]`, `feriado["name"]`, `feriado["type"]` (lista de dicts da API); item 3: dict `{"nome","data","dia_semana","dias"}` |
| C | C1 | Condicionais/loops/lógicos/aritméticos significativos | 2 | 2 | `while atual <= fim` + `atual += timedelta(days=1)`; `eh_dia_util(dia) and dia_iso not in datas_feriados`; `if not ano`/`if not feriados`; `{-diferenca}`, `(data-hoje).days` |
| C | C2 | Funções com responsabilidade definida, sem monólito | 2 | 2 | Lógica dividida em 5 módulos; `iniciar()` (menu.py) é dispatcher de menu (~250 linhas) mas cada item delega parse/consulta/exibição a funções de outros módulos (observação registrada) |
| C | C3 | SQLite real: schema, INSERT no fluxo, SELECT p/ exibição, registros no .db | 3 | 3 | `CREATE TABLE IF NOT EXISTS feriados(...)`; `INSERT` em `inserir_feriado` (com `UNIQUE` + `IntegrityError`); `SELECT` em todos os itens; `sqlite3 feriados.db "SELECT COUNT(*)..."` → 28 registros (14/2025, 14/2026) |
| C | C4 | Dados externos exclusivamente via requests + parse, sem hardcode | 3 | 3 | `api.py`: `requests.get(f"https://brasilapi.com.br/api/feriados/v1/{ano}")` → `resposta.json()`; nenhum dataset hardcoded (confirmado por grep e tráfego real durante os testes) |
| D | D1 | rich para toda apresentação estruturada | 3 | 3 | Tables rich em: resumo de importação, lista de feriados, próximos feriados, dias úteis (título + cores + colunas) — visível na execução |
| D | D2 | Sem print() simples p/ dados estruturados | 2 | 2 | `grep -rn "print(" --include=*.py | grep -v "console.print"` → vazio; menu usa `console.print` + `input()` (aceitável) |
| E | E-1.1a..e | Item 1.1 | 10 | 7 | Ver seção 3 |
| E | E-1.2a..e | Item 1.2 | 10 | 7 | Ver seção 3 |
| E | E-1.3a..e | Item 1.3 | 10 | 8,5 | Ver seção 3 |
| E | E-1.4a..e | Item 1.4 | 10 | 8,5 | Ver seção 3 |
| E | E-1.5a..e | Item 1.5 | 10 | 8,5 | Ver seção 3 |
| F | F1 | ≥ 3 inputs inválidos sem traceback | 3 | 3 | 4/4 da lista 5.1 tratados (seção 5) |
| F | F2 | Falha de API tratada | 2 | 0 | Rede bloqueada → `requests.exceptions.ProxyError` com traceback completo, app morre (seção 5) |
| G | G | Bônus demonstrados | 10 | 0 | Menu contém apenas os itens 1–5 + sair; nenhum bônus específico (cadastro manual, calendário ASCII, alerta) nem geral (export, batch, dashboard, config, testes, logging) no código |

## 3. Testes dinâmicos por item

### Item 1.1 — Consultar/armazenar ano
- **Entradas:** `1` → `2025` (execução 1); `1` → `2025` (execução 2, duplicatas)
- **Saída (corte):**
  ```
  Resumo da Importação
  ┏━━━━━━━━━━━┳━━━━━━━━━━━━━┓
  ┃ Inseridos ┃ Já Existiam ┃
  ┡━━━━━━━━━━━╇━━━━━━━━━━━━━┩
  │    14     │      0      │   ← 1ª execução
  │     0     │     14      │   ← 2ª execução
  └───────────┴─────────────┘
  ```
  Tabela rich com colunas Ano | Data | Nome | Tipo | Dia da Semana (14 linhas p/ 2025).
- **Verificadores específicos:** ✓ nº inserido × já existente; ✓ 2ª execução → 0 inseridos; ✓ tabela rich com ano, data, nome, tipo, dia da semana (campos presentes).
- **⚠ Falha de dados:** as datas gravadas não batem com a API. A API (ISO) retornou `2025-05-01` (Dia do trabalho), `2025-11-02` (Finados), `2025-10-12` (N.S. Aparecida), `2025-03-04` (Carnaval), mas o banco contém `2025-01-05`, `2025-02-11`, `2025-12-10`, `2025-04-03` — 4/14 corrompidos. Causa (provada em teste isolado): `parse("2025-05-01", dayfirst=True)` → `2025-01-05` — o `dayfirst=True` de `converter_data` (dates.py) troca mês/dia da data ISO da API. Em 2026 a corrupção afeta 7/14 (Páscoa→05-04, Dia do trabalho→01-05, Independência→07-09, N.S. Aparecida→12-10, Finados→02-11, Corpus→04-06, Sexta-feira Santa→03-04).
- **Subcritérios:** E-a 2 / E-b 2 / E-c 0,5 (dateutil usado, mas o parse corrompe a data — falha relevante) / E-d 0,5 (registros existem com os campos, mas `data` errada em 4/14 de 2025) / E-e 2

### Item 1.2 — Status de uma data
- **Entradas:** `25/12/2026`; `2026-12-25`; `25 de dezembro de 2026`; `15/02/2026` (domingo); `17/01/2026`; `07/01/2026`
- **Saída (corte):**
  ```
  FERIADO / Natal / Faltam 101 dias.        ← 25/12/2026 ✓ (101 dias exato)
  FERIADO / Natal / Faltam 101 dias.        ← 2026-12-25 ✓
  Data inválida.                            ← "25 de dezembro de 2026" ✗
  FIM DE SEMANA                             ← 15/02/2026 ✓
  FIM DE SEMANA                             ← 17/01/2026 (sábado — ver observação)
  DIA ÚTIL                                  ← 07/01/2026 (quarta) ✓
  ```
- **Verificadores específicos:** ✗ "os 3 formatos aceitos" (apenas 2: `parse("25 de dezembro de 2026")` → `ParserError`); ✓ Natal → feriado + nome + dias restantes; ✓ domingo → fim de semana; ✓ dia útil (com `07/01/2026`, quarta-feira).
- **⚠ Nota (erro da rubrica):** a rubrica rotula `17/01/2026` como "terça, útil", mas 17/01/2026 é **sábado** (1º/1/2026 = quinta). A resposta do app ("FIM DE SEMANA") é a correta; o caso de "dia útil" foi validado com `07/01/2026`.
- **⚠ Consequência do bug:** `05/01/2026` (Dia do trabalho real) → **"FERIADO / Dia do trabalho / Passaram 253 dias"** (registrado como 2026-01-05); `05/01/2025` → "FERIADO / Passaram 618 dias" (registrado como 2025-01-05). Respostas erradas para feriados reais com mês ≤ 12.
- **Subcritérios:** E-a 0,5 (2/3 formatos) / E-b 2 (consulta ao SQLite, conforme spec) / E-c 2 (dateutil faz o parse da entrada) / E-d 0,5 (consulta correta, mas o banco tem datas corrompidas → respostas inconsistentes, ex. acima) / E-e 2 (rich com status colorido, nome e dias)

### Item 1.3 — Próximos feriados
- **Entradas:** `3` → `3`
- **Saída (corte):**
  ```
  Próximos Feriados
  Nome                      Data        Dia da Semana  Dias Restantes
  Proclamação da República  2026-11-15  Domingo        61
  Dia da consciência negra  2026-11-20  Sexta-feira    66
  Nossa Senhora Aparecida   2026-12-10  Quinta-feira   27
  ```
- **Verificadores específicos:** ✓ exatamente 3 linhas com nome, data, dia da semana, dias restantes; ✓ contagem via dateutil (61 e 66 exatos).
- **⚠ Inconsistências:** N.S. Aparecida real é 10/12/2026 (passou em relação a 15/09); o banco tem 12/10 (corrompido), exibido como futuro. Além disso, a linha mostra data `2026-12-10` mas "27 dias restantes" — a contagem re-parseia a data com `dayfirst` (12/10 → 10/12), ficando inconsistente com a data exibida (86 dias).
- **Subcritérios:** E-a 2 / E-b 2 (banco, conforme spec) / E-c 2 (dateutil no parse e na contagem) / E-d 0,5 (registros lidos corrompidos) / E-e 2 (tabela com todos os campos, 3 linhas)

### Item 1.4 — Dias úteis entre duas datas
- **Entradas:** `4` → `01/02/2026` → `28/02/2026`
- **Saída (corte):**
  ```
  Dias úteis encontrados: 17
  Feriados no período
  2026-02-11  Finados        ← errado (Finados real: 11/02/2026)
  2026-02-16  Carnaval
  2026-02-17  Carnaval
  ```
- **Verificadores específicos:** ✗ total exato — recalculado pelo avaliador: 28 dias − 8 de fim de semana (fev/2026 começa em domingo) − 2 feriados reais (Carnaval 16 e 17) = **18**; o app exibe **17** por descontar o Finados corrompido (02/11). ✓ lista dos feriados no período (tabela rich).
- **Subcritérios:** E-a 2 / E-b 2 / E-c 2 (dateutil no parse + iteração do intervalo) / E-d 0,5 (verificador de total exato falhou; causa: registros corrompidos) / E-e 2

### Item 1.5 — Listar armazenados
- **Entradas:** `5` → `2025`; depois `5` → ENTER (todos)
- **Saída:** tabela rich somente 2025 (14 linhas); sem filtro → 28 linhas (2025+2026).
- **Verificadores específicos:** ✓ tabela rich somente 2025; ✓ filtro por ano funciona. (Dados exibidos herdam a corrupção de 1.1 — já penalizado em E-d/E-c do item 1.1 e em E-d deste item.)
- **Subcritérios:** E-a 2 / E-b 2 / E-c 2 (item de listagem: a spec do item 5 não exige a biblioteca-tempero; nenhum uso indevido — critério atendido sem violação) / E-d 0,5 (consulta OK, mas 4/14 linhas de 2025 com data errada) / E-e 2

## 4. Banco de dados
- **Tabelas:** `feriados` (id INTEGER PK AUTOINCREMENT, ano INT, data TEXT UNIQUE, nome TEXT, tipo TEXT, dia_semana TEXT)
- **Contagem:** 28 total (14 em 2025, 14 em 2026) — todos criados pelos fluxos testados (banco limpo no início).
- **Campos exigidos presentes:** ✓ ano, data, nome, tipo, dia_semana
- **Integridade:** ✗ 11/28 registros com `data` incorreta (4/14 em 2025; 7/14 em 2026) — bug de `dayfirst=True` sobre datas ISO da API.

## 5. Robustez

| Input inválido | Comportamento | Traceback? | Pts |
|---|---|---|---|
| ⊘ ano `abc` | "Ano inválido." → menu | Não | 1 |
| ⊘ ano `999` | "Nenhum dado encontrado." (API 404 tratada por `status_code`) → menu | Não | 1 |
| ⊘ data `31/02/2026` | "Data inválida." → menu | Não | 1 |
| ⊘ data vazia | "Data inválida." → menu | Não | 1 |
| ⊘ (extra) `3`→`abc` | "Informe um número válido." | Não | — |
| ⊘ (extra) `5`→`xyz`; opção `9` | "Ano inválido." / "Opção inválida." | Não | — |
| **Falha de API** (rede bloqueada via proxy inválido, item 1) | `requests.exceptions.ProxyError` + traceback completo; **aplicação termina** | **SIM** | **0 (F2)** |

F1 = 3/3 · F2 = 0/2

## 6. Bônus

| Bônus | Demonstrado? | Evidência | Pts |
|---|---|---|---|
| Específicos (cadastro manual, calendário ASCII, alerta de proximidade) | Não | Menu com apenas opções 1–5/0; grep sem código correspondente | 0 |
| Gerais (export, batch, dashboard, config, testes, logging) | Não | idem | 0 |

## 7. Resultado
- **Subtotais:** A **9,5** · B **10** · C **10** · D **5** · E **39,5** · F **3** · G **0**
- **Tetos aplicados:** nenhum (R1–R5 não dispararam)
- **Total: 77,00 / 100 → Nota: 7,7 / 10**
- **Aprovado?** SIM (≥ 70)

## 8. Observações qualitativas
- **Pontos fortes:** organização modular exemplar (6 módulos com responsabilidade clara); uso real da API sugerida com parse correto do payload; SQLite bem usado (UNIQUE + `IntegrityError` para o controle de duplicatas, consultas parametrizadas); exibição integralmente com `rich`; robusta contra inputs inválidos do menu (nenhum traceback); `requirements.txt` completo com versões pinadas (passa `pip check`).
- **Problemas principais:**
  1. **Bug central — `dayfirst=True` aplicado à data ISO da API** (`converter_data` em `dates.py`): `parse("2025-05-01", dayfirst=True)` → 05/01 em vez de 01/05. Corrompe 11 de 28 registros e propaga erros para os itens 2, 3 e 4 (total de dias úteis errado: 17 vs 18; feriados reais reportados como dia útil e vice-versa; linha de "próximos" com data e dias restantes inconsistentes). Correção simples: não usar `dayfirst` para as datas da API (ISO) — usar `parse` sem `dayfirst` (ou `date.fromisoformat`) para a API e `dayfirst=True` apenas para a entrada do usuário.
  2. Formato `25 de dezembro de 2026` rejeitado (`ParserError`) — a spec pede aceite de múltiplos formatos incluindo esse.
  3. Falha de rede na API não tratada → traceback e queda do app (F2).
  4. Nenhum bônus implementado (G = 0).
- **Pendências/limitações não testadas:** nenhuma API fora do ar; todos os itens executados em ambiente limpo.
- **Observações adicionais (sem impacto na nota):** a rubrica rotula `17/01/2026` como "terça" — é sábado (erro de calendário na rubrica; o app respondeu corretamente "FIM DE SEMANA"); `feriados.db` não está no `.gitignore`; `README.md` é mínimo e diz "Trabalho-2" (o código é do Trabalho 1); `database.py` contém pares de funções duplicadas não usadas (`buscar_feriados_periodo`/`feriados_no_periodo`, `buscar_proximos`/`proximos_feriados`, `listar_todos`/`listar_feriados`); ano `999` (3 dígitos) não é rejeitado na validação (chega à API e vira "Nenhum dado encontrado" — atende o critério F1, mas a spec pede "quatro dígitos").
