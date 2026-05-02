# capataz

**Lib leve de agentes ReAct** — Lego para LLMs.

Filosofia: peças independentes, sem magia, sem peso.

---

## Instalação

```bash
pip install .
```

Dependências: nenhuma (usa apenas stdlib). A comunicação com a LLM é feita via função passada pelo usuário.

---

## Quick Start

```python
import capataz as cp

# 1. Define sua LLM
def minha_llm(messages: list[dict]) -> str:
    # messages = [{"role": "system", "content": "..."},
    #              {"role": "user", "content": "..."}]
    # retorna texto da LLM (pode conter Action:, Final Answer:, etc.)
    return resposta

cp.set_llm(minha_llm)

# 2. Cria tools
@cp.tool("clima", desc="Clima de uma cidade. Parâmetro: cidade (str).")
def clima(args: dict) -> str:
    return f"{args['cidade']}: 28°C"

# 3. Cria um agente
cp.agent.create("assistente", system="Você é um assistente.")

# 4. Executa
resposta = cp.run("assistente", "Qual o clima em Fortaleza?")
print(resposta)
```

---

## Módulos

| Módulo | Descrição |
|---|---|
| [`agent`](agent.md) | CRUD de agentes com persistência JSON |
| [`decider`](decider.md) | Loop ReAct: Thought → Action → Observation |
| [`memory`](memory.md) | Memória de curto/longo prazo com janela de contexto |
| [`prompt`](prompt.md) | Gerador de system prompt ReAct |
| [`tools`](tools.md) | Registro e execução de ferramentas |
| [`skills`](skills.md) | Skills injetáveis via arquivos .md |
| [`runner`](runner.md) | Interface principal `run()` |

---

## API Pública

```python
import capataz as cp

cp.set_llm(fn)                        # Define LLM global
cp.run(agent, input, **opts)           # Executa agente
cp.tool(name, desc="")                 # Decorator de tool

cp.agent.create(name, **config)        # Cria agente
cp.agent.get(name)                     # Obtém config
cp.agent.update(name, **kwargs)        # Atualiza campos
cp.agent.delete(name)                  # Remove agente
cp.agent.list_all()                    # Lista agentes

cp.skills.load(path, match_mode)       # Carrega skills
cp.skills.list_all()                   # Lista skills carregadas
cp.skills.match(user_input)            # Skills ativadas
cp.skills.inject(system_prompt, input) # Injeta no prompt

Memory(persist_path, context_size)     # Construtor
Memory.add(role, content)              # Adiciona mensagem
Memory.get()                           # Últimas N mensagens
Memory.last_n(n)                       # Últimas N específicas
Memory.save() / .load() / .clear()     # Persistência
```
