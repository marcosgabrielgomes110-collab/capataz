# `session` — Gerenciador de Sessões

Gerencia múltiplas sessões de conversa independentes. Cada sessão tem seu próprio `Memory` com persistência isolada.

---

## `SessionManager(persist_dir=".", context_size=None)`

```python
from capataz import SessionManager

sessions = SessionManager(
    persist_dir="./data/",    # onde salvar os JSONs
    context_size=6,           # janela de contexto por sessão
)
```

| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| `persist_dir` | `str` | `"."` | Diretório de persistência |
| `context_size` | `int` | `None` | Janela de contexto por sessão |

---

## `get(session_id)`

Obtém (ou cria) a sessão pelo ID.

```python
mem = sessions.get("user_42")
# → Memory(persist_path="./data/session_user_42.json", context_size=6)

mem.add("user", "Olá!")
```

Se a sessão não existe, cria automaticamente com arquivo `{persist_dir}/session_{session_id}.json`.

---

## `delete(session_id)`

Remove uma sessão e seu arquivo de persistência.

```python
sessions.delete("user_42")
```

---

## `clear(session_id)`

Limpa o histórico da sessão sem removê-la.

```python
sessions.clear("user_42")
```

---

## `list_sessions()`

Lista todos os IDs de sessão ativos em memória.

```python
sessions.list_sessions()
# → ["user_42", "chat_telegram_123", "heartbeat"]
```

---

## `save_all()`

Persiste todas as sessões em disco de uma vez.

```python
sessions.save_all()
```

---

## Exemplo completo

```python
import capataz as cp
from capataz import SessionManager

cp.set_llm(minha_llm)
cp.agent.create("bot", system="Seja útil.")

sessions = SessionManager(persist_dir="./data/", context_size=6)

def responder(user_id: str, texto: str) -> str:
    mem = sessions.get(user_id)
    resp = cp.run("bot", texto, memory=mem)
    mem.save()
    return resp

print(responder("ana", "Oi!"))
print(responder("joao", "Olá!"))
print(responder("ana", "Lembra de mim?"))
# "ana" e "joao" têm históricos independentes
```
