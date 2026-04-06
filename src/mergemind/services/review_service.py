from uuid import uuid4

from mergemind.graph.review_graph import BuildPrNode, review_graph
from mergemind.models.api import RunReviewRequest, RunReviewResponse
from mergemind.models.state import ReviewState


class ReviewService:
    async def run_review(self, request: RunReviewRequest) -> RunReviewResponse:
        state = ReviewState(request=request)

        graph_run_result = await review_graph.run(BuildPrNode(), state=state)
        report = graph_run_result.output

        print(f"Generated review report: {report}")

        return RunReviewResponse(
            review_id=f"rev_{uuid4().hex[:8]}",
            status="completed",
            report=report,
            warnings=state.warnings,
        )
