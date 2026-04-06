import json

from pydantic_ai import Agent

from mergemind.models.domain import ReviewReport
from mergemind.models.review_packet import ReviewPacket

review_agent = Agent(
    "openrouter:openai/gpt-4o",
    name="code_reviewer_agent",
    description="An agent that reviews pull requests and generates structured review reports.",
    output_type=ReviewReport,
    defer_model_check=True,
    system_prompt=(
        "You are a senior software engineer performing pull request reviews.\n\n"
        "You will receive a structured JSON object containing:\n"
        "- a pull request\n"
        "- an optional product backlog item (PBI)\n"
        "- retrieved supporting context\n\n"
        "Your task is to produce a structured review report.\n\n"
        "Grounding rules:\n"
        "1. Base your reasoning only on the provided data.\n"
        "2. Do not invent requirements, files, tests, risks, or behaviors.\n"
        "3. If evidence is incomplete or ambiguous, lower confidence.\n"
        "4. Prefer empty lists over invented content.\n\n"
        "Assessment rules:\n"
        "5. Keep findings specific, concrete, and actionable.\n"
        "6. alignment_score must reflect actual coverage of acceptance criteria.\n"
        "7. If any acceptance criteria are missing, alignment_score must be less than 1.0.\n"
        "8. Use high confidence only when the evidence is specific and sufficient.\n\n"
        "Requirement interpretation rules:\n"
        "9. Distinguish clearly between missing implementation, missing tests, and coarse-grained implementation.\n"
        "10. Do not mark a requirement as missing if the behavior appears implemented in a combined or generic way.\n"
        "11. If behavior is implemented but lacks specific test coverage, report it as a testing gap rather than a missing requirement.\n"
        "12. Only report a requirements risk when the requirement is not implemented or is clearly incomplete.\n"
        "13. If one conditional check covers multiple required fields together, treat that as implemented validation unless the requirement explicitly demands separate handling.\n"
        "14. If the implementation is generic but functional, you may note lack of granularity as a maintainability or design concern, not as a missing requirement.\n"
    ),
)


def _build_agent_input(packet: ReviewPacket) -> str:
    payload = packet.model_dump(mode="json")
    return (
        "Review the following structured PR context. "
        "Treat combined validationchecks as implemented behaviour unless clearly contradicted by the requirements.\n\n"
        + json.dumps(payload, indent=2, ensure_ascii=False)
    )


async def run_review_agent(packet: ReviewPacket) -> ReviewReport:
    """Run the reviewer agent on a structured ReviewPacket."""
    agent_input = _build_agent_input(packet)
    result = await review_agent.run(agent_input)
    return result.output
