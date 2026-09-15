trabalho 09:

de: [https://github.com/Zidrewndacht/BFD_Tarefa_2/blob/main/tarefas.md](https://github.com/Zidrewndacht/BFD_Tarefa_2/blob/main/tarefas.md)

Trabalho 9 — Tabela FIPE com Valores por Extenso
Biblioteca-tempero: num2words
API sugerida: https://brasilapi.com.br/api/fipe/preco/v1/{codigoFipe} (e endpoints auxiliares de marcas/modelos)

Descrição geral
Aplicação que consulta preços de veículos na tabela FIPE e converte os valores numéricos para representação por extenso em português. A biblioteca num2words deve ser usada para transformar qualquer valor monetário ou inteiro em texto por extenso.

Menu inicial e comportamento
Consultar preço por código FIPE

Solicita o código FIPE (padrão alfanumérico) e o tipo de veículo (carro, moto, caminhão).
Consulta a API. Se o código for inválido ou não retornar dados, informa o usuário e retorna ao menu.
Armazena no SQLite: código FIPE, marca, modelo, ano, preço numérico e preço por extenso.
Exibe em tabela rich: veículo, ano, preço numérico e preço por extenso completo.
Listar marcas por tipo

Solicita o tipo de veículo.
Consulta a API de marcas.
Armazena as marcas no SQLite com uma flag indicando que são metadados de catálogo.
Exibe em tabela rich: código da marca, nome e quantidade de modelos já consultados (se houver histórico).
Listar modelos por marca

Solicita o código de uma marca.
Consulta a API de modelos.
Armazena no SQLite vinculado à marca.
Exibe em tabela rich: código do modelo, nome e preço médio dos anos já consultados (se houver).
Comparar preços de dois veículos

Solicita dois códigos FIPE.
Consulta ambos (ou recupera do SQLite se já existirem).
Exibe comparação lado a lado em rich: modelo, ano, preço numérico, preço por extenso e diferença absoluta (também por extenso).
Indica qual é o mais caro e qual é o mais barato.
Histórico de consultas

Lista todas as consultas de preço armazenadas no SQLite.
Permite filtro por tipo de veículo, por marca ou por faixa de preço.
Exibe em tabela rich com todas as colunas, incluindo o preço por extenso.
