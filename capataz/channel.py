"""
capataz.channel — Adaptadores de canal (CLI, Telegram, etc.)

Cada canal escuta mensagens, converte para formato padrão
e as encaminha para o agente.
"""

import sys
from abc import ABC, abstractmethod
from .session import SessionManager


class Channel(ABC):
    """Base para adaptadores de canal."""

    @abstractmethod
    def start(self):
        """Inicia o canal (bloqueante)."""
        ...

    @abstractmethod
    def stop(self):
        """Para o canal."""
        ...

    @abstractmethod
    def reply(self, user_id: str, text: str):
        """Envia resposta de volta para o usuário."""
        ...


class CLIChannel(Channel):
    """
    Canal interativo via terminal (stdin).
    Cada linha de input é uma mensagem do usuário.
    """

    def __init__(self, sessions: SessionManager = None):
        self.sessions = sessions or SessionManager()
        self._running = False

    def start(self):
        """
        Loop de input. Cada linha vira user_id = "cli:{n}".
        Retorna quando o usuário digitar 'sair'.
        """
        self._running = True
        print("🤠 capataz CLI — digite 'sair' para encerrar\n")
        turn = 0
        while self._running:
            try:
                user_input = input("Você: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if not user_input:
                continue
            if user_input.lower() == "sair":
                break

            turn += 1
            user_id = f"cli:{turn}"
            yield user_id, user_input

        self.stop()

    def stop(self):
        self._running = False

    def reply(self, user_id: str, text: str):
        print(f"Assistente: {text}\n")


class TelegramChannel(Channel):
    """
    Canal via Telegram Bot.

    Requer: pip install python-telegram-bot

    Uso:
        tg = TelegramChannel(token="TOKEN")
        def handler(user_id, text):
            return resposta
        tg.start(handler)
    """

    def __init__(self, token: str, sessions: SessionManager = None):
        self.token = token
        self.sessions = sessions or SessionManager()
        self._app = None

    def start(self, message_handler: callable):
        """
        Inicia o bot. message_handler(user_id: str, text: str) -> str
        Bloqueia a thread principal.
        """
        try:
            from telegram import Update
            from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
        except ImportError:
            raise ImportError(
                "TelegramChannel requer 'python-telegram-bot'. Instale com:\n"
                "  pip install python-telegram-bot"
            )

        async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user_id = str(update.effective_user.id)
            text = update.message.text
            response = message_handler(user_id, text)
            await update.message.reply_text(response)

        async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text("🤠 capataz — pronto para ajudar!")

        self._app = Application.builder().token(self.token).build()
        self._app.add_handler(CommandHandler("start", handle_start))
        self._app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
        )

        self._app.run_polling()

    def stop(self):
        if self._app:
            self._app.stop()

    def reply(self, user_id: str, text: str):
        # Telegram responde no handler, não aqui
        pass
