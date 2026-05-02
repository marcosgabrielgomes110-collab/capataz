# `heartbeat` — Daemon Autônomo

Executa o agente periodicamente com um prompt configurável. O agente "acorda" sozinho, age sem ser chamado.

---

## `Heartbeat(interval, prompt, agent_name="chat", sessions=None, session_id="heartbeat", llm_fn=None, debug=False)`

```python
from capataz import Heartbeat

hb = Heartbeat(
    interval=60,                # segundos entre execuções
    prompt="Verifique se há novidades.",
    agent_name="monitor",       # agente a ser usado
    session_id="monitor",       # ID da sessão (memória)
    debug=True,
)
```

| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| `interval` | `float` | — | Segundos entre disparos |
| `prompt` | `str` | — | Prompt enviado ao agente a cada ciclo |
| `agent_name` | `str` | `"chat"` | Nome do agente |
| `sessions` | `SessionManager` | `None` | Gerencia sessões |
| `session_id` | `str` | `"heartbeat"` | ID da sessão do heartbeat |
| `llm_fn` | `callable` | `None` | LLM escopada |
| `debug` | `bool` | `False` | Mostra execução detalhada |

---

## `start(runner_fn)`

Inicia o heartbeat em uma **thread daemon** separada. O `runner_fn` deve ter a mesma assinatura de `cp.run()`.

```python
import capataz as cp

hb = Heartbeat(interval=30, prompt="Analise o contexto atual.")
hb.start(cp.run)  # dispara cp.run() a cada 30s

# o programa continua rodando...
input("Pressione Enter para parar...")
hb.stop()
```

---

## `stop()`

Para o heartbeat e aguarda a thread finalizar (timeout de 5s).

```python
hb.stop()
```

---

## `is_running` (property)

```python
if hb.is_running:
    print("Heartbeat ativo")
```

---

## Exemplo completo

```python
import capataz as cp
from capataz import Heartbeat, SessionManager

cp.set_llm(minha_llm)

@cp.tool("log", desc="Registra evento. Parâmetro: evento (str).")
def log(args):
    with open("log.txt", "a") as f:
        f.write(f"{args.get('evento')}\n")
    return "ok"

cp.agent.create("monitor", system="Você é um monitor autônomo. Use a tool log.")

# Heartbeat a cada 5 minutos
hb = Heartbeat(
    interval=300,
    prompt="Analise os eventos recentes e registre um resumo no log.",
    agent_name="monitor",
    debug=True,
)

hb.start(cp.run)

# Programa principal continua
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    hb.stop()
```
