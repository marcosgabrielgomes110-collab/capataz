# `.env` — Configuração por Variáveis de Ambiente

O `main.py` usa variáveis de ambiente para configuração. Crie um arquivo `.env` na raiz do projeto (ou copie o existente).

---

## Arquivo completo

```env
# ─── LLM ─────────────────────────────────────────────────────

# Modelo da LLM (formato: provider/modelo)
LLM_MODEL=seu-modelo-aqui

# Chave de API do provedor
API_KEY=sua_chave_aqui

# ─── Identificação ────────────────────────────────────────────

# ID do usuário (define o arquivo de memória: memoria_{USER_ID}.json)
USER_ID=default

# ─── Skills ───────────────────────────────────────────────────

# Pasta com arquivos .md de skills
SKILLS_DIR=./exemplo_skills/

# ─── Memória ──────────────────────────────────────────────────

# Limita o contexto às últimas N mensagens (vazio = histórico completo)
# CONTEXT_SIZE=6

# ─── Debug ────────────────────────────────────────────────────

# Ativa logs detalhados (skills ativadas, tools executadas, cada turno)
# DEBUG=true
```

---

## Parâmetros

| Variável | Padrão | Descrição |
|---|---|---|
| `LLM_MODEL` | — | Modelo da LLM |
| `API_KEY` | — | Chave de API (obrigatória) |
| `USER_ID` | `default` | Identificador do usuário para memória |
| `SKILLS_DIR` | `./exemplo_skills/` | Diretório de skills `.md` |
| `CONTEXT_SIZE` | vazio (ilimitado) | Janela de mensagens no contexto |
| `DEBUG` | vazio (desligado) | `true`/`1`/`sim` para ativar |

---

## Comportamento por omissão

Se o `.env` não existir ou estiver vazio:

- `main.py` tenta carregar, silencia se não achar (`FileNotFoundError` ignorado)
- Skills não são carregadas (diretório padrão não existe → aviso)
- Memória salva histórico completo (`CONTEXT_SIZE` vazio = sem limite)
- Debug desligado

---

## Exemplo mínimo

```env
API_KEY=minha_chave
```

Apenas a chave de API é obrigatória. Todo o resto tem fallback seguro.
