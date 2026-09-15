# Relatório de Correção — Trabalho 9: Tabela FIPE com Valores por Extenso

**Identificação:** dupla / repositório `09` (arquivos: `main.py`, `opcoes.py`, `operacoes_db.py`, `consulta_API.py`, `outro.py`, `banco.db`, `requirements.txt`, `espec.md`)
**Data da avaliação:** 2026-02-14

## 1. Veredito executivo
- **Executa?** SIM (o menu inicia e aceita opções), mas **nenhum dos 5 itens obrigatórios funciona**: item 1 consulta um endpoint inexistente (404) e os itens 2, 3 e 5 causam *traceback* (`AttributeError` por funções inexistentes); o item 4 falha pela mesma razão do item 1.
- **API utilizada:** `https://parallelum.com.br/fipe/api/v1` (API pública real de FIPE, alternativa à brasilapi sugerida — aceitável pela Seção 5 da rubrica, **desde que** os endpoints existam). O endpoint usado para o preço, `GET /veiculos/{codigoFipe}`, **não existe** (verificado: `404 {"error":"Cannot GET /api/v1/veiculos/007018-1"}`, testado com e sem hífen).
- **Biblioteca-tempero efetivamente usada:** PARCIAL — `num2words` está corretamente integrada no código dos itens 1 e 4 (preço e diferença por extenso, `lang='pt_BR'`), mas esses caminhos **nunca executam** em runtime (API 404).
- **Regras de teto disparadas:** nenhuma (R1–R5 não se aplicam; ver Seção 7).

## 2. Grade

| Seção | Cód. | Critério | Pts possíveis | Pontuado | Evidência (comando / trecho / query) |
|---|---|---|---|---|---|
| A | A1 | Projeto documenta/usa venv | 2 | **0** | Sem `README`, sem `venv/`, sem `.gitignore` no diretório (`ls -a /workspace/09`: apenas os 8 arquivos listados) |
| A | A2 | `pip install -r` exit 0 em venv limpo | 4 | **4** | Venv limpo criado do zero: `Successfully installed ... num2words-0.5.14 requests-2.34.2 rich-15.0.0` (exit 0); `pip check` → `No broken requirements found` (exit 0); app inicia |
| A | A3 | Lista `requests`, `rich`, `num2words` | 2 | **2** | `requirements.txt`: `num2words==0.5.14`, `requests==2.34.2`, `rich==15.0.0` (+ transitive deps) |
| A | A4 | `.gitignore` com venv/.db | 2 | **0** | `.gitignore` não existe; além disso `banco.db` foi commitado (0 linhas) |
| B | B1 | Múltiplos módulos `.py` (≥3, 1 entrada) | 2 | **2** | 5 módulos: `main.py` (entrada), `opcoes.py` (6 funções), `operacoes_db.py` (4 funções), `consulta_API.py` (4 funções), `outro.py` |
| B | B2 | Funções reutilizáveis | 2 | **2** | `operacoes_db.*` e `consulta_API.*` usadas em múltiplos lugares de `opcoes.py` |
| B | B3 | `if __name__ == "__main__":` com delegação | 2 | **2** | `main.py:45 if __name__ == "__main__": main()` — lógica delegada a `main()` (também em `outro.py:86`) |
| B | B4 | 3 tipos de import | 2 | **2** | Built-in `sqlite3` (`operacoes_db.py`), locais `import operacoes_db/opcoes/consulta_API` (`main.py`), pip `requests`/`rich`/`num2words` |
| B | B5 | Dicionários no fluxo | 2 | **2** | Respostas da API em dict (`resp.json()`); dict de cache em `obter_ou_buscar_dados` (`opcoes.py:96`) |
| C | C1 | Condicionais/loops/operadores significativos | 2 | **2** | `if/elif` do menu, `for ... in dados`, `try/except ValueError`, `if not consulta or 'Preco' not in consulta` |
| C | C2 | Lógica fragmentada, sem monólito | 2 | **2** | Módulos por responsabilidade (API/DB/opções); obs.: lógica de consultar-preço duplicada em `consultar_preco` e na função aninhada de `comparar_veiculos` (~85 linhas) |
| C | C3 | SQLite real: schema, INSERT, SELECT, registros | 3 | **1** | Schema criado em `conectar()`; `INSERT` em `salvar_consulta`; `SELECT` em `buscar_por_fipe`. Porém **nenhum registro no .db** (banco commitado tem 0 linhas; nada foi gravado porque a API do item 1 responde 404) e **faltam as tabelas de marcas/modelos** exigidas pelo item 2/3 |
| C | C4 | API pública real via `requests`, sem hardcode | 3 | **2** | 4 `requests.get` em `consulta_API.py` contra API pública real (parallelum); parse `resp.json()` com chaves corretas (`Marca`, `Modelo`, `AnoModelo`, `Preco` — conferidas na resposta real). Desconto: o endpoint de preço `/veiculos/{fipe}` retorna 404 sempre → nenhum preço é efetivamente adquirido |
| D | D1 | `rich` para dados estruturados, visível na execução | 3 | **0,5** | `Table` rich corretamente construído no código (itens 2/4/5), mas **nunca renderizado** em runtime (todos os itens falham antes); item 1 é `print` |
| D | D2 | `print` só para menu/navegação | 2 | **0,5** | Item 1 imprime dados estruturados com 6 `print()` (`opcoes.py:39-44`) em vez da tabela rich exigida pela especificação |
| E | E-1.1 | Item 1 — preço por código FIPE | 10 | **2,5** | Ver Seção 3 (a=1, b=0,5, c=0,5, d=0,5, e=0) |
| E | E-1.2 | Item 2 — marcas por tipo | 10 | **1** | Ver Seção 3 (a=1, b=0, c=0, d=0, e=0) |
| E | E-1.3 | Item 3 — modelos por marca | 10 | **0** | Ver Seção 3 (a=0, b=0, c=0, d=0, e=0) |
| E | E-1.4 | Item 4 — comparar dois veículos | 10 | **3** | Ver Seção 3 (a=1, b=0,5, c=0,5, d=0,5, e=0,5) |
| E | E-1.5 | Item 5 — histórico com filtros | 10 | **0** | Ver Seção 3 (a=0, b=0, c=0, d=0, e=0) |
| F | F1 | 3+ inputs inválidos sem traceback | 3 | **3** | Ver Seção 5 |
| F | F2 | Falha de API tratada | 2 | **1** | 404 HTTP tratado (mensagem amigável, app continua — observado); falha de rede **não** tratada: `consulta_API.py` sem `try/except` (ConnectionError → traceback não tratado) |
| G | G | Bônus | 10 | **0** | Nenhum bônus específico (inglês/recibo/depreciação) nem geral (export/batch/painel/config/testes/logging) implementado |

## 3. Testes dinâmicos por item

### Item 1.1 — Consultar preço por código FIPE
- Entradas: opção `1`, tipo `carros`, código `007018-1` (código válido descoberto via API, executado 2×)
- Saída (corte):
  ```
  [API FIPE] Código não encontrado no banco. Consultando API externa...
  Erro ao buscar o valor ou código FIPE inválido.
  ```
  (2ª execução idêntica — nunca chega a cache pois nada foi gravado)
- Verificadores específicos: ✗ tabela rich (veículo, ano, preço numérico, extenso) — nada exibido; ✗ armazenamento no SQLite (banco permanece com 0 linhas); ✗ extenso conferível
- Causa raiz: `consulta_API.get_valor` usa `GET {base}/veiculos/{cod}` → endpoint inexistente (404 verificado direto: `404 {"error":"Cannot GET /api/v1/veiculos/007018-1"}`)
- Subcritérios: E-a **1** / E-b **0,5** / E-c **0,5** / E-d **0,5** / E-e **0** = **2,5**

### Item 1.2 — Listar marcas por tipo
- Entradas: opção `2`, tipo `carros`
- Saída (corte):
  ```
  File "/tmp/eval09/opcoes.py", line 172, in listar_marcas
      marcas = consulta_API.buscar_marcas(tipo)
  AttributeError: module 'consulta_API' has no attribute 'buscar_marcas'
  ```
- Verificadores específicos: ✗ tudo (app **crasha**; a API nunca é chamada; a `operacoes_db.salvar_marcas` e `listar_marcas_com_historico` também não existem — `grep` confirma as referências órfãs em `opcoes.py:172-178`)
- Subcritérios: E-a **1** / E-b **0** / E-c **0** / E-d **0** / E-e **0** = **1**

### Item 1.3 — Listar modelos por marca
- Entradas: opção `3`
- Saída (corte):
  ```
  File "/tmp/eval09/opcoes.py", line 208, in listar_marcas_detalhado
      dados = operacoes_db.listar_marca()
  AttributeError: module 'operacoes_db' has no attribute 'listar_marca'
  ```
- Verificadores específicos: ✗ tudo. Além do crash, a função **nem solicita o código da marca nem consulta a API de modelos** — implementação do item errado mesmo em código
- Subcritérios: E-a **0** / E-b **0** / E-c **0** / E-d **0** / E-e **0** = **0**

### Item 1.4 — Comparar dois veículos
- Entradas: opção `4`, códigos `007018-1` e `010042-1`
- Saída (corte):
  ```
  [API] Veículo 007018-1 não encontrado no banco. Consultando API...
  [API] Veículo 010042-1 não encontrado no banco. Consultando API...
  Erro ao buscar um dos veículos (código FIPE inválido ou erro na API).
  ```
- Verificadores específicos: ✗ tabela lado a lado, ✗ diferença por extenso, ✗ indicação de mais caro — nunca renderizados (mesmo 404 do item 1). O código da `Table` com todos os campos (incl. `dif_extenso` via num2words e "mais caro") existe em `opcoes.py:127-151`, mas é inalcançável
- Subcritérios: E-a **1** / E-b **0,5** / E-c **0,5** / E-d **0,5** / E-e **0,5** = **3**

### Item 1.5 — Histórico de consultas
- Entradas: opção `5`
- Saída (corte):
  ```
  File "/tmp/eval09/opcoes.py", line 192, in listar_historico
      dados = operacoes_db.listar_consultas()
  AttributeError: module 'operacoes_db' has no attribute 'listar_consultas'. Did you mean: 'salvar_consulta'?
  ```
- Verificadores específicos: ✗ tudo. Além do crash: **não há filtros** (tipo/marca/faixa) — a função não faz nem um `input`; a tabela tem 6 colunas mas desempacota tuplas de 3 (`for cod, nome, count`) e **não inclui a coluna "preço por extenso"** exigida
- Subcritérios: E-a **0** / E-b **0** / E-c **0** / E-d **0** / E-e **0** = **0**

## 4. Banco de dados
- Tabelas: `fipe_cache` (única) — commitada com **0 linhas**
- Contagem: `fipe_cache`: 0 (antes e depois de todas as execuções — nenhum INSERT efetivo ocorreu)
- Campos exigidos: ✗ sem tabela de marcas (metadados de catálogo c/ flag, item 2); ✗ sem tabela de modelos vinculados à marca (item 3); ✓ `fipe_cache` tem `codigo_fipe, marca, modelo, ano_modelo, preco, preco_extenso` (schema adequado ao item 1, mas vazio)

## 5. Robustez
| Input inválido | Comportamento | Traceback? | Pts |
|---|---|---|---|
| Código FIPE `abc123` (item 1) | "Erro ao buscar o valor ou código FIPE inválido.", retorna ao menu | Não | 1 |
| Opção de menu `abc` / `99` | "Por favor, digite um número válido." / "Opção inválida, retornando ao menu principal." | Não | 1 |
| Entradas vazias (tipo/código, item 1) | "Erro ao buscar o valor ou código FIPE inválido." | Não | 1 |
| *(observação)* Qualquer entrada nas opções 2/3/5 | Crash com `AttributeError` não tratado (aplica-se a qualquer input, não só inválidos) | **Sim** | já refletido em E |

F2: falha HTTP (404) tratada com mensagem amigável e app utilizável (observado); falha de conexão de rede não tratada (`consulta_API.py` sem `try/except`; contraste com `outro.py`, que trata). **F2 = 1/2**

## 6. Bônus
| Bônus | Demonstrado? | Evidência | Pts |
|---|---|---|---|
| Extenso em inglês / recibo fictício / depreciação (Trabalho 9) | Não | Menu tem apenas itens 1–6; nenhuma dessas funcionalidades no código | 0 |
| Bônus gerais (export, batch, painel, config, testes, logging) | Não | Nenhum módulo/funcionalidade correspondente | 0 |

`outro.py` é um script CLI separado (funciona de ponta a ponta contra a parallelum — verificado — mas sem SQLite, sem `num2words`, sem `rich` e não integrado ao app) — é código morto para o trabalho, não pontua como bônus.

## 7. Resultado
- Subtotais: A **6** · B **10** · C **7** · D **1** · E **6,5** · F **4** · G **0**
- Tetos aplicados:
  - R1 não (requirements OK); R2 não (aplicação inicia); R3 não (num2words de fato integrada na lógica dos itens 1 e 4 em código — não é import decorativo, embora os caminhos falhem em runtime); R4 não (SQLite funcional: conexão/schema/queries OK em runtime, C3=1); R5 não (nenhum dado hardcoded)
- **Total: 34,50 / 100 → Nota: 3,45 / 10**
- **Aprovado?** NÃO (exige ≥ 70)

## 8. Observações qualitativas
- **Pontos fortes:** ambiente de dependências limpo e instalável (A2/A3); boa organização em módulos (B); `num2words` usada com `lang='pt_BR'` e `to='currency'` da forma correta; tratamento amigável de entrada inválida no menu; `outro.py` demonstra que a dupla conhecia o fluxo funcional da API parallelum (marcas → modelos → anos → valor).
- **Problemas principais:** (1) endpoint de preço inexistente (`/veiculos/{fipe}` → 404) quebra os itens 1 e 4 — o fluxo correto existe no mesmo repositório (`outro.py`), mas nunca foi integrado; (2) quatro funções referenciadas não existem (`buscar_marcas`, `salvar_marcas`, `listar_marcas_com_historico`, `listar_consultas`, `listar_marca`) → itens 2, 3 e 5 crasham com traceback; (3) item 3 não implementa o fluxo pedido (não pede código da marca nem consulta modelos); (4) item 5 sem filtros e sem coluna de extenso; (5) item 1 exibe com `print` em vez de tabela rich.
- **Pendências/limitações não testadas:** simulação de queda de rede (sem permissão de `unshare` no ambiente) — avaliada por análise estática de `consulta_API.py`; `TIMEOUT = 3000` (s) em `consulta_API.py` é claramente um bug (50 min), não testado dinamicamente por ser demorado, mas documentado.
- **Higiene:** `banco.db` commitado (7.4 da rubrica — negativo de higiene, registrado em A4); sem `README`/`.gitignore`.
