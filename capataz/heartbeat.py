"""
capataz.heartbeat — Daemon que acorda o agente em intervalos

Executa o agente periodicamente com um prompt configurável,
simulando um "coração" autônomo.
"""

import time
import threading
from .session import SessionManager


class Heartbeat:
    """
    Daemon que dispara o agente em intervalos regulares.

    Uso:
        hb = Heartbeat(interval=60, prompt="Resuma o que aconteceu.", agent="monitor")
        hb.start(runner_fn)
        # ... agente roda a cada 60s ...
        hb.stop()
    """

    def __init__(
        self,
        interval: float,
        prompt: str,
        agent_name: str = "chat",
        sessions: SessionManager = None,
        session_id: str = "heartbeat",
        llm_fn=None,
        debug: bool = False,
    ):
        self.interval = interval
        self.prompt = prompt
        self.agent_name = agent_name
        self.sessions = sessions or SessionManager()
        self.session_id = session_id
        self.llm_fn = llm_fn
        self.debug = debug
        self._thread: threading.Thread = None
        self._running = False

    def _loop(self, runner_fn):
        while self._running:
            session = self.sessions.get(self.session_id)
            try:
                runner_fn(
                    agent_name=self.agent_name,
                    user_input=self.prompt,
                    memory=session,
                    llm_fn=self.llm_fn,
                    debug=self.debug,
                )
                session.save()
            except Exception as e:
                if self.debug:
                    print(f"[heartbeat] Erro: {e}")
            time.sleep(self.interval)

    def start(self, runner_fn):
        """
        Inicia o heartbeat em uma thread separada.

        runner_fn: função compatível com capataz.run() (mesma assinatura).
        """
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, args=(runner_fn,), daemon=True)
        self._thread.start()

    def stop(self):
        """Para o heartbeat."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)

    @property
    def is_running(self) -> bool:
        return self._running
