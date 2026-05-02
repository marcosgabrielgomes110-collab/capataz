# `decider` — Loop ReAct

Coração da lib. Executa o loop **Thought → Action → Observation → Final Answer** até a LLM dar uma resposta final.

> ⚠️ Uso direto raramente necessário. Prefira [`cp.run()`](runner.md).

---

## `run_loop(messages, system_prompt, max_turns=5, verbose=False, llm_fn=None)`

Executa o loop ReAct.

```python
from capataz.decider import run_loop

resultado = run_loop(
    messages=[{"role": "user", "content": "Olá!"}],
    system_prompt="Você é um assistente.",
    max_turns=5,
    verbose=False,
    llm_fn=minha_funcao_llm,   # opcional, escopado (não altera global)
)
```

| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| `messages` | `list[dict]` | — | Histórico `[{"role", "content"}]` |
| `system_prompt` | `str` | — | Prompt do sistema com tools |
| `max_turns` | `int` | `5` | Máx. iterações |
| `verbose` | `bool` | `False` | Printa cada turno e tool |
| `llm_fn` | `callable` | `None` | LLM escopada (não toca o global) |

**Retorno:** `str` com a resposta final (`Final Answer:`) ou texto direto da LLM.

---

## Formato esperado da LLM

### Com tool:
```
Thought: Preciso do clima.
Action: clima
Action Input: {"cidade": "Fortaleza"}
```

### Múltiplas tools no mesmo turno:
```
Thought: Preciso do clima e de um cálculo.
Action: clima
Action Input: {"cidade": "Fortaleza"}
Action: calc
Action Input: {"expr": "2+2"}
```

### Resposta final:
```
Thought: Já tenho os dados.
Final Answer: Fortaleza está a 28°C.
```

### Resposta direta (sem Action):
```
Thought: Vou responder.
Final Answer: Olá! Como posso ajudar?
```

---

## Observação

Se a LLM chamar a **mesma sequência de tools** repetidamente (3x), o loop é interrompido automaticamente para evitar loops infinitos.
