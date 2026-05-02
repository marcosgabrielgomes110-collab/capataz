# `skills` — Sistema de Skills

Skills são instruções injetadas no system prompt quando a LLM detecta que são relevantes. Cada skill é um arquivo `.md` simples.

---

## Visão geral

```
exemplo_skills/
├── busca_web.md
├── resumo_texto.md
└── modo_dev.md
      ↓
  cp.skills.load("./exemplo_skills/")
      ↓
  usuário diz "pesquisar algo"
      ↓
  skill ativada → injetada no system prompt do agente
```

---

## `load(path, match_mode="keyword")`

Carrega todos os `.md` de uma pasta.

```python
import capataz as cp

cp.skills.load("./exemplo_skills/")
# → skills carregadas: ["busca_web", "modo_dev", "resumo_texto"]

# Modo LLM (mais preciso, custa tokens)
cp.skills.load("./exemplo_skills/", match_mode="llm")
# Requer skills.set_llm(fn) configurada
```

| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| `path` | `str` | — | Diretório com arquivos `.md` |
| `match_mode` | `str` | `"keyword"` | `"keyword"` (rápido) ou `"llm"` (preciso) |

**Exceções:** `NotADirectoryError` se path não existe.

---

## `parse(md_content)`

Parseia um conteúdo `.md` para objeto `Skill`.

```python
from capataz.skills import parse

skill = parse("""skill name: busca_web
gatilhos: buscar, pesquisar
prioridade: alta

# Busca na Web
Instruções para busca...
""")
# → skill.name == "busca_web"
# → skill.gatilhos == ["buscar", "pesquisar"]
# → skill.body == "# Busca na Web\nInstruções..."
```

---

## `match(user_input)`

Retorna as skills ativadas para um input.

```python
skills = cp.skills.match("me ajuda a pesquisar sobre Python")
# → [Skill(name="busca_web", ...)]

skills = cp.skills.match("bom dia")
# → [] (nenhuma skill relevante)
```

---

## `inject(system_prompt, user_input)`

Adiciona skills ativadas ao final do system prompt.

```python
prompt = "System prompt original."
prompt = cp.skills.inject(prompt, "preciso resumir um texto")
# → "System prompt original.\n\n--- SKILLS ATIVAS ---\n## resumo_texto\n..."
```

---

## `list_all()`

Lista todas as skills carregadas.

```python
cp.skills.list_all()
# → ["busca_web", "modo_dev", "resumo_texto"]
```

---

## Formato do arquivo `.md`

```markdown
skill name: analise_dados
gatilhos: analisar, dados, csv, tabela, gráfico
prioridade: alta

# Análise de Dados

Quando o usuário pedir para analisar dados:
1. Pergunte o formato (CSV, JSON, texto)
2. Identifique padrões relevantes
3. Apresente insights de forma clara
```

Campos obrigatórios: `skill name`, `gatilhos` (separados por vírgula).

Campos opcionais: `prioridade` (`alta`, `media`, `baixa` — usada para ordenação).

---

## Estratégias de matching

### `keyword` (padrão)
- Verifica se **qualquer gatilho** aparece no texto do usuário
- Rápido, zero custo de API
- Exato, não semântico

### `llm`
- Envia uma query para a LLM perguntando quais skills são relevantes
- Preciso semanticamente, mas custa tokens

---

## Integração automática

Quando você chama `cp.run()`, o `runner` já:
1. Chama `skills.match(user_input)`
2. Chama `skills.inject(system, user_input)`
3. Envia o prompt enriquecido para a LLM

Zero configuração extra depois do `load()`.
