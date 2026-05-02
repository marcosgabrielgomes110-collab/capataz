# `channel` — Adaptadores de Canal

Adapta diferentes canais de entrada (CLI, Telegram, etc.) para o formato padrão de mensagens do capataz.

---

## `Channel` (ABC)

Classe base abstrata. Todos os canais implementam:

| Método | Descrição |
|---|---|
| `start()` | Inicia o canal (bloqueante) |
| `stop()` | Para o canal |
| `reply(user_id, text)` | Envia resposta de volta |

---

## `CLIChannel(sessions=None)`

Canal interativo via terminal.

```python
from capataz import CLIChannel, SessionManager

sessions = SessionManager()
cli = CLIChannel(sessions=sessions)

for user_id, text in cli.start():
    mem = sessions.get(user_id)
    resposta = cp.run("bot", text, memory=mem)
    cli.reply(user_id, resposta)
    mem.save()
```

`cli.start()` é um **gerador** — a cada linha do terminal, produz `(user_id, text)`. O `user_id` é auto-incrementado como `"cli:1"`, `"cli:2"`, etc.

| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| `sessions` | `SessionManager` | `None` | Gerencia sessões por user |

---

## `TelegramChannel(token, sessions=None)`

Canal via Telegram Bot.

```python
from capataz import TelegramChannel, SessionManager

sessions = SessionManager()
tg = TelegramChannel(token="SEU_TOKEN", sessions=sessions)

def handler(user_id: str, text: str) -> str:
    mem = sessions.get(user_id)
    resp = cp.run("bot", text, memory=mem)
    mem.save()
    return resp

tg.start(handler)  # bloqueia a thread principal
```

| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| `token` | `str` | — | Token do bot Telegram |
| `sessions` | `SessionManager` | `None` | Gerencia sessões por user |

Dependências opcionais (só se usar TelegramChannel):
```bash
pip install python-telegram-bot
```

---

## Implementando um canal customizado

```python
from capataz.channel import Channel

class WhatsAppChannel(Channel):
    def __init__(self, phone: str, sessions=None):
        self.phone = phone
        self.sessions = sessions or SessionManager()

    def start(self):
        # conecta no WhatsApp, escuta mensagens
        ...

    def stop(self):
        # desconecta
        ...

    def reply(self, user_id: str, text: str):
        # envia resposta via WhatsApp
        ...
```
