# `agent` — CRUD de Agentes

Gerencia configurações de agentes com persistência automática em JSON.

---

## `create(name, system="", max_turns=5, verbose=False)`

Cria um novo agente.

```python
import capataz as cp

cp.agent.create(
    "assistente",
    system="Você é um assistente útil.",
    max_turns=10,
    verbose=False,
)
```

| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| `name` | `str` | — | Nome único do agente |
| `system` | `str` | `""` | System prompt base |
| `max_turns` | `int` | `5` | Máx. iterações do loop ReAct |
| `verbose` | `bool` | `False` | Mostra execução detalhada |

**Exceções:** `ValueError` se nome já existe ou `max_turns`/`verbose` inválidos.

---

## `get(name)`

Obtém configuração do agente.

```python
config = cp.agent.get("assistente")
# → {"system": "...", "max_turns": 5, "verbose": False}
```

**Exceções:** `KeyError` se agente não existe.

---

## `update(name, **kwargs)`

Atualiza um ou mais campos.

```python
cp.agent.update("assistente", max_turns=8, verbose=True)
```

Campos permitidos: `system`, `max_turns`, `verbose`.

**Exceções:** `ValueError` para campo inválido ou tipo errado.

---

## `delete(name)`

Remove um agente e retorna seus dados.

```python
dados = cp.agent.delete("assistente")
```

**Exceções:** `KeyError` se agente não existe.

---

## `list_all()`

Lista todos os agentes cadastrados.

```python
agentes = cp.agent.list_all()
# → ["assistente", "dev", "analista"]
```

---

## Persistência

Os agentes são salvos automaticamente em `capataz_agents.json` no diretório do módulo. Qualquer operação (`create`, `update`, `delete`) persiste imediatamente.

JSON corrompido na carga → inicializa vazio (sem crash).
