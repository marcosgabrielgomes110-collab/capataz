# `run()` — Interface Principal

Função principal para executar um agente. Junta todos os módulos (prompt, tools, skills, memória, decider) numa chamada só.

---

## `run(agent_name, user_input, llm_fn=None, memory=None, context_size=None, debug=False)`

```python
import capataz as cp

# Uso básico
resposta = cp.run("meu_agente", "Qual o clima?")

# Com memória persistente
from capataz import Memory
mem = Memory(persist_path="chat.json", context_size=6)
resposta = cp.run("meu_agente", "Olá!", memory=mem)

# Com LLM escopada (não altera global)
resposta = cp.run("meu_agente", "Oi", llm_fn=minha_llm_temp)

# Com debug
resposta = cp.run("meu_agente", "pesquisar algo", debug=True)
```

| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| `agent_name` | `str` | — | Nome do agente (criado via `cp.agent.create()`) |
| `user_input` | `str` | — | Mensagem do usuário |
| `llm_fn` | `callable` | `None` | LLM escopada (não altera o global) |
| `memory` | `Memory` | `None` | Objeto Memory para histórico |
| `context_size` | `int` | `None` | Sobrescreve o `context_size` da Memory |
| `debug` | `bool` | `False` | Mostra skills ativadas e execução detalhada |

**Retorno:** `str` com a resposta final do agente.

---

## Fluxo interno

```
run("chat", "pesquisar Python")
  │
  ├─ 1. agent.get("chat") → {system, max_turns, verbose}
  │
  ├─ 2. memory.add("user", "pesquisar Python")
  │
  ├─ 3. prompt.build(system) → system prompt com tools + few-shot
  │
  ├─ 4. skills.inject(system, input) → skills ativadas incluídas
  │     └─ debug: mostra skills ativadas
  │
  ├─ 5. decider.run_loop(messages, system_prompt, max_turns, llm_fn)
  │     └─ debug: verbose ligado automaticamente
  │
  └─ 6. memory.add("assistant", resultado)
       return resultado
```

---

## Debug

Com `debug=True`, o runner mostra:

```
[debug] Skills ativadas:
  - busca_web (gatilhos: buscar, pesquisar, ..., prioridade: alta)

[capataz | turno 1]
Thought: Preciso pesquisar...
Action: terminal
Action Input: {"comando": "..."}

[capataz | tool] terminal({"comando": "..."}) → resultado
```

---

## Exemplos completos

```python
import capataz as cp
from capataz import Memory

# Configura LLM
def llm(messages):
    return "Final Answer: resposta"

cp.set_llm(llm)

# Tools
@cp.tool("calc", desc="Calculadora. Parâmetro: expr (str).")
def calc(args):
    return str(eval(args.get("expr", "0")))

# Agente
cp.agent.create("assistente", system="Você ajuda.", max_turns=5)

# Skills
cp.skills.load("./exemplo_skills/")

# Memória com janela de 6 mensagens
mem = Memory(persist_path="chat.json", context_size=6)

# Execução
print(cp.run("assistente", "calcula 2+2", memory=mem))
# Debug opcional
print(cp.run("assistente", "pesquisar", debug=True))
```
