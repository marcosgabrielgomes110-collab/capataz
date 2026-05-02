"""
capataz.session — Gerenciador de sessões multi-usuário

Cada sessão tem seu próprio Memory, isolado dos demais.
"""

import os
from .memory import Memory


class SessionManager:
    """Gerencia múltiplas sessões de conversa independentes."""

    def __init__(self, persist_dir: str = None, context_size: int = None):
        self._sessions: dict[str, Memory] = {}
        self.persist_dir = persist_dir or "."
        self.context_size = context_size

    def _mem_path(self, session_id: str) -> str:
        return os.path.join(self.persist_dir, f"session_{session_id}.json")

    def get(self, session_id: str) -> Memory:
        """
        Obtém a sessão pelo ID. Cria automaticamente se não existir.

        session_id: identificador único (user_id, chat_id, canal, etc.)
        Retorna o Memory associado.
        """
        if session_id not in self._sessions:
            self._sessions[session_id] = Memory(
                persist_path=self._mem_path(session_id),
                context_size=self.context_size,
            )
        return self._sessions[session_id]

    def delete(self, session_id: str):
        """Remove uma sessão (memória e arquivo)."""
        mem = self._sessions.pop(session_id, None)
        if mem and mem.persist_path and os.path.exists(mem.persist_path):
            os.remove(mem.persist_path)

    def clear(self, session_id: str):
        """Limpa o histórico de uma sessão sem removê-la."""
        if session_id in self._sessions:
            self._sessions[session_id].clear()
            self._sessions[session_id].save()

    def list_sessions(self) -> list[str]:
        """Lista todos os IDs de sessão ativos."""
        return list(self._sessions.keys())

    def save_all(self):
        """Persiste todas as sessões em disco."""
        for mem in self._sessions.values():
            mem.save()
