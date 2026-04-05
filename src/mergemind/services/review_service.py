from uuid import uuid4

from mergemind.models.api import RunReviewRequest, RunReviewResponse
from mergemind.models.domain import ReviewComment, ReviewIssue, ReviewReport


class ReviewService:
    async def run_review(self, request: RunReviewRequest) -> RunReviewResponse:
        """
        Run a PR review (v1: mock implementation).
        Later this will call:
        - integrations (GitHub, Jira)
        - retrieval layer
        - agent (PydanticAI)
        - graph (Pydantic Graph)
        """

        report = ReviewReport(
            pr_summary=(
                f"PR {request.pr_number or 'from URL'} updates repository "
                f"'{request.repo}'."
            ),
            pbi_summary=(
                f"Linked to PBI '{request.pbi_id}'." if request.pbi_id else None
            ),
            alignment_score=0.78,
            covered_acceptance_criteria=[
                "Core functionality implemented",
                "Feature aligns with PBI scope",
            ],
            missing_acceptance_criteria=[
                "Edge cases not fully covered",
                "Error handling not explicitly tested",
            ],
            risks=[
                ReviewIssue(
                    severity="medium",
                    category="testing",
                    title="Insufficient test coverage",
                    description="Critical paths lack automated tests.",
                    file_path="tests/",
                    line=None,
                )
            ],
            missing_tests=[
                "Test invalid inputs",
                "Test failure scenarios",
            ],
            suggested_comments=[
                ReviewComment(
                    file_path="src/example.py",
                    line=10,
                    comment="Add input validation here.",
                )
            ],
            confidence=0.72,
        )

        return RunReviewResponse(
            review_id=f"rev_{uuid4().hex[:8]}",
            status="completed",
            report=report,
        )
