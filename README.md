# Correção automatizada de trabalhos (experimento)

Experimento em estágio inicial: correção padronizada de trabalhos de programação por agentes locais de IA (LLM). Testado com cyankiwi/Qwen3.8-27B-AWQ-INT4 via vLLM.

## Estrutura

| Item | Papel |
|---|---|
| `tarefas.md` | Especificação dos 12 trabalhos de Python ("Bibliotecas Externas em Python") |
| `01/` … `09/` | Entregas das duplas — cada pasta é um trabalho a corrigir |
| `rubrica.md` | Rubrica do corretor: protocolo, grade (100 pts), tetos (R1–R5), roteiros por trabalho |
| `relatorio_*.md` | Saídas das correções já geradas (uma por trabalho) |

## Como funciona

1. **Correção por agente:** cada agente corrige uma única pasta do trabalho, seguindo a `rubrica.md` (análise estática como base; execução opcional, só em sandbox `_avaliacao/` dentro da pasta do trabalho).
2. **Isolamento:** as correções rodam simultâneas, por agentes diferentes, no mesmo ambiente — cada um toca apenas a sua pasta e não modifica o código entregue.
3. **Saída:** relatório de avaliação em pt-BR com nota 0–100, tetos aplicados e justificativa de cada ponto, como feedback para a dupla.

## Ambiente

- Devcontainer (`.devcontainer/`): Node 22 + [Pi](https://github.com/badlogic/pi-mono) coding agent, com LLM local via vLLM (`Qwen3.8-27B`).
- `.venv_eval/`: venv de Python para avaliação; `.vscode/settings.json`: apenas convenções (EOL).
