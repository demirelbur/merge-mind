from uuid import uuid4

from mergemind.graph.review_graph import BuildPrNode, review_graph
from mergemind.models.api import ReviewTraceItem, RunReviewRequest, RunReviewResponse
from mergemind.models.state import ReviewState


class ReviewService:
    async def run_review(self, request: RunReviewRequest) -> RunReviewResponse:
        state = ReviewState(request=request)

        graph_run_result = await review_graph.run(BuildPrNode(), state=state)
        report = graph_run_result.output

        trace = [
            ReviewTraceItem(
                step="build_pr",
                detail=state.pr.title if state.pr is not None else "PR not built",
            ),
            ReviewTraceItem(
                step="resolve_pbi",
                detail=state.pbi.id if state.pbi is not None else "No PBI resolved",
            ),
            ReviewTraceItem(
                step="retrieve_context",
                detail=f"Retrieved {len(state.retrieved_chunks)} supporting chunks",
            ),
            ReviewTraceItem(
                step="assemble_packet",
                detail="Review packet assembled"
                if state.packet is not None
                else "Review packet missing",
            ),
            ReviewTraceItem(
                step="run_review",
                detail="Review report generated"
                if state.report is not None
                else "Review report missing",
            ),
            ReviewTraceItem(
                step="validate_and_repair",
                detail=(
                    f"Warnings: {len(state.warnings)}, "
                    f"repair attempts: {state.repair_attempts}"
                ),
            ),
        ]

        return RunReviewResponse(
            review_id=f"rev_{uuid4().hex[:8]}",
            status="completed",
            report=report,
            warnings=state.warnings,
            repair_attempts=state.repair_attempts,
            trace=trace,
        )
