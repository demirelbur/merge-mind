from pydantic import BaseModel, Field

from mergemind.models.api import RunReviewRequest
from mergemind.models.domain import PBI, PullRequest, ReviewReport
from mergemind.models.review_packet import RetrievedChunk, ReviewPacket


class ReviewState(BaseModel):
    request: RunReviewRequest = Field(
        ..., description="Incoming API request for running a review"
    )
    pr: PullRequest | None = Field(
        default=None,
        description="Pull request data resolved for the review",
    )
    pbi: PBI | None = Field(
        default=None,
        description="Resolved Product Backlog Item, if available",
    )
    retrieved_chunks: list[RetrievedChunk] = Field(
        default_factory=list,
        description="Retrieved supporting evidence",
    )
    packet: ReviewPacket | None = Field(
        default=None,
        description="Structured review packet built from PR, PBI, and retrieved context",
    )
    report: ReviewReport | None = Field(
        default=None,
        description="Final structured review report produced by the agent",
    )
    errors: list[str] = Field(
        default_factory=list,
        description="Collected workflow errors encountered during the review process",
    )
    warnings: list[str] = Field(
        default_factory=list,
        description="Non-fatal validation warnings about the generated review report",
    )
    repair_attempts: int = Field(
        default=0,
        description="Number of repair attempts applied to the generated review report",
    )
