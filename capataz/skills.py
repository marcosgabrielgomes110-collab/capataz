"""
capataz.skills — Sistema de skills injetáveis no system prompt
"""
import os
import re
import warnings
from dataclasses import dataclass


@dataclass
class Skill:
    name: str
    gatilhos: list[str]
    body: str
    prioridade: str = "media"


_skills: dict[str, Skill] = {}
_match_mode: str = "keyword"
_llm_fn = None


def set_llm(fn):
    global _llm_fn
    _llm_fn = fn


def parse(md_content: str) -> Skill:
    """
    Extrai name + gatilhos + body + prioridade de um .md de skill.
    """
    header_pattern = re.compile(
        r"skill name:\s*(.+?)[\r\n]+"
        r"gatilhos:\s*(.+?)[\r\n]+"
        r"(?:prioridade:\s*(.+?)[\r\n]+)?"
        r"(?:[\r\n]+(.*))?",
        re.DOTALL | re.IGNORECASE,
    )
    match = header_pattern.match(md_content.strip())
    if not match:
        raise ValueError("Formato inválido de skill. Esperado: skill name, gatilhos")

    name = match.group(1).strip().lower()
    gatilhos_raw = match.group(2).strip()
    prioridade_raw = match.group(3)
    body = match.group(4) or ""

    gatilhos = [g.strip().lower() for g in gatilhos_raw.split(",") if g.strip()]
    prioridade = prioridade_raw.strip().lower() if prioridade_raw else "media"

    if prioridade not in ("alta", "media", "baixa"):
        prioridade = "media"

    body = body.strip()

    return Skill(
        name=name,
        gatilhos=gatilhos,
        body=body,
        prioridade=prioridade,
    )


def load(path: str, match_mode: str = "keyword"):
    """
    Lê todos os .md da pasta e popula o registro de skills.
    """
    global _match_mode
    if match_mode not in ("keyword", "llm"):
        raise ValueError(f"match_mode inválido: '{match_mode}'. Use 'keyword' ou 'llm'.")
    _match_mode = match_mode

    if not os.path.isdir(path):
        raise NotADirectoryError(f"'{path}' não é um diretório válido.")

    _skills.clear()

    for filename in sorted(os.listdir(path)):
        if not filename.endswith(".md"):
            continue
        filepath = os.path.join(path, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            skill = parse(content)
            _skills[skill.name] = skill
        except (ValueError, OSError) as e:
            warnings.warn(f"Skill '{filename}' ignorada: {e}")


def _match_keyword(user_input: str) -> list[Skill]:
    """
    Matching simples: verifica se alguma palavra gatilho aparece no input.
    """
    input_lower = user_input.lower()
    matched: list[Skill] = []
    for skill in _skills.values():
        for gatilho in skill.gatilhos:
            if gatilho in input_lower:
                matched.append(skill)
                break
    return matched


def _match_llm(user_input: str) -> list[Skill]:
    """
    Matching via LLM: pergunta ao modelo quais skills são relevantes.
    """
    if _llm_fn is None:
        raise RuntimeError(
            "match_mode='llm' requer uma LLM definida via skills.set_llm(fn)"
        )

    if not _skills:
        return []

    skills_desc = "\n".join(
        f"- {s.name}: gatilhos={s.gatilhos}" for s in _skills.values()
    )

    prompt = f"""Dado o input do usuário abaixo, determine quais skills (se alguma) são relevantes.

Skills disponíveis:
{skills_desc}

Input: "{user_input}"

Responda APENAS com os nomes das skills relevantes separados por vírgula, ou "nenhuma" se nenhuma for relevante."""

    response = _llm_fn([{"role": "user", "content": prompt}])
    if not isinstance(response, str):
        response = str(response or "")
    response = response.strip().lower()

    if response == "nenhuma":
        return []

    matched = []
    for part in response.split(","):
        name = part.strip()
        if name in _skills:
            matched.append(_skills[name])
    return matched


def match(user_input: str) -> list[Skill]:
    if not user_input:
        return []
    if _match_mode == "llm":
        return _match_llm(user_input)
    return _match_keyword(user_input)


_PRIORIDADE_ORDER = {"alta": 0, "media": 1, "baixa": 2}


def inject(system_prompt: str, user_input: str) -> str:
    """
    Adiciona skills ativadas ao final do system prompt.
    """
    matched = match(user_input)

    if not matched:
        return system_prompt

    matched.sort(key=lambda s: _PRIORIDADE_ORDER.get(s.prioridade, 1))

    blocks = []
    for skill in matched:
        blocks.append(f"## {skill.name}\n{skill.body}")

    skills_section = (
        "\n\n--- SKILLS ATIVAS ---\n" + "\n\n".join(blocks) + "\n---------------------"
    )

    return system_prompt + skills_section


def list_all() -> list[str]:
    return list(_skills.keys())
