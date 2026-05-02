# Exemplos Completos

---

## Exemplo 1: Chat interativo com memória

```python
import capataz as cp
from capataz import Memory

# ─── LLM ───
def llm_fn(messages):
    import requests
    resp = requests.post(
        "https://api.cohere.com/v2/chat",
        headers={"Authorization": "Bearer SUA_CHAVE"},
        json={"model": "command-a-03-2025", "messages": messages},
        timeout=60,
    )
    return resp.json()["message"]["content"][0]["text"]

cp.set_llm(llm_fn)

# ─── Tools ───
@cp.tool("clima", desc="Clima de uma cidade. Parâmetro: cidade (str).")
def clima(args):
    return f"{args.get('cidade')}: 28°C, ensolarado"

@cp.tool("calc", desc="Calcula expressão. Parâmetro: expr (str).")
def calc(args):
    from ast import literal_eval
    try:
        return str(literal_eval(args.get("expr", "0")))
    except:
        return "Erro na expressão"

# ─── Agente ───
cp.agent.create("chat", system="Você é um assistente.", max_turns=5)

# ─── Memória ───
mem = Memory(persist_path="historico.json", context_size=6)

# ─── Loop ───
while True:
    entrada = input("Você: ")
    if entrada == "sair":
        mem.save()
        break
    resposta = cp.run("chat", entrada, memory=mem)
    print(f"Assistente: {resposta}")
```

---

## Exemplo 2: Skills + Debug

```python
import capataz as cp

# LLM
def llm(messages):
    return "Final Answer: ok"

cp.set_llm(llm)

@cp.tool("ping", desc="Retorna pong.")
def ping(args):
    return "pong"

cp.agent.create("bot", system="Seja breve.", max_turns=2)

# Carrega skills
cp.skills.load("./exemplo_skills/")

# Debug mostra skills ativadas
resultado = cp.run(
    "bot",
    "preciso resumir um texto longo",
    debug=True,
)
```

Saída esperada do debug:
```
[debug] Skills ativadas:
  - resumo_texto (gatilhos: resumir, resumo, ..., prioridade: media)

[capataz | turno 1]
...
```

---

## Exemplo 3: Uso programático (sem input do usuário)

```python
import capataz as cp

def llm(messages):
    return "Final Answer: processado."

cp.set_llm(llm)

@cp.tool("saudacao", desc="Saudação. Parâmetro: nome (str).")
def saudacao(args):
    nome = args.get("nome", "mundo")
    return f"Olá, {nome}!"

cp.agent.create("bot", system="Sempre use a tool saudacao primeiro.")

# Execução programática
respostas = []
for nome in ["Ana", "João", "Maria"]:
    resp = cp.run("bot", f"fala com {nome}")
    respostas.append(resp)

print(respostas)
```

---

## Exemplo 4: Duas LLMs diferentes sem conflito

```python
import capataz as cp

def llm_a(messages):
    return "Final Answer: resposta da LLM A"

def llm_b(messages):
    return "Final Answer: resposta da LLM B"

cp.set_llm(llm_a)  # LLM padrão

@cp.tool("eco", desc="Retorna o texto enviado.")
def eco(args):
    return args.get("texto", "")

cp.agent.create("padrao", system="Use a tool eco.")
cp.agent.create("especial", system="Seja criativo.")

# Usa a LLM global (llm_a)
r1 = cp.run("padrao", "teste")

# Usa llm_b escopada (não altera o global)
r2 = cp.run("especial", "teste", llm_fn=llm_b)

# Continua usando llm_a (não vazou)
r3 = cp.run("padrao", "outro teste")
```

---

## Exemplo 5: API via FastAPI

```python
from fastapi import FastAPI
from pydantic import BaseModel
import capataz as cp
from capataz import Memory

app = FastAPI()

def llm(messages):
    ...
cp.set_llm(llm)
cp.agent.create("api", system="Assistente de API.")

# Memória por sessão (exemplo simplificado)
memorias: dict[str, Memory] = {}

class ChatRequest(BaseModel):
    user_id: str
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    if req.user_id not in memorias:
        memorias[req.user_id] = Memory(context_size=6)

    resp = cp.run("api", req.message, memory=memorias[req.user_id])
    return {"resposta": resp}
```
