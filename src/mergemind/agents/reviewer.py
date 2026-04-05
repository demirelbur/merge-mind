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
        "Rules:\n"
        "1. Base your reasoning only on the provided data.\n"
        "2. Do not invent requirements, files, tests, or risks.\n"
        "3. If evidence is incomplete, lower confidence.\n"
        "4. Keep findings specific and actionable.\n"
        "5. Prefer empty lists over invented content.\n"
        "6. alignment_score must reflect actual coverage of acceptance criteria.\n"
        "7. If any acceptance criteria are missing, alignment_score must be less than 1.0.\n"
        "8. Use high confidence only when the evidence is specific and sufficient.\n"
        "9. Do not mark a requirement as missing if the behavior appears implemented but insufficiently tested.\n"
        "10. Distinguish clearly between missing implementation, missing tests, and coarse-grained implementation.\n"
        "11. Only report a requirements risk when the requirement is not implemented or is clearly incomplete.\n"
    ),
)


def _build_agent_input(packet: ReviewPacket) -> str:
    payload = packet.model_dump(mode="json")
    return json.dumps(payload, indent=2, ensure_ascii=False)


async def run_review_agent(packet: ReviewPacket) -> ReviewReport:
    """Run the reviewer agent on a structured ReviewPacket."""
    agent_input = _build_agent_input(packet)
    result = await review_agent.run(agent_input)
    return result.output
