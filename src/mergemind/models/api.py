from pydantic import BaseModel, Field, HttpUrl, model_validator

from mergemind.models.domain import ReviewReport


class RunReviewRequest(BaseModel):
    repo: str = Field(
        ...,
        description="Repository identifier, for example 'owner/repo'",
        examples=["openai/example-repo"],
    )
    pr_number: int | None = Field(
        default=None,
        description="Pull request number if provided directly",
        ge=1,
        examples=[42],
    )
    pr_url: HttpUrl | None = Field(
        default=None,
        description="Full pull request URL as an alternative to pr_number",
        examples=["https://github.com/openai/example-repo/pull/42"],
    )
    pbi_id: str | None = Field(
        default=None,
        description="Optional identifier for the associated Product Backlog Item (PBI)",
        examples=["PBI-123"],
    )

    @model_validator(mode="after")
    def validate_pr_reference(self) -> "RunReviewRequest":
        if self.pr_number is None and self.pr_url is None:
            raise ValueError("Either pr_number or pr_url must be provided")
        if self.pr_number is not None and self.pr_url is not None:
            raise ValueError("Only one of pr_number or pr_url should be provided")
        return self

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "repo": "openai/example-repo",
                    "pr_number": 42,
                    "pbi_id": "PBI-123",
                },
                {
                    "repo": "openai/example-repo",
                    "pr_url": "https://github.com/openai/example-repo/pull/42",
                },
            ]
        }
    }


class ReviewTraceItem(BaseModel):
    step: str = Field(..., description="Description of the workflow step")
    detail: str = Field(..., description="Human-readable details about the step")


class RunReviewResponse(BaseModel):
    review_id: str = Field(
        ...,
        description="Unique identifier for the review process",
        examples=["rev_001"],
    )
    status: str = Field(
        ...,
        description="Status of the review run",
        examples=["pending", "completed"],
    )
    report: ReviewReport = Field(..., description="Structured review report")
    warnings: list[str] = Field(
        default_factory=list,
        description="Non-fatal warnings produced during workflow validation",
    )
    repair_attempts: int = Field(
        default=0,
        description="Number of repair attempts applied to the generated review report",
    )
    trace: list[ReviewTraceItem] = Field(
        default_factory=list,
        description="Lightweight execution trace for debugging and transparency",
    )


class HealthResponse(BaseModel):
    status: str = Field(..., description="Service health status", examples=["ok"])
