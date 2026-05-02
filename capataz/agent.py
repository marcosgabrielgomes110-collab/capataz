"""
capataz.agent — CRUD de agentes com persistência JSON
"""

import json
import os

_agents: dict = {}
_persist_file: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "capataz_agents.json")


def _save():
    os.makedirs(os.path.dirname(_persist_file) or ".", exist_ok=True)
    with open(_persist_file, "w", encoding="utf-8") as f:
        json.dump(_agents, f, ensure_ascii=False, indent=2)


def _load():
    global _agents
    if os.path.exists(_persist_file):
        try:
            with open(_persist_file, "r", encoding="utf-8") as f:
                _agents = json.load(f)
        except (json.JSONDecodeError, IOError):
            _agents = {}


# Carrega agentes salvos ao importar
_load()


def create(name: str, system: str = "", max_turns: int = 5, verbose: bool = False):
    """Cria um novo agente."""
    if name in _agents:
        raise ValueError(f"Agente '{name}' já existe. Use update() para modificar.")
    if not isinstance(max_turns, int) or max_turns < 1:
        raise ValueError("max_turns deve ser um inteiro >= 1.")
    if not isinstance(verbose, bool):
        raise ValueError("verbose deve ser True ou False.")
    _agents[name] = {
        "system": system,
        "max_turns": max_turns,
        "verbose": verbose,
    }
    _save()
    return _agents[name]


def get(name: str) -> dict:
    """Retorna configuração de um agente."""
    if name not in _agents:
        raise KeyError(f"Agente '{name}' não encontrado.")
    return _agents[name]


def update(name: str, **kwargs):
    """Atualiza campos de um agente."""
    if name not in _agents:
        raise KeyError(f"Agente '{name}' não encontrado.")
    allowed = {"system", "max_turns", "verbose"}
    for key in kwargs:
        if key not in allowed:
            raise ValueError(f"Campo inválido: '{key}'. Permitidos: {allowed}")
    if "max_turns" in kwargs and (not isinstance(kwargs["max_turns"], int) or kwargs["max_turns"] < 1):
        raise ValueError("max_turns deve ser um inteiro >= 1.")
    if "verbose" in kwargs and not isinstance(kwargs["verbose"], bool):
        raise ValueError("verbose deve ser True ou False.")
    _agents[name].update(kwargs)
    _save()
    return _agents[name]


def delete(name: str) -> dict:
    """Remove um agente."""
    if name not in _agents:
        raise KeyError(f"Agente '{name}' não encontrado.")
    removed = _agents.pop(name)
    _save()
    return removed


def list_all() -> list:
    """Lista todos os agentes cadastrados."""
    return list(_agents.keys())
