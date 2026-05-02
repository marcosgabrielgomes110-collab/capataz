"""
capataz.__main__ — CLI interativa: python -m capataz

Uso:
    python -m capataz
    capataz                        (se instalado via pip)
"""

import sys
import os
import ast
import operator as op
import subprocess
import shlex

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import capataz as cp
from capataz import Memory


def load_env(path=".env"):
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())
    except FileNotFoundError:
        pass


_SAFE_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}


def _safe_eval(expr: str) -> float:
    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.BinOp):
            return _SAFE_OPS[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp):
            return _SAFE_OPS[type(node.op)](_eval(node.operand))
        raise ValueError(f"Operação não permitida: {type(node).__name__}")
    return _eval(ast.parse(expr, mode="eval"))


def _llm_fn(messages):
    API_KEY = os.getenv("API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL", "")
    if not API_KEY:
        return "Final Answer: API_KEY não configurada. Crie um arquivo .env."
    endpoint = os.getenv("LLM_ENDPOINT", "https://api.cohere.com/v2/chat")
    import requests
    try:
        resp = requests.post(
            endpoint,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json={"model": LLM_MODEL, "messages": messages},
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        text = data.get("message", {}).get("content", [{}])
        if text and isinstance(text, list):
            return text[0].get("text", "")
        return "Final Answer: Desculpe, não consegui processar sua mensagem."
    except Exception as e:
        return f"Final Answer: Erro na API: {e}"


def main():
    load_env()

    API_KEY = os.getenv("API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL", "")
    USER_ID = os.getenv("USER_ID", "default")
    MEMORY_FILE = f"memoria_{USER_ID}.json"
    SKILLS_DIR = os.getenv("SKILLS_DIR", "")
    CONTEXT_SIZE = int(s) if (s := os.getenv("CONTEXT_SIZE")) else None
    DEBUG = os.getenv("DEBUG", "").lower() in ("1", "true", "sim")

    cp.set_llm(_llm_fn)

    @cp.tool("clima", desc="Clima de uma cidade. Parâmetro: cidade (str).")
    def clima(args):
        cidade = args.get("cidade", "desconhecida")
        return f"{cidade}: 28°C, ensolarado"

    @cp.tool("calc", desc="Calcula expressão matemática. Parâmetro: expr (str).")
    def calc(args):
        try:
            return str(_safe_eval(args.get("expr", "0")))
        except Exception as e:
            return f"Erro no cálculo: {e}"

    @cp.tool("terminal", desc="Executa um comando no shell.")
    def terminal(args):
        try:
            cmd = args.get("comando", "")
            if not cmd:
                return "Nenhum comando fornecido."
            result = subprocess.run(
                shlex.split(cmd), capture_output=True, text=True, timeout=15
            )
            return (result.stdout + result.stderr).strip() or "Sem saída."
        except subprocess.TimeoutExpired:
            return "Comando excedeu 15s."
        except Exception as e:
            return f"Erro: {e}"

    if SKILLS_DIR and os.path.isdir(SKILLS_DIR):
        cp.skills.load(SKILLS_DIR)

    if "chat" not in cp.agent.list_all():
        cp.agent.create("chat", system="Você é um assistente pessoal.", max_turns=5)

    mem = Memory(persist_path=MEMORY_FILE, context_size=CONTEXT_SIZE)

    print(f"🤠 capataz")
    print(f"Modelo: {LLM_MODEL or 'não configurado'}")
    print(f"Memória: {MEMORY_FILE}")
    if cp.skills.list_all():
        print(f"Skills: {cp.skills.list_all()}")
    print()

    while True:
        try:
            entrada = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            mem.save()
            break
        if not entrada:
            continue
        if entrada.lower() == "sair":
            mem.save()
            print("Memória salva. Até mais!")
            break
        if entrada.lower() == "limpar":
            mem.clear()
            print("Memória limpa!")
            continue
        try:
            resposta = cp.run("chat", entrada, memory=mem, debug=DEBUG)
            print(f"Assistente: {resposta}\n")
            mem.save()
        except Exception as e:
            print(f"[ERRO] {e}\n")


if __name__ == "__main__":
    main()
