# `tools` — Registro de Ferramentas

Sistema para registrar e executar funções que a LLM pode chamar (tools).

---

## `@tool(name, desc="")`

Decorator para registrar uma tool.

```python
import capataz as cp

# Com nome explícito e descrição
@cp.tool("clima", desc="Clima de uma cidade. Parâmetro: cidade (str).")
def clima(args: dict) -> str:
    cidade = args.get("cidade", "desconhecida")
    return f"{cidade}: 28°C"

# Nome = nome da função
@cp.tool
def calc(args: dict) -> str:
    """Calcula expressão matemática. Parâmetro: expr (str)."""
    return str(eval(args.get("expr", "0")))

# Sem parênteses, sem descrição (usa docstring)
@cp.tool
def minha_tool(args: dict) -> str:
    """Descrição usada automaticamente."""
    return "ok"
```

| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| `name` | `str` | `fn.__name__` | Nome usado pela LLM |
| `desc` | `str` | `fn.__doc__` | Descrição para o system prompt |

A função registrada **recebe um único `dict`** com os parâmetros.

---

## `call(name, args)`

Executa uma tool pelo nome.

```python
from capataz import tools

resultado = tools.call("clima", {"cidade": "São Paulo"})
# → "São Paulo: 28°C"
```

Se a tool não existir ou falhar, retorna string com `[ERRO]` prefixado.

---

## `list_tools()`

Lista todas as tools registradas.

```python
tools.list_tools()
# → ["clima", "calc"]
```

---

## `describe_tools()`

Gera descrição formatada para o system prompt.

```python
tools.describe_tools()
# → "- clima: Clima de uma cidade. Parâmetro: cidade (str).\n- calc: ..."
```

---

## Boas práticas

1. **Nomes curtos e em português** (a LLM vai chamar pelo nome)
2. **`desc` clara** com parâmetros e exemplo
3. **Parâmetro único `dict`** — a LLM enviará `Action Input: {"chave": "valor"}`
4. **Trate erros internamente** — retorne string explicativa
5. **Nunca use `eval()` em produção** — prefira `ast.literal_eval` ou um parser seguro
