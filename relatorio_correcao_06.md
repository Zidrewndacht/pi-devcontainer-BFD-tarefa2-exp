# Relatório de Correção — Trabalho 6: Estatísticas de Nomes
**Identificação:** dupla do diretório `06` (arquivos: `README.md` + `trabalho2_py` — não é repositório git; sem commit)
**Data da avaliação:** 2025-07-09

## 1. Veredito executivo
- **Executa? SIM** — `python trabalho2_py` roda (menu funcional, saída rich, banco criado). Arquivo de entrada sem extensão `.py` (`trabalho2_py`), executável via `python <arquivo>`.
- **API utilizada:** `https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}` — API pública real do IBGE (equivalente à exigida pela especificação do Trabalho 6: "API pública de frequência de nomes por década"). Formato verificado: `[{"nome":..., "res":[{"periodo":"[1930,1940[","frequencia":...},...]}]`.
- **Biblioteca-tempero efetivamente usada: SIM** — `humanize.intword` em `_humanizar_numero` (itens 1, 2, 5) e `humanize.intcomma` na prevalência (item 4). Nota: `intword` retorna inglês ("60.2 thousand"); o app faz `.replace('thousand','mil')` etc. — funciona, mas mantém ponto decimal ("60.2 mil" em vez de "60,2 mil").
- **Regras de teto disparadas: R1** (`requirements.txt` ausente) → teto **30 pts**.

## 2. Grade
| Seção | Cód. | Critério | Pts poss. | Pontuado | Evidência |
|---|---|---|---|---|---|
| A | A1 | venv documentado/uso + ambiente via requirements.txt roda | 2 | 0 | Sem pasta `venv`; README diz "apenas Python 3"; sem requirements.txt (`ls requirements.txt` → "No such file") |
| A | A2 | `pip install -r` exit 0 em venv limpo | 4 | 0 | **requirements.txt não existe** (R1) |
| A | A3 | requirements lista requests, rich, humanize | 2 | 0 | Arquivo inexistente |
| A | A4 | `.gitignore` com venv/db | 2 | 0 | `find . -type f` → só `README.md`, `trabalho2_py` |
| B | B1 | Múltiplos arquivos .py (mín. 3 módulos) | 2 | 0 | 1 único arquivo (e sem extensão .py): `find . -name "*.py" \| wc -l` → 0 |
| B | B2 | Módulo com funções reutilizáveis | 2 | 1 | `BancoDeDados` (responsabilidade de banco) e helpers `_humanizar_numero`, `_limpar_periodo`, `buscar_dados_api` reutilizadas nas 5 operações — mas tudo num único arquivo, sem módulo independente |
| B | B3 | `if __name__ == "__main__":` com delegação | 2 | 2 | L.251: `if __name__ == "__main__": app = IBGENomesApp(); app.executar()` |
| B | B4 | 3 tipos de import (built-in, local, pip) | 2 | 0.5 | Built-in (`sqlite3`, `re`) ✓, pip (`requests`, `rich`, `humanize`) ✓, **local ✗** (arquivo único, impossível importar módulo do projeto) |
| B | B5 | Dicionários no fluxo de dados | 2 | 2 | L.96 `resposta.json()[0]['res']`; L.119-120 `item['periodo']`, `item['frequencia']` |
| C | C1 | Condicionais/loops/op. lógicos/aritméticos significativos | 2 | 2 | `while True` (menu), `for item in dados`, `and` (L.95), comparações de tendência, `sum`, `abs`, `%`, `*` (barras) |
| C | C2 | Funções com responsabilidade; sem monolito | 2 | 1 | Métodos de 10–30 linhas, bem divididos; porém é um script monolítico de arquivo único (critério veda "script monolítico") |
| C | C3 | SQLite real: schema + INSERT + SELECT + registros | 3 | 3 | Schema (2 tabelas) criado em `criar_tabelas`; INSERT em `salvar_frequencia`/`salvar_resumo`; SELECT em ranking/faixa; `sqlite3`: 16 linhas em `frequencia`, 1 em `resumo` |
| C | C4 | API exclusivamente via requests, parse json(), sem hardcoded | 3 | 3 | L.94 `requests.get(url)` contra IBGE real (verificado via curl); parse `resposta.json()[0]['res']`; `POPULACAO_BRASIL` é constante de cálculo, não substitui API |
| D | D1 | rich em toda apresentação estruturada | 3 | 2 | Tables (frequência, ranking), barras coloridas (comparação), menu rich; **item 4 sai via `print()` simples** (l.204) |
| D | D2 | Sem print() para dados estruturados | 2 | 1.5 | `print()` l.167 (linha em branco, trivial) e l.204 `print(prevalencia)` — frase final do item 4 fora do rich (não é tabela/lista/painel, mas é saída final de dados) |
| E | E-6.1 | Item 1.1 Consultar frequência | 10 | 9.5 | ver §3 |
| E | E-6.2 | Item 6.2 Comparar nomes | 10 | 10 | ver §3 |
| E | E-6.3 | Item 6.3 Ranking de década | 10 | 10 | ver §3 |
| E | E-6.4 | Item 6.4 Resumo | 10 | 8.5 | ver §3 |
| E | E-6.5 | Item 6.5 Faixa de frequência | 10 | 9.5 | ver §3 |
| F | F1 | 3+ inputs inválidos sem traceback | 3 | 3 | ver §5 |
| F | F2 | Falha de API tratada | 2 | 2 | ver §5 |
| G | G | Bônus | 10 | 0 | Nenhum bônus (específico ou geral) implementado |

## 3. Testes dinâmicos por item
Ambiente: venv limpo `/tmp/venv_eval` (Python 3.13) com `requests`, `rich`, `humanize` instalados manualmente (requirements.txt ausente — R1). API IBGE disponível durante toda a avaliação.

### Item 6.1 — Consultar frequência (`Joao`)
- Entradas: menu `1` → `Joao`
- Saída (corte):
```
┃ Década ┃ Frequência Bruta ┃ Frequência Humanizada ┃ Tendência ┃
│  1930  │            60155 │              60.2 mil │    N/A    │
│  1930  │           141772 │             141.8 mil │   Subiu   │
│  1940  │           256001 │             256.0 mil │   Subiu   │
│  1970  │           279975 │             280.0 mil │  Desceu   │
│  1990  │           352552 │             352.6 mil │   Subiu   │
```
- Verificadores: ✓ tabela rich com década/bruta/humanizada/tendência; ✓ humanize por linha; ✓ tendência correta em 3 linhas conferidas (1940: 256001>141772 Subiu; 1970: 279975<429148 Desceu; 1990: 352552>273960 Subiu); ✗ estado "estável" nunca exibido (só Subiu/Desceu/N/A — spec pede "subiu, desceu **ou estável**"); ✗ API devolve entrada extra `"1930["` → duas linhas "1930" na tabela (a 2ª sobrescreve a 1ª no banco, por `DELETE ... WHERE nome AND decada`).
- Subcritérios: E-a 2 / E-b 2 / E-c 2 / E-d 2 / E-e 1.5 → **9.5**

### Item 6.2 — Comparar (`Joao` × `Maria`)
- Entradas: menu `2` → `Joao`, `Maria`
- Saída (corte):
```
Mais popular: MARIA
Diferença: 8.8 milhões registros (293.2% maior)
JOAO            | ██████████ 3.0 milhões
MARIA           | ████████████████████████████████████████ 11.7 milhões
```
- Verificadores: ✓ mais popular; ✓ diferença absoluta humanizada (11,7M − 2,984M ≈ 8,7–8,8M ✓); ✓ percentual conferido (8,75/2,984 × 100 ≈ 293,2% ✓); ✓ barras proporcionais (10 vs 40 chars ≈ razão 0,255 = 2,98/11,7 ✓).
- Subcritérios: E-a 2 / E-b 2 / E-c 2 / E-d 2 (spec do item 2 não exige persistência) / E-e 2 → **10**
- Nota: item 2 **não grava no SQLite** — consequência visível no item 3 (Maria ausente do ranking). Conformidade literal com a spec (só o item 1 manda "Armazena no SQLite").

### Item 6.3 — Ranking de década (3 nomes consultados → `2000`)
- Entradas: após consultar Joao, comparar com Maria, consultar Ana → menu `3` → `2000`
- Saída (corte):
```
┃ Posição ┃ Nome ┃ Frequência ┃
│    1    │ ANA  │  935.2 mil │
│    2    │ JOAO │  794.1 mil │
```
- Verificadores: ✓ top ordenado por frequência bruta decrescente (`ORDER BY frequencia_bruta DESC LIMIT 10`); ✓ humanizado; ✓ consulta só o banco (MARIA ausente porque o item 2 não persiste — 2 linhas = 2 nomes persistidos, consistente com o banco).
- Subcritérios: E-a 2 / E-b 2 / E-c 2 / E-d 2 / E-e 2 → **10**

### Item 6.4 — Resumo (`Joao`)
- Entradas: menu `4` → `Joao`
- Saída (corte): `A cada 68 brasileiros, 1 se chama Joao`
- Verificadores: ✓ prevalência plausível (203.062.512 // 2.984.119 = 68; base populacional 203 mi, próxima do ~215 mi da spec); ✓ resumo gravado no SQLite: `('JOAO', 2984119, 2000, 'A cada 68 brasileiros, 1 se chama Joao')` — total ✓ e década de pico ✓ (2000 = maior frequência) **no banco**; ✗ **total e década de pico NÃO são exibidos** ao usuário (só a frase de prevalência, via `print()` simples, sem rich).
- Subcritérios: E-a 2 / E-b 2 / E-c 2 / E-d 2 / E-e 0.5 → **8.5**

### Item 6.5 — Faixa de frequência
- Entradas (1ª): `100000`–`500000` → "Nenhum nome encontrado na faixa entre 100.0 mil e 500.0 mil." (correto: totais dos 3 nomes > 500 mil)
- Entradas (2ª): `2000000`–`3500000` →
```
Nomes na faixa (Entre 2.0 milhões e 3.5 milhões):
ANA: 3.1 milhões no total
JOAO: 2.9 milhões no total
```
- Verificadores: ✓ nomes da faixa listados (3,056,463 e 2,984,119 ∈ [2M, 3.5M] ✓); ✓ limites via humanize; ✗ sintaxe de entrada é 2 números brutos, não o estilo "mais de 100 mil"/"entre 10 mil e 50 mil" da spec (sintaxe numérica equivalente aceita pelo roteiro, com dedução leve em E-a); format "2.0 milhões" (ponto decimal, herdado do inglês).
- Subcritérios: E-a 1.5 / E-b 2 / E-c 2 / E-d 2 / E-e 2 → **9.5**

## 4. Banco de dados
- Tabelas: `frequencia (id, nome, decada, frequencia_bruta, frequencia_humanizada)`, `resumo (nome PK, total, decada_pico, prevalencia)`
- Contagem após os fluxos: `frequencia` = 16 (8 ANA + 8 JOAO), `resumo` = 1
- Campos exigidos: ✓ nome/década/bruta/humanizada em `frequencia`; ✓ total/década_pico/prevalência em `resumo`
- Sem `.db` commitado pela dupla (criado pela avaliação); observação: a entrada extra da API ("1930[") é sobrescrita no banco (2ª ocorrência da mesma década), então o total de JOAO no banco (2.984.119) exclui os 60.155 da 1ª linha.

## 5. Robustez
| Input inválido | Comportamento | Traceback? | Pts |
|---|---|---|---|
| ⊘ Nome `ZzqqXx99` (item 1) | "Nenhum dado encontrado para o nome 'ZZQQXX99' no IBGE." → volta ao menu | Não | 1 |
| ⊘ Década `2024` sem dados (item 3) | "Nenhum dado salvo no banco para a década de 2024." → volta ao menu | Não | 1 |
| ⊘ Década `abc` (IntPrompt) | Re-prompt do rich, aceita valor seguinte, sem crash | Não | 1 |
| ⊘ Nome vazio (item 1) | API 404 → "Nenhum dado encontrado para o nome '' no IBGE." | Não | (+) |
| ⊘ Falha de API (proxy 127.0.0.1:9) | "Erro ao conectar com a API: HTTPSConnectionPool(...)" → app continua, sai normalmente (exit 0) | Não | F2 = 2 |

## 6. Bônus
| Bônus | Demonstrado? | Evidência | Pts |
|---|---|---|---|
| Predição da próxima década (T6) | Não | Ausente no código | 0 |
| Equivalente à população de cidade (T6) | Não | Ausente | 0 |
| Certificado de popularidade (T6) | Não | Ausente | 0 |
| Bônus gerais (export/batch/dashboard/config/tests/logging) | Não | Sem menu/opção correspondente | 0 |

## 7. Resultado
- Subtotais: A **0**  B **5.5**  C **8**  D **3.5**  E **47.5**  F **5**  G **0**
- Total bruto: **69.5 / 100**
- **Teto aplicado: R1** (requirements.txt ausente → teto 30; R2–R5 não disparadas: app executa, humanize é efetiva, SQLite funciona, API real)
- **Total: 30.00 / 100 → Nota: 3.00 / 10**
- **Aprovado? NÃO** (< 70)

## 8. Observações qualitativas
- **Pontos fortes:** aplicação funcional de ponta a ponta (API real IBGE → parse → SQLite → rich); robustez excelente (nenhum traceback em nenhum input inválido; falha de rede tratada e app utilizável); humanize usada de fato na lógica central; SQL bem escrito (HAVING/BETWEEN, ORDER BY, upsert); código limpo e bem organizado em classes/métodos dentro do arquivo único.
- **Problemas principais:** (1) **sem `requirements.txt`** → quebra o requisito central de reprodutibilidade (R1, teto 30); (2) arquivo único (viola modularidade: B1=0, B4 parcial, C2 parcial) e sem extensão `.py`; (3) sem `venv`/`.gitignore`; (4) item 4 não exibe total e década de pico (só grava); (5) tendência sem estado "estável"; (6) item 2 não persiste (efeito colateral no ranking); (7) import `rprint` não usado.
- **Pendências/limitações:** API IBGE disponível durante toda a avaliação (sem casos da Seção 7); o estado "estável" de tendência não pôde ser exercitado via API (dados reais raramente empata década a década) — falha apontada por análise de código (l.126-130: só `>`/`<`, sem `==`).
- **Justa-cause do teto:** sem requirements.txt a recriação do ambiente é impossível conforme a especificação ("Deve ser possível recriar o ambiente com `pip install -r requirements.txt`"), independentemente da qualidade do código, que em execução isolada teria atingido 69,5 pts (borderline de aprovação).
