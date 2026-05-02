"""
capataz.tool — Cadastro de tools
"""

import traceback

_registry: dict = {}


def tool(name: str = None, *, desc: str = ""):
    """Decorator para registrar uma tool.

    Uso:
        @cp.tool("nome")
        def minha_tool(args): ...

        @cp.tool("nome", desc="Faz algo específico")
        def minha_tool(args): ...
    """
    def decorator(fn):
        final_name = name or fn.__name__
        _registry[final_name] = {
            "fn": fn,
            "desc": desc or fn.__doc__ or "Sem descrição.",
        }
        return fn

    if callable(name):
        fn = name
        _registry[fn.__name__] = {
            "fn": fn,
            "desc": fn.__doc__ or "Sem descrição.",
        }
        return fn

    return decorator


def call(name: str, args: dict):
    """Executa uma tool pelo nome."""
    if name not in _registry:
        return f"[ERRO] Tool '{name}' não encontrada. Disponíveis: {list(_registry.keys())}"
    try:
        return str(_registry[name]["fn"](args))
    except Exception as e:
        tb = traceback.format_exc()
        return f"[ERRO] Tool '{name}' falhou: {e}\n{tb}"


def list_tools() -> list:
    """Retorna lista de tools registradas."""
    return list(_registry.keys())


def describe_tools() -> str:
    """Retorna descrição das tools para o system prompt."""
    if not _registry:
        return "Nenhuma tool disponível."
    lines = []
    for name, entry in _registry.items():
        lines.append(f"- {name}: {entry['desc'].strip()}")
    return "\n".join(lines)
