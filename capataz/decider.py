"""
capataz.decider — Loop ReAct robusto: Thought → Action → Observation → Final Answer
"""

import re
import json
from .tools import call as tool_call

_llm_fn = None


def set_llm(fn):
    global _llm_fn
    _llm_fn = fn


def _extract_action_args(snippet: str) -> dict:
    """
    Extrai argumentos de uma string (JSON ou key=value).
    """
    if not snippet:
        return {}

    # 1. Tenta JSON decoder (lida com nested objects, strings escapadas, etc.)
    try:
        obj, _end = json.JSONDecoder().raw_decode(snippet)
        if isinstance(obj, dict):
            return obj
    except json.JSONDecodeError:
        pass

    # 2. Tenta extrair JSON com regex (nível único de aninhamento)
    json_match = re.search(r"\{.*?\}", snippet, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass

    # 3. Fallback: key=value simples
    kv = {}
    for part in re.findall(r'(\w[\w-]*)\s*[=:]\s*"([^"]*)"', snippet):
        kv[part[0]] = part[1]
    for part in re.findall(r'(\w[\w-]*)\s*[=:]\s*"([^"]*)"', snippet):
        pass  # valores aspeados já capturados acima

    for part in re.findall(r'(\w[\w-]*)\s*[=:]\s*(\S+)', snippet):
        key, val = part
        val = val.strip('"').strip("'")
        if key not in kv:
            kv[key] = val

    return kv


def _check_final_answer(response: str) -> str | None:
    """Extrai Final Answer da resposta ou retorna None."""
    match = re.search(r"Final Answer:\s*(.*)", response, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def _parse_actions(text: str) -> list[tuple[str, dict]]:
    """
    Extrai múltiplos blocos Action/Action Input de uma resposta.
    Exemplo:
        Action: clima
        Action Input: {"cidade": "Fortaleza"}
        Action: calc
        Action Input: {"expr": "2+2"}
    Retorna: [("clima", {"cidade": "Fortaleza"}), ("calc", {"expr": "2+2"})]
    """
    actions = []
    pattern = re.compile(r"Action:\s*(\S+).*?Action Input:\s*", re.DOTALL | re.IGNORECASE)
    for match in pattern.finditer(text):
        name = match.group(1).strip()
        snippet = text[match.end():].strip()
        args = _extract_action_args(snippet)
        actions.append((name, args))
    return actions


def run_loop(
    messages: list[dict],
    system_prompt: str,
    max_turns: int = 5,
    verbose: bool = False,
    llm_fn=None,
) -> str:
    """
    Executa o loop ReAct até Final Answer ou max_turns.

    messages: histórico atual (list of dicts com role/content)
    system_prompt: prompt do sistema com tools embutidas
    max_turns: limite de iterações
    verbose: imprime cada turno
    llm_fn: função LLM opcional (sobrescreve global apenas nesta chamada)
    """
    fn = llm_fn or _llm_fn
    if fn is None:
        raise RuntimeError("LLM não definida. Use capataz.set_llm(sua_funcao) ou passe llm_fn.")

    full_messages = [{"role": "system", "content": system_prompt}] + messages
    recent_action_hashes: set[int] = set()
    consecutive_same = 0

    for turn in range(max_turns):
        response = fn(full_messages)

        if not isinstance(response, str):
            response = str(response or "")

        if verbose:
            print(f"\n[capataz | turno {turn + 1}]\n{response}\n")

        # 1. Checa Final Answer primeiro
        final = _check_final_answer(response)
        if final:
            return final

        # 2. Extrai todas as ações da resposta
        actions = _parse_actions(response)

        if actions:
            # Detecta loop: mesma sequência repetida (2x consecutivas) ou alternância (3x vista antes)
            action_hash = hash(tuple(sorted((a, json.dumps(k, sort_keys=True)) for a, k in actions)))
            if action_hash in recent_action_hashes:
                consecutive_same += 1
            else:
                consecutive_same = 0

            if consecutive_same >= 2:
                if verbose:
                    print("[capataz] Loop detectado — encerrando.")
                return response.strip()

            recent_action_hashes.add(action_hash)

            # Executa todas as ações e coleta observações
            observations = []
            for action, args in actions:
                result = tool_call(action, args)
                observations.append(f"Observation ({action}): {result}")

                if verbose:
                    print(f"[capataz | tool] {action}({args}) → {result}")

            full_messages.append({"role": "assistant", "content": response})
            full_messages.append({"role": "user", "content": "\n".join(observations)})
        else:
            # Sem Action e sem Final Answer — resposta direta
            return response.strip()

    return "Não consegui completar a tarefa no número máximo de iterações. Tente simplificar sua pergunta."
