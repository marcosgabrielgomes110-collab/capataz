# `Memory` — Sistema de Memória

Gerencia histórico de conversa com suporte a janela de contexto e persistência.

---

## Construtor

```python
from capataz import Memory

# Memória sem persistência
mem = Memory()

# Memória com persistência em arquivo
mem = Memory(persist_path="historico.json")

# Memória com janela de contexto (últimas 6 mensagens)
mem = Memory(persist_path="historico.json", context_size=6)
```

| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| `persist_path` | `str` | `None` | Caminho do arquivo JSON |
| `context_size` | `int` | `None` | Máx. mensagens retornadas por `get()` |

---

## `add(role, content)`

Adiciona uma mensagem ao histórico.

```python
mem.add("user", "Qual o clima?")
mem.add("assistant", "28°C em Fortaleza.")
```

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `role` | `str` | `"user"`, `"assistant"`, `"system"` |
| `content` | `str` | Texto da mensagem |

---

## `get()`

Retorna mensagens para enviar à LLM. Se `context_size` estiver definido, retorna **apenas as últimas N**.

```python
msgs = mem.get()
# → [{"role": "user", "content": "..."}, ...]
```

A lista completa fica preservada internamente para `save()`.

---

## `last_n(n)`

Retorna as últimas N mensagens específicas.

```python
ultimas_3 = mem.last_n(3)
```

Se `n <= 0`, retorna lista vazia.

---

## `save()`

Salva o **histórico completo** em JSON.

```python
mem.save()  # Cria diretórios intermediários se necessário
```

**Exceções:** `ValueError` se `persist_path` não foi definido.

---

## `load()`

Carrega histórico do arquivo. Se o arquivo estiver corrompido, inicia vazio (sem crash).

```python
mem.load()
```

---

## `clear()`

Limpa todo o histórico.

```python
mem.clear()
```

---

## Uso típico

```python
from capataz import Memory

mem = Memory(persist_path="chat.json", context_size=6)

# Carrega histórico salvo (se existir)
# ...

# Adiciona nova interação
mem.add("user", user_input)
# ... executa LLM ...
mem.add("assistant", resposta)

# Persiste ao final
mem.save()
```
