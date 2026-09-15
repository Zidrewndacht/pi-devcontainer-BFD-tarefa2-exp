# Relatório de Correção — Trabalho 5: Geocodificação de Municípios
**Identificação:** dupla / diretório `05` (GeoAtlas Brasil)
**Data da avaliação:** 2026-09-15

## 1. Veredito executivo
- **Executa? SIM** — `main.py` inicia no venv limpo; todos os 5 itens + robustez testados com tráfego real.
- **API utilizada:** IBGE `https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios` (a sugerida, com variante por estado — mesma semântica) + Nominatim via `geopy` (como previsto na spec). Nenhuma alteração problemática.
- **Biblioteca-tempero efetivamente usada: SIM** — `geopy` em `geocodificador.py`: `Nominatim` (com `RateLimiter`) para obter coordenadas e `geodesic` para distância km/milhas (lógica central dos itens 1–4).
- **Regras de teto disparadas: nenhuma** (R1–R5 não se aplicam).

## 2. Grade

| Seção | Cód. | Critério | Pts possíveis | Pontuado | Evidência |
|---|---|---|---|---|---|
| A | A1 | venv documentado + ambiente via requirements roda | 2 | 2 | README: `python3 -m venv .venv` (Win/Linux); app executado em venv limpo |
| A | A2 | `pip install -r` exit 0 em venv limpo | 4 | 4 | `install_exit=0`; `pip check` → "No broken requirements found" |
| A | A3 | requirements lista requests, rich, geopy | 2 | 2 | `geopy>=2.4,<3` / `requests>=2.32,<3` / `rich>=13.9,<15` |
| A | A4 | .gitignore c/ venv, .db, artefatos | 2 | 2 | `.venv/`, `*.db`, `exports/*.csv`, `logs/*.log`, `__pycache__/` |
| B | B1 | ≥3 módulos não vazios + entrada | 2 | 2 | 14 módulos na raiz (main, database, servicos, geocodificador, ibge_api, validacoes, models, config, interface, batch, dashboard, exportacao, mapa_ascii, logging_config) |
| B | B2 | Funções reutilizáveis | 2 | 2 | `validacoes.validar_uf` usada em ibge_api/servicos/interface; `BancoDados` em servico+interface+dashboard |
| B | B3 | `if __name__` com delegação | 2 | 2 | `main.py:42` → `criar_aplicacao().executar()` |
| B | B4 | 3 tipos de import | 2 | 2 | built-in (`sqlite3`, `json`, `os`, `re`, `csv`, `unicodedata`), módulos locais, pip (`geopy`, `requests`, `rich`) |
| B | B5 | Dicionários no fluxo | 2 | 2 | resposta IBGE `list[dict]`, `capitais` (JSON→dict), `resultado` da sincronização, `estatisticas()` |
| C | C1 | Condicionais/loops/lógicos/aritmética significativos | 2 | 2 | loop de sync c/ cache, `validar_raio` (aritmética), `geodesic`, `medias()` |
| C | C2 | Funções responsavelizadas, sem gigante | 2 | 2 | função maior: `servicos.sincronizar` = 51 linhas; arquitetura camadas (api/geocoder/db/serviço/iface) |
| C | C3 | SQLite de fato (schema+INSERT+SELECT) | 3 | 3 | `.tables` → `municipios`, `sincronizacoes`; 223 registros confirmados; upsert `ON CONFLICT DO UPDATE`; `SELECT` para exibição |
| C | C4 | Dados externos só via requests + parse | 3 | 3 | `ibge_api.py:21` `requests.get(...).json()`; `capitais.json` só no fallback do bônus (coordenada aproximada), não substitui API; 0 hardcoded de municípios |
| D | D1 | rich para toda apresentação estruturada | 3 | 3 | Table/Panel/Progress/Layout/grid observados em execução |
| D | D2 | Sem print() de dados estruturados | 2 | 2 | `grep print(` fora de `console.print` → 0 ocorrências |
| E | E-1.1 | Item 1.1 Sincronizar UF | 10 | 10 | ver §3 |
| E | E-1.2 | Item 1.2 Buscar coordenadas | 10 | 10 | ver §3 |
| E | E-1.3 | Item 1.3 Distância | 10 | 10 | ver §3 |
| E | E-1.4 | Item 1.4 Próximos | 10 | 10 | ver §3 |
| E | E-1.5 | Item 1.5 Listar | 10 | 8,5 | E-c 0,5: ver §3 |
| F | F1 | 3+ inputs inválidos sem traceback | 3 | 3 | 5 testados (UF `XX`, `Xyz/DF`, raio `0`, `-5`, `abc`) — todos com painel e retorno ao menu |
| F | F2 | Falha de API tratada | 2 | 2 | IBGE 404 → painel "Nenhum município foi retornado..."; Nominatim inacessível → fallback capital; app continua utilizável nos dois casos |
| G | Bônus | 3 bônus demonstrados (teto 10) | 10 | 10 | fallback capital (3,33) + mapa ASCII (3,33) + CSV built-in (3,33) + geral (batch, dashboard, config JSON/env, testes, logging, JSON) → teto |

## 3. Testes dinâmicos por item

### Item 1.1 — Sincronizar UF (`DF`)
- Entradas: `1` → `DF`
- Saída (corte):
```
Brasília ━━━━━━━━━━ 1/1 0:00:02
╭────────────────────────── Resumo da sincronização ───────────────────────────╮
│ Municípios da UF                                  1                          │
│ Geocodificados agora                              1                          │
│ Média latitude / longitude  -15.793987 / -47.882800                          │
│ Estimativa inicial                              1 s                          │
│ Tempo decorrido                                 2 s                          │
```
- Verificadores: ✓ total (1, correto p/ DF) ✓ médias ✓ tempo (estimativa + decorrido) ✓ coordenadas plausíveis (−15,79/−47,88 ≈ −15,8/−47,9) ✓ schema c/ ID IBGE, nome, UF, lat, lon, data
- Reexecução (cache): `Obtidos do cache: 1`, `Geocodificados agora: 0`, tempo 0 s (sem chamadas ao Nominatim)
- Subcritérios: E-a 2 / E-b 2 / E-c 2 / E-d 2 / E-e 2 = **10**

### Item 1.2 — Buscar coordenadas
- Entradas: `Brasília/DF` (cache) → `Maceió/AL` (ausente)
- Saída (corte): `Município Maceió/AL │ ID IBGE 2704302 │ Latitude -9.647684 │ Longitude -35.733926 │ ... Mapa https://www.openstreetmap.org/?mlat=...`
- Verificadores: ✓ 1º do SQLite (sem rede); ✓ 2º via IBGE+geopy e gravado no banco (confirmado via `sqlite3`); ✓ nome/UF/lat/lon + link de mapa (link funcional, melhor que "fictício")
- Subcritérios: 2/2/2/2/2 = **10**

### Item 1.3 — Distância
- Entradas: `Brasília/DF × Boa Vista/RR`; adicional: `Goiânia/GO × Senador Canedo/GO`
- Saída: `2494.26 km / 1549.86 milhas / Não são vizinhos`; `17.40 km / 10.81 milhas / Vizinhos`
- Verificadores: ✓ km e milhas; ✓ tolerância: recálculo independente `geodesic` = 2494,74 km (Δ 0,02%); ✓ classificação ambas as branches (<50 → "Vizinhos", ≥50 → "Não são vizinhos")
- Subcritérios: 2/2/2/2/2 = **10**

### Item 1.4 — Municípios próximos
- Entradas: `Brasília/DF`, raio `500`
- Saída: 207 linhas, ex.: `Novo Gama 32.41 km`, `Anápolis 129.09 km`
- Verificadores: ✓ ordem crescente confirmada programaticamente (`sorted(vals)==vals` → True); ✓ distâncias exatas vs. recálculo (Novo Gama 32.41 = 32.41; Anápolis 129.09 = 129.09); ✓ tabela rich c/ distância
- Subcritérios: 2/2/2/2/2 = **10**

### Item 1.5 — Listar sincronizados
- Entradas: filtro `y` → `GO`; depois `n` (todas)
- Saída: tabela rich com ID IBGE, Município, UF, Latitude, Longitude, Fonte; filtro por UF correto (apenas GO)
- Verificadores: ✓ tabela rich ✓ filtro funcional
- Subcritérios: E-a 2 / E-b 2 / **E-c 0,5** (geopy não influencia a lógica central do item — listagem pura do SQLite; rubrica lida: "deve influenciar parse/validação/cálculo/formatação" — não ocorre neste item; a biblioteca é efetiva nos itens 1.1–1.4, por isso não cai a 0 e a regra R3 não dispara) / E-d 2 / E-e 2 = **8,5**

## 4. Banco de dados
- Tabelas: `municipios`, `sincronizacoes`
- Contagem: `municipios` = 223 (AL 1, DF 1, GO 216, PR 3, RR 1, SP 1); `sincronizacoes` = 2
- Campos exigidos: ✓ `id_ibge`, `nome`, `uf` (CHECK length=2), `latitude/longitude` (CHECK range), `data_consulta` (timestamp ISO), + extras (`fonte_coordenada`, `coordenada_aproximada`, `endereco_retornado`)
- Registro de fallback confirmado: `São Carlos|SP|-23.5505|-46.6333|capital_fallback|1`
- Nota: GO sincronizado a 216/246 — o IBGE hoje retorna 246 municípios p/ GO e a execução foi interrompida por artefato do meu harness (pipe truncado), não falha da app; os 216 gravados estão corretos e o fluxo é incremental (re-sync usa cache).

## 5. Robustez
| Input inválido | Comportamento | Traceback? | Pts |
|---|---|---|---|
| UF `XX` | painel "Informe uma sigla de UF válida." + menu | não | 1 |
| Município `Xyz/DF` | "Xyz não consta na lista do IBGE para DF." + menu | não | 1 |
| Raio `0` | "O raio deve ser maior que zero e menor ou igual a 5.000 km." + menu | não | 1 |
| Raio `-5` | idem (bônus de teste) | não | — |
| Raio `abc` | "Informe um raio numérico válido." + menu | não | — |
| Falha API IBGE (URL 404 via `TAREFA5_IBGE_URL`) | "Nenhum município foi retornado para a UF informada."; app continua (busca por cache funciona depois) | não | F2 ✓ |
| Falha Nominatim (domínio inválido via env) | fallback da capital, flag `aproximada`, sem crash | não | F2 ✓ (bônus) |

## 6. Bônus
| Bônus | Demonstrado? | Evidência | Pts |
|---|---|---|---|
| Fallback capital (bônus do trabalho) | ✓ ao vivo | domínio Nominatim inválido → `São Carlos/SP` com `capital_fallback`/`aproximada=1` no banco | 3,33 |
| Mapa ASCII (bônus do trabalho) | ✓ | grade 60×20 p/ PR com legenda e faixas lat/lon | 3,33 |
| CSV exportado (bônus do trabalho) | ✓ | `exports/municipios_20260915_195241.csv` existe, 222 registros + header, caminho absoluto exibido, módulo `csv` built-in | 3,33 |
| Gerais: export JSON, batch, dashboard, config JSON+env, testes simulados, logging | ✓ | batch 3/3; dashboard rich Layout multi-coluna; env `TAREFA5_NOMINATIM_DOMAIN` aplicada; 35 testes OK (0,26 s); log c/ timestamps (594 linhas) | (teto) |
| **Subtotal (teto 10)** | | | **10** |

## 7. Resultado
- Subtotais: A **10** · B **10** · C **10** · D **5** · E **48,5** · F **5** · G **10**
- Tetos aplicados: nenhum (R1–R5 não dispararam)
- **Total: 98,50 / 100 → Nota: 9,85 / 10**
- **Aprovado? SIM** (≥ 70)

## 8. Observações qualitativas
- **Pontos fortes:** arquitetura em camadas limpa (api/geocoder/DB/serviço/interface) com tipagem completa; `RateLimiter` respeitando o limite do Nominatim; cache com re-sincronização incremental; upsert idempotente + CHECK constraints; 35 testes automatizados (simulados, sem API real) passando; 6+ bônus implementados e demonstráveis; logging rotativo e config por JSON/env; zero `print()` cru.
- **Problemas principais:** (1) E-c de 1.5 em 0,5 — item de listagem não exerce a geopy na lógica central (leitura literal da rubrica). (2) Se o stdout fechar durante a sincronização (ex.: pipe truncado), o `rich Progress` provoca `BrokenPipeError` não tratado e o processo morre sem mensagem amigável — não ocorre em uso interativo terminal, mas é uma fragilidade de robustez fora da lista F.
- **Pendências/limitações:** GO sincronizado a 216/246 por interrupção do avaliador (não da app); o resumo/registro da sincronização de GO não foi gravado pela mesma razão — o fluxo de sync completo foi validado em DF (registro em `sincronizacoes` confirmado). Nenhuma API fora do ar no momento da avaliação.
