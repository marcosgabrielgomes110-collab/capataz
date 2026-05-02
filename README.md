# 🤠 capataz

> Lib leve de agentes ReAct em Python.  
> Filosofia: **Lego** — peças independentes, sem magia, sem peso.

---

## Instalação

```bash
pip install git+https://github.com/marcosgabrielgomes110-collab/capataz.git
```

Dependências: nenhuma (stdlib pura). A LLM é plugada pelo usuário.

---

## Quick Start

```python
import capataz as cp

# 1. Sua LLM (qualquer provider)
def llm(messages: list[dict]) -> str:
    # messages = [{"role": "system/user/assistant", "content": "..."}]
    return "Final Answer: resposta"

cp.set_llm(llm)

# 2. Tools
@cp.tool("clima", desc="Clima de uma cidade. Parâmetro: cidade (str).")
def clima(args: dict) -> str:
    return f"{args['cidade']}: 28°C"

# 3. Agente
cp.agent.create("bot", system="Você é um assistente.")

# 4. Executa
print(cp.run("bot", "Qual o clima em Fortaleza?"))
```

---

## Módulos

| Módulo | Descrição |
|---|---|
| [`agent`](docs/agent.md) | CRUD de agentes com persistência JSON |
| [`decider`](docs/decider.md) | Loop ReAct: Thought → Action → Observation |
| [`memory`](docs/memory.md) | Memória com janela de contexto e persistência |
| [`prompt`](docs/prompt.md) | Gerador de system prompt ReAct |
| [`tools`](docs/tools.md) | Registro e execução de ferramentas |
| [`skills`](docs/skills.md) | Skills injetáveis via arquivos `.md` |
| [`runner`](docs/runner.md) | Interface principal `run()` |

Documentação completa em [`docs/`](docs/index.md).

---

## Funcionalidades

### Múltiplas tools por turno

A LLM pode chamar várias tools numa única resposta — todas são executadas antes de voltar para a LLM.

```
Thought: Preciso do clima e de um cálculo.
Action: clima
Action Input: {"cidade": "Fortaleza"}
Action: calc
Action Input: {"expr": "2+2"}
```

### Skills injetáveis

Skills são arquivos `.md` com instruções que entram no system prompt automaticamente quando o input do usuário ativa um gatilho.

```python
cp.skills.load("./skills/")
cp.run("bot", "pesquisar...")     # skill busca_web injetada automaticamente
```

### Memória com janela de contexto

```python
from capataz import Memory

mem = Memory(persist_path="hist.json", context_size=6)
cp.run("bot", "Olá!", memory=mem)
mem.save()
```

### Debug

```python
cp.run("bot", "pesquisar algo", debug=True)
```

Mostra skills ativadas, cada turno da LLM e cada tool executada.

### LLM escopada

```python
cp.run("bot", "oi", llm_fn=minha_llm_temporaria)  # não altera o global
```

---

## CLI

```bash
# Chat interativo via terminal
python -m capataz

# ou se instalado com pip
capataz
```

---

## Contrato da LLM

```python
def sua_llm(messages: list[dict]) -> str:
    return "Final Answer: ..."   # ou Action: ... + Action Input: ...
```

A LLM deve seguir o formato ReAct:
- `Action: nome` + `Action Input: {"param": "valor"}` para chamar tools
- Pode chamar **várias tools na mesma resposta**
- `Final Answer: texto` para responder ao usuário

---

## Licença

MIT

---

## Criador

**Marcos Gabriel Gomes**

- GitHub: [marcosgabrielgomes110-collab](https://github.com/marcosgabrielgomes110-collab)
- Email: marcosgabrielgomes110@gmail.com

---

> Feito com 🤠 para simplificar agentes com LLM.
