"""
capataz — Lib leve de agentes ReAct
Filosofia: Lego — peças independentes, sem magia, sem peso.
"""

from . import agent
from . import decider
from . import skills
from . import tools
from .tools import tool
from .memory import Memory
from .runner import run
from . import session
from .session import SessionManager
from . import channel
from .channel import CLIChannel
from . import heartbeat
from .heartbeat import Heartbeat


def set_llm(fn):
    """Define a função LLM global. fn(messages: list[dict]) -> str"""
    if not callable(fn):
        raise TypeError(f"set_llm espera uma função, recebeu {type(fn).__name__}")
    decider.set_llm(fn)


__all__ = [
    "agent",
    "skills",
    "tool",
    "tools",
    "Memory",
    "SessionManager",
    "CLIChannel",
    "Heartbeat",
    "run",
    "set_llm",
    "decider",
    "session",
    "channel",
    "heartbeat",
]
