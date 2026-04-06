import json

from pydantic_ai import Agent

from mergemind.models.domain import ReviewReport

repair_agent = Agent(
    "openrouter:openai/gpt-4o",
    name="review_report_repair_agent",
    description="Repairs inconsistent fields in a generated review report.",
    output_type=ReviewReport,
    defer_model_check=True,
    system_prompt=(
        "You are a review report repair agent.\n\n"
        "You will receive:\n"
        "- a previously generated review report\n"
        "- a list of validation warnings\n\n"
        "Your task is to repair only the inconsistent parts of the report.\n\n"
        "Rules:\n"
        "1. Keep the report as close as possible to the original.\n"
        "2. Only change fields necessary to address the warnings.\n"
        "3. Do not invent new risks, tests, comments, or acceptance criteria unless required.\n"
        "4. If missing_acceptance_criteria is non-empty, alignment_score must be less than 1.0.\n"
        "5. Preserve grounded, existing content whenever possible.\n"
        "6. If a requirement is described elsewhere in the report as implemented, do not keep it in missing_acceptance_criteria.\n"
        "7. If the real gap is missing tests, keep that as a testing issue rather than a missing requirement.\n"
    ),
)


async def run_repair_agent(
    report: ReviewReport,
    warnings: list[str],
) -> ReviewReport:
    payload = {
        "report": report.model_dump(mode="json"),
        "warnings": warnings,
    }

    result = await repair_agent.run(json.dumps(payload, indent=2, ensure_ascii=False))
    return result.output
