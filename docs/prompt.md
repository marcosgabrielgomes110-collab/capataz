# `prompt` — Gerador de System Prompt

Constrói o system prompt completo com template ReAct, descrição das tools e exemplos few-shot.

---

## `build(system="", extra="")`

Monta o system prompt final.

```python
from capataz import prompt as prompt_module

prompt_completo = prompt_module.build(
    system="Você é um analista de dados.",
    extra="Instruções extras aqui.",
)
```

| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| `system` | `str` | `""` | System prompt base do agente |
| `extra` | `str` | `""` | Texto adicional inserido no template |

### Saída gerada:

```
Você é um analista de dados.       ← system

Você é um agente autônomo que resolve tarefas usando tools.
## Formato de resposta
...

## Ferramentas disponíveis
- clima: Retorna o clima de uma cidade.
- calc: Calcula expressão matemática.

## Exemplos
Usuário: Quanto é 3.14 * 2.5?
Thought: Vou usar a tool calc.
Action: calc
Action Input: {"expr": "3.14 * 2.5"}

{extra}                              ← parâmetro extra
```

---

## Como funciona

1. Busca tools registradas via `tools.describe_tools()`
2. Gera exemplos few-shot apenas para tools que **existem** no registro
3. Aplica template ReAct com placeholders preenchidos
4. Adiciona system prompt do agente como prefixo (se fornecido)

> ⚠️ O `runner` já chama `prompt.build()` internamente. Raramente você precisa chamá-lo diretamente.
