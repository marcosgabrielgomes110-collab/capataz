"""
capataz.prompt — Gerador de system prompt ReAct com técnicas avançadas
"""

from .tools import describe_tools, list_tools


REACT_TEMPLATE = """Você é um agente autônomo que resolve tarefas usando tools (ferramentas).

## Formato de resposta

Toda resposta DEVE seguir **estritamente** um destes formatos:

### Para usar uma ferramenta:
```
Thought: [seu raciocínio em português]
Action: [nome exato da tool]
Action Input: {{"param1": "valor1", "param2": "valor2"}}
```

### Para dar a resposta final:
```
Thought: [raciocínio conclusivo]
Final Answer: [resposta completa e direta para o usuário]
```

## Regras obrigatórias
1. O Action Input DEVE ser um JSON válido entre chaves ({{}}), sem exceções.
2. Use EXATAMENTE os nomes das tools como listado abaixo — não invente.
3. Se uma tool retornar erro começando com [ERRO], analise a causa e corrija os parâmetros.
4. Se a ferramenta retornar dados, use-os para responder — nunca alucine resultados.
5. SEMPRE termine com Final Answer quando tiver a informação suficiente.
6. Não repita tools que já foram chamadas a menos que os parâmetros mudem.
7. Não adicione texto fora do formato. Cada resposta DEVE começar com Thought:.
{examples_section}
## Ferramentas disponíveis
{tools}

{extra}"""


FEWSHOT_EXAMPLES = {
    "calc": """Usuário: Quanto é 3.14 * 2.5?
Thought: O usuário quer multiplicar 3.14 por 2.5. Vou usar a tool calc.
Action: calc
Action Input: {"expr": "3.14 * 2.5"}""",

    "clima": """Usuário: Como está o clima em Fortaleza?
Thought: Preciso consultar o clima de Fortaleza usando a tool clima.
Action: clima
Action Input: {"cidade": "Fortaleza"}""",

    "terminal": """Usuário: Quais arquivos .py existem no diretório atual?
Thought: Vou listar os arquivos .py com o comando ls.
Action: terminal
Action Input: {"comando": "ls *.py"}""",
}


def _build_examples() -> str:
    """Gera exemplos few-shot dinâmicos baseados nas tools registradas."""
    available = set(list_tools())
    examples = []
    for tool_name, example in FEWSHOT_EXAMPLES.items():
        if tool_name in available:
            examples.append(example)
    if not examples:
        return ""
    return "\n## Exemplos\n" + "\n\n".join(examples) + "\n"


def build(system: str = "", extra: str = "") -> str:
    """Monta o system prompt com técnicas avançadas de prompting."""
    tools_desc = describe_tools()
    examples = _build_examples()
    base = REACT_TEMPLATE.format(
        tools=tools_desc,
        extra=extra,
        examples_section=examples,
    ).strip()
    if system:
        return f"{system}\n\n{base}"
    return base
