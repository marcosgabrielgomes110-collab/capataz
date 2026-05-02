"""
capataz.memory — Memória de curto e longo prazo
"""

import json
import os


class Memory:
    def __init__(self, persist_path: str = None, context_size: int = None):
        self.messages: list[dict] = []
        self.persist_path = persist_path
        self.context_size = context_size
        if persist_path and os.path.exists(persist_path):
            self.load()

    def add(self, role: str, content: str):
        """Adiciona mensagem ao histórico."""
        self.messages.append({"role": role, "content": content})

    def get(self) -> list[dict]:
        """
        Retorna mensagens para o contexto.
        Se context_size estiver definido, retorna apenas as últimas N.
        """
        if self.context_size and self.context_size > 0:
            return self.messages[-self.context_size:]
        return self.messages

    def clear(self):
        """Limpa histórico."""
        self.messages = []

    def _ensure_dirs(self):
        if self.persist_path:
            os.makedirs(os.path.dirname(self.persist_path) or ".", exist_ok=True)

    def save(self):
        """Persiste memória em JSON."""
        if not self.persist_path:
            raise ValueError("persist_path não definido.")
        self._ensure_dirs()
        with open(self.persist_path, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=2)

    def load(self):
        """Carrega memória do JSON."""
        if not self.persist_path:
            raise ValueError("persist_path não definido.")
        try:
            with open(self.persist_path, "r", encoding="utf-8") as f:
                self.messages = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            self.messages = []

    def last_n(self, n: int) -> list[dict]:
        """Retorna as últimas N mensagens."""
        if n <= 0:
            return []
        return self.messages[-n:]
