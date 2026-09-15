# Relatório de Correção — Trabalho 2: Telefones Brasileiros
**Identificação:** dupla 02 (repositório `./02`)
**Data da avaliação:** 2026-09-15

## 1. Veredito executivo
- **Executa? SIM** — `python main.py` roda em venv limpo (exit 0 em todos os fluxos testados).
- **API utilizada:** `https://brasilapi.com.br/api/ddd/v1/{ddd}` (a sugerida, sem alteração; tráfego real confirmado durante a avaliação).
- **Biblioteca-tempero efetivamente usada: SIM** — `phonenumbers` no parse/validação/formatação (itens 1, 5), validação dos números gerados (item 3) e geocoder. **Não** é usada na validação do DDD no item 2 (lista local em `config.py`).
- **Regras de teto disparadas: nenhuma.**
- Nota: o repositório contém também `Validar_e_Consultar.py`, versão anterior com apenas 2 dos 5 itens (código morto no fluxo `main.py`). Avaliado o ponto de entrada `main.py` (menu completo).

## 2. Grade
| Seção | Cód. | Critério | Pts possíveis | Pontuado | Evidência (comando / trecho / query) |
|---|---|---|---|---|---|
| A | A1 | venv documentado/usado e ambiente via requirements roda a aplicação | 2 | 2 | `.gitignore` linha 153-155: `.venv`, `venv/`; app executado em venv limpo (exit 0). README não tem instruções, mas o .gitignore cobre o critério ("pasta venv no .gitignore"). |
| A | A2 | `pip install -r` exit 0 em venv limpo, sem deps faltantes | 4 | 4 | `pip install -r requirements.txt` → "Successfully installed ... phonenumbers-8.13.47 ... requests-2.32.3 rich-13.9.4", EXIT=0; `pip check` → "No broken requirements found"; `import phonenumbers, requests, rich` OK. |
| A | A3 | requirements lista requests, rich e phonenumbers | 2 | 2 | `cat requirements.txt`: `phonenumbers==8.13.47`, `requests==2.32.3`, `rich==13.9.4` (nomes corretos). |
| A | A4 | .gitignore com venv; .db ignorado (bom ponto) | 2 | 2 | `.gitignore` inclui `venv/` e `.venv` (exigido ✓). Não ignora `*.db` (não exigido); nenhum `.db` commitado no repo. |
| B | B1 | Múltiplos módulos .py (≥3 com ≥1 função), um ponto de entrada | 2 | 2 | 8 arquivos .py; `main.py` (ponto de entrada), `menu_utils.py` (5 fun.), `telefone_utils.py` (9), `ui_utils.py` (14), `database.py` (8), `api_utils.py` (1), `config.py`. |
| B | B2 | Módulo com funções reutilizáveis | 2 | 2 | `database.py` (CRUD reutilizado por 3 handlers), `telefone_utils.py`, `ui_utils.py`, `api_utils.py` — usadas em vários lugares. |
| B | B3 | `if __name__ == "__main__":` com delegação | 2 | 2 | `main.py:40` → `main()` delega a `menu_utils.validar_numero/consultar_ddd/...`. |
| B | B4 | 3 tipos de import (built-in, local, pip) | 2 | 2 | built-in: `sqlite3`, `os`, `sys`, `random`; local: `from database import criar_banco`, `from telefone_utils import ...`; pip: `import phonenumbers`, `import requests`, `from rich.table import Table`. |
| B | B5 | Dicionários no fluxo de dados | 2 | 2 | `UF_PARA_DDDS` (config.py), respostas da API como dict (`dados.get('state')`), dict `dados` do telefone (telefone_utils.py:56-63). |
| C | C1 | Condicionais, loops, `and/or/not`, aritmética significativa | 2 | 2 | `menu_utils.gerar_numeros`: `quantidade // len(ddds)`, `quantidade % len(ddds)`, distribução por DDD; condicionais em todos os handlers. |
| C | C2 | Fragmentação; sem função-gigante (>~80 linhas) | 2 | 0,5 | `gerar_numeros` tem **125 linhas** e faz parsing de opção, seleção UF/DDD, geração e persistência (excesso). Demais módulos bem fragmentados. |
| C | C3 | SQLite de fato usado: schema, INSERT, SELECT | 3 | 3 | `sqlite3 telefones_ddd.db ".tables"` → `ddd_consultas`, `telefones`; 8 INSERTs confirmados; `listar_telefones()` faz SELECT com filtro (usado no item 4). |
| C | C4 | Dados externos exclusivamente via requests, parse `.json()`, sem hardcode no lugar da API | 3 | 3 | `api_utils.py:9-13`: `requests.get(url, timeout=5)`, `resposta.json()` → dict. Tráfego real (execução 1). Obs.: mapa UF→DDD é referência estática em `config.py` (a API não oferece endpoint UF→DDD); não é dado de API passando-se por API — anotado, sem desconto. |
| D | D1 | rich para toda apresentação de dados estruturados | 3 | 3 | Tabelas rich observadas nas execuções (Dados do Telefone, DDD, Números Gerados, Histórico); `from rich.table/panel` em `ui_utils.py`. |
| D | D2 | `print()` simples não usado para dados estruturados | 2 | 2 | `grep -rn "print("` em todos os módulos do fluxo `main.py` → apenas `console.print` (rich). `Validar_e_Consultar.py` (código morto, não importado por `main.py`) usa `print` — anotado. |
| E | E-2.1 | Item 2.1 Validar/formatar | 10 | 8,5 | ver §3 |
| E | E-2.2 | Item 2.2 Consultar DDD | 10 | 7 | ver §3 |
| E | E-2.3 | Item 2.3 Gerar por região | 10 | 6 | ver §3 |
| E | E-2.4 | Item 2.4 Histórico | 10 | 9 | ver §3 |
| E | E-2.5 | Item 2.5 Comparar dois números | 10 | 9 | ver §3 |
| F | F1 | 3 inputs inválidos sem traceback, msg informativa, retorno ao menu | 3 | 3 | ver §5 |
| F | F2 | Falha de API tratada, sem traceback, app continua | 2 | 2 | ver §5 (proxy morto) |
| G | G | Bônus | 10 | 1,67 | ver §6 |

## 3. Testes dinâmicos por item
### Item 2.1 — Validar e formatar
- Entradas: `11999998888` → `(21) 3333-4444` → `+55 11 99999-8888`
- Saída (corte):
```
┃ Nacional      │ (11) 99999-8888   │
┃ Internacional │ +55 11 99999-8888 │
┃ Tipo          │ Celular           │
┃ DDD           │ 11                │
┃ País          │ Brasil            │
✓ Salvo com ID 1
...
┃ Tipo          │ Fixo              │  (2ª entrada, (21) 3333-4444)
```
- Verificadores específicos: ✓ 3 formatos aceitos; ✓ nacional+internacional corretos; ✓ móvel nos 1º/3º, fixo no 2º; ✓ registro no SQLite com timestamp (IDs 1-3); ✗ "status de validade" não exibido na tabela (campo ausente).
- Subcritérios: E-a 2 / E-b 2 / E-c 2 / E-d 2 / E-e 0,5 → **8,5**
  (E-e 0,5: spec exige exibir "status de validade"; a tabela mostra Nacional/Internacional/Tipo/DDD/País mas não o status.)

### Item 2.2 — Consultar DDD
- Entradas: `21`
- Saída (corte):
```
DDD 21 pertence a UF RJ
┃ Estado ┃ Cidades                                                             ┃
│ RJ     │ TERESÓPOLIS, TANGUÁ, SEROPÉDICA, ..., RIO DE JANEIRO, ... NOVA IGUAÇU │
│        │ ... e mais 13 cidades                                               │
✓ Consulta salva com ID 1
```
- Verificadores específicos: ✓ estado RJ; ✓ cidades listadas (23; total comunicável via "10 + e mais 13"); ✓ DDD "validado" — porém via lista local `DDD_VALIDOS` (config.py), **não** via phonenumbers (validador específico falhou); ✓ registro em `ddd_consultas` com timestamp.
- Subcritérios: E-a 2 / E-b 2 / E-c 0 / E-d 2 / E-e 1 → **7**
  (E-c 0: phonenumbers ausente do caminho do item — a validação de plausibilidade do DDD usa o dicionário local; o verificador específico "DDD validado via phonenumbers" não se cumpre no `main.py`. O arquivo legado `Validar_e_Consultar.py` usava phonenumbers, mas não é o ponto de entrada.)

### Item 2.3 — Gerar números por região
- Entradas: `uf` → `SP` → `celular` → `5` → distribuir `s`
- Saída (corte):
```
Encontrados 9 DDDs para UF SP: 11, 12, 13, 14, 15, 16, 17, 18, 19
│ 1 │ SP │ 11 │ Celular │ 11921055911 │ (11) 9210-55911 │
│ 2 │ SP │ 12 │ Celular │ 12956147933 │ (12) 9561-47933 │
... (5 linhas, DDDs 11–15)
✓ 5 números salvos no banco de dados.
```
- Verificadores específicos: ✓ 5 números semanticamente válidos para DDDs de SP (11–19, prefixo 9 = celular); ✓ `ficticio = 1` confirmada no banco (IDs 4-8); ✗ campo `numero_internacional` malformado nos gerados: `+55 (11) 9210-55911` (menu_utils.py monta `f"+55 {num['formatado']}"`); obs.: descoberta dos DDDs da UF por mapa local em vez de API (aceitável — BrasilAPI não expõe UF→DDD; não é dado de API disfarçado).
- Subcritérios: E-a 2 / E-b 1 / E-c 0,5 / E-d 0,5 / E-e 2 → **6**
  (E-b 1: descoberta UF→DDD via config local, spec pedia API; E-c 0,5: geração é pattern/random, phonenumbers só valida a posteriori o `valido`; E-d 0,5: registros existem com `ficticio=1`, mas `numero_internacional` com valor inválido.)

### Item 2.4 — Histórico
- Entradas: filtro `tipo` → `Celular`; depois filtro `nenhum`
- Saída (corte): filtro Celular exibe apenas IDs 1,3,4,5,6,7,8 (Fixo ID 2 excluído); `nenhum` exibe os 8 registros.
- Verificadores específicos: ✓ filtro por tipo funciona; ✓ filtro por estado existe (UF→DDD list); ✓ tabela com todas as colunas (ID, Nacional, Internacional, Tipo, DDD, UF, Válido, Fictício, Timestamp). Obs.: rótulo "Celular" vs. "móvel" da spec — aceitável (rubrica §7.5: o que vale é o comportamento).
- Subcritérios: E-a 2 / E-b 2 / E-c 1 / E-d 2 / E-e 2 → **9**
  (E-c 1: o item não exige a biblioteca-tempero por spec — é listagem/filtro do SQLite; critério não violado.)

### Item 2.5 — Comparar dois números
- Entradas: `(11) 99999-8888` × `+5511999998888`; depois `11999998888` × `2133334444`
- Saída (corte):
```
Equivalentes: SIM
Normalizado 1: +5511999998888
Normalizado 2: +5511999998888
...
Equivalentes: NÃO
Normalizado 1: +5511999998888
Normalizado 2: +552133334444
```
- Verificadores específicos: ✓ 1º par equivalentes; ✓ 2º par distintos; ✓ normalização E164 via phonenumbers.
- Subcritérios: E-a 2 / E-b 2 / E-c 2 / E-d 1 / E-e 2 → **9**
  (E-d 1: a spec não exige persistência neste item — nada a gravar/consultar.)

## 4. Banco de dados
- Tabelas: `telefones`, `ddd_consultas`
- Contagens: `telefones` = 8 (3 reais + 5 fictícios); `ddd_consultas` = 1 (+1 no teste do DDD 99)
- Campos exigidos: ✓ `ficticio` (0/1), ✓ `timestamp` (DATETIME, preenchido: `2026-09-15 19:00:15`), ✓ ddd/estado/cidades em `ddd_consultas`
- Query: `SELECT * FROM telefones;` → linhas 1-8 conforme §3; `SELECT * FROM ddd_consultas;` → `21|RJ|TERESÓPOLIS, ... BELFORD ROXO|2026-09-15 19:00:15`

## 5. Robustez
| Input inválido | Comportamento | Traceback? | Pts |
|---|---|---|---|
| número `12345` | "Número inválido!" → retorno ao menu | não | 1 |
| número vazio | "Número inválido!" (NumberParseException capturada) → retorno ao menu | não | 1 |
| DDD `99` | **99 é DDD real (MA)**: "DDD 99 pertence a UF MA" + tabela da API (102 cidades) — tratamento correto para DDD válido; sem traceback, volta ao menu. (Premissa da rubrica equivocada; comportamento correto.) | não | 1 |
| Falha de API (HTTPS_PROXY=127.0.0.1:9, DDD 21) | "Erro ao consultar DDD 21 na API." → app continua utilizável (F2 = 2) | não | (F2) |

## 6. Bônus
| Bônus | Demonstrado? | Evidência | Pts |
|---|---|---|---|
| Lista de bloqueio | não | `grep -rni "bloqueio\|reclama"` → sem correspondência | 0 |
| Custo de ligação | **parcial** | `calcular_custo_ligacao()` existe em `telefone_utils.py:158` e funciona isoladamente (fixo-fixo mesmo DDD=0.0, fixo-móvel=0.5, outro DDD=1.0/2.0), mas **não é chamado por nenhum item do app** — a spec pede "exibir o custo ao comparar origem e destino" e o item 5 não o exibe → bônus "meio funcional", 50% | 1,67 |
| vCard (.vcf) | não | `grep -rni "vcard\|vcf"` → sem correspondência | 0 |

## 7. Resultado
- Subtotais: A **10** B **10** C **8,5** D **5** E **39,5** F **5** G **1,67**
- Tetos aplicados: nenhum (R1–R5 não disparadas)
- **Total: 79,17 / 100 → Nota: 7,92 / 10**
- **Aprovado? SIM** (≥ 70)

## 8. Observações qualitativas
- **Pontos fortes:**
  - Aplicação completa (5/5 itens), estável, sem traceback em nenhum teste (inclusive com rede cortada).
  - Boa modularização (8 módulos com responsabilidades claras: config, database, api, telefone, ui, menu, main) e uso consistente de `rich`.
  - Robustez real: exceções de API capturadas, `NumberParseException` tratada, menu rejeita opções inválidas.
  - Banco bem modelado (`ficticio`, `timestamp`) e filtros funcionais.
- **Problemas principais:**
  1. `Validar_e_Consultar.py` (versão antiga com 2 itens, `print` direto e conexão no escopo global) ficou no repositório como código morto — higiene de projeto.
  2. Item 2: validação de DDD via dicionário local, não via `phonenumbers` (exigência específica do item).
  3. `numero_internacional` malformado para números gerados (`+55 (11) 9210-55911`).
  4. Item 1 não exibe "status de validade" (exigido pela spec).
  5. `gerar_numeros` com 125 linhas (função-gigante).
  6. Bônus "custo de ligação" implementado mas não integrado ao menu; bloqueio e vCard ausentes.
- **Pendências/limitações não testadas:** nenhuma — API BrasilAPI disponível durante toda a avaliação; todos os itens e inputs de robustez executados.
