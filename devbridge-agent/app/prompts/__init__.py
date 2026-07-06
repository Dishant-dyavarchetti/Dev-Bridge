import pathlib

PROMPTS_DIR = pathlib.Path(__file__).parent


def load_prompt(agent_name: str, prompt_type: str) -> str:
    """
    Load a prompt file (system, developer, or examples) for a given agent.
    """
    path = PROMPTS_DIR / agent_name / f"{prompt_type}.md"
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return ""


def get_system_instruction(agent_name: str) -> str:
    """
    Combines system prompt, developer guidelines, and few-shot examples
    to construct the full model instructions.
    """
    system_prompt = load_prompt(agent_name, "system")
    developer_prompt = load_prompt(agent_name, "developer")
    examples_prompt = load_prompt(agent_name, "examples")

    parts = []
    if system_prompt:
        parts.append(system_prompt)
    if developer_prompt:
        parts.append(f"## Developer Guidelines\n{developer_prompt}")
    if examples_prompt:
        parts.append(f"## Few-shot Examples\n{examples_prompt}")

    return "\n\n".join(parts)


__all__ = [
    "load_prompt",
    "get_system_instruction",
]
