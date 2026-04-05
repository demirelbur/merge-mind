from typing import Literal

from pydantic import BaseModel, Field

from mergemind.models.domain import PBI, PullRequest


class RetrievedChunk(BaseModel):
    source_type: Literal["pbi", "pr", "doc", "code"] = Field(
        ..., description="Type of source, e.g., 'pbi', 'pr', 'doc', 'code'."
    )
    source_id: str = Field(
        ...,
        description="Identifier of the source document or entity",
    )
    path: str | None = Field(
        default=None,
        description="Optional file path associated with the chunk",
    )
    content: str = Field(..., description="Retrieved text content")
    score: float | None = Field(
        default=None, description="Optional retrieval relevance score", ge=0.0, le=1.0
    )
    metadata: dict[str, str] | None = Field(
        default=None,
        description="Optional metadata about the chunk (e.g., author, timestamp)",
    )


class ReviewPacket(BaseModel):
    pr: PullRequest = Field(..., description="Pull request under review")
    pbi: PBI | None = Field(
        default=None, description="Associated Product Backlog Item, if resolved"
    )
    retrieved_chunks: list[RetrievedChunk] = Field(
        default_factory=list,
        description="Supporting evidence retrieved for the review",
    )
