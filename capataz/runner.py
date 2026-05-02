"""
capataz.runner — Interface principal: run(agent, input, llm_fn?)
"""

from . import agent as agent_module
from . import decider
from . import prompt as prompt_module
from . import skills as skills_module
from .memory import Memory


def run(
    agent_name: str,
    user_input: str,
    llm_fn=None,
    memory: Memory = None,
    context_size: int = None,
    debug: bool = False,
) -> str:
    """
    Executa um agente.

    agent_name: nome do agente criado com capataz.agent.create()
    user_input: mensagem do usuário
    llm_fn: função LLM (sobrescreve o global apenas nesta chamada)
    memory: objeto Memory opcional para histórico entre chamadas
    context_size: limita o número de mensagens do histórico enviadas à LLM
    debug: mostra skills ativadas e execução detalhada das tools
    """
    # Pega config do agente
    ag = agent_module.get(agent_name)

    # Monta memory se não passada
    if memory is None:
        memory = Memory()

    # context_size passado por parâmetro sobrescreve o da Memory
    if context_size is not None:
        memory.context_size = context_size

    # Adiciona input do usuário
    memory.add("user", user_input)

    # Monta system prompt com tools
    system = prompt_module.build(system=ag.get("system", ""))

    # Injeta skills ativadas no system prompt
    system = skills_module.inject(system, user_input)

    if debug:
        matched = skills_module.match(user_input)
        if matched:
            print("[debug] Skills ativadas:")
            for s in matched:
                print(f"  - {s.name} (gatilhos: {', '.join(s.gatilhos)}, prioridade: {s.prioridade})")
        else:
            print("[debug] Nenhuma skill ativada")

    # Roda o loop (llm_fn é escopada, não altera o global)
    verbose = ag.get("verbose", False) or debug
    result = decider.run_loop(
        messages=memory.get(),
        system_prompt=system,
        max_turns=ag.get("max_turns", 5),
        verbose=verbose,
        llm_fn=llm_fn,
    )

    # Salva resposta na memória
    memory.add("assistant", result)

    return result
