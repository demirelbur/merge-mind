from uuid import uuid4

from mergemind.agents.reviewer import run_review_agent
from mergemind.models.api import RunReviewRequest, RunReviewResponse
from mergemind.retrieval.mock_packet_builder import MockPacketBuilder


class ReviewService:
    def __init__(self, packet_builder: MockPacketBuilder | None = None) -> None:
        self.packet_builder = packet_builder or MockPacketBuilder()

    async def run_review(self, request: RunReviewRequest) -> RunReviewResponse:
        packet = self.packet_builder.build(request)
        report = await run_review_agent(packet)

        print(f"Generated review report: {report}")

        return RunReviewResponse(
            review_id=f"rev_{uuid4().hex[:8]}",
            status="completed",
            report=report,
        )
