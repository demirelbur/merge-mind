from typing import Literal

from pydantic import BaseModel, Field


class PBI(BaseModel):
    id: str = Field(..., description="Unique identifier for the PBI")
    title: str = Field(..., description="Title of the PBI")
    description: str | None = Field(
        default=None, description="Detailed description of the PBI"
    )
    acceptance_criteria: list[str] = Field(
        default_factory=list, description="Acceptance criteria for the PBI"
    )


class ChangedFile(BaseModel):
    path: str = Field(..., description="Path of the changed file")
    patch: str | None = Field(
        default=None, description="Patch content for the changed file"
    )
    status: Literal["added", "modified", "deleted", "renamed"] = Field(
        ..., description="Status of the changed file"
    )


class PullRequest(BaseModel):
    id: int = Field(..., description="Unique identifier for the pull request")
    title: str = Field(..., description="Title of the pull request")
    body: str | None = Field(
        default=None, description="Detailed description of the pull request"
    )
    branch: str = Field(..., description="Branch name associated with the pull request")
    changed_files: list[ChangedFile] = Field(
        default_factory=list, description="List of changed files in the pull request"
    )


class ReviewIssue(BaseModel):
    severity: Literal["low", "medium", "high"] = Field(
        ..., description="Severity level of the review issue"
    )
    category: Literal[
        "correctness", "testing", "security", "maintainability", "requirements"
    ] = Field(..., description="Category of the review issue")
    title: str = Field(..., description="Title of the review issue")
    description: str = Field(
        ..., description="Detailed description of the review issue"
    )
    file_path: str | None = Field(default=None, description="Path of the related file")
    line: int | None = Field(
        default=None, description="Line number in the related file"
    )


class ReviewComment(BaseModel):
    file_path: str = Field(..., description="Path of the related file")
    line: int | None = Field(
        default=None, description="Line number in the related file"
    )
    comment: str = Field(..., description="Content of the review comment")


class ReviewReport(BaseModel):
    pr_summary: str = Field(..., description="Summary of the pull request")
    pbi_summary: str | None = Field(default=None, description="Summary of the PBI")
    alignment_score: float = Field(
        ..., description="Alignment score between the PR and PBI (0 to 1)", ge=0, le=1
    )
    covered_acceptance_criteria: list[str] = Field(
        default_factory=list,
        description="Acceptance criteria covered by the PR",
    )
    missing_acceptance_criteria: list[str] = Field(
        default_factory=list,
        description="Acceptance criteria not covered by the PR",
    )
    risks: list[ReviewIssue] = Field(
        default_factory=list, description="Identified review issues"
    )
    missing_tests: list[str] = Field(
        default_factory=list,
        description="Missing test cases based on the acceptance criteria",
    )
    suggested_comments: list[ReviewComment] = Field(
        default_factory=list,
        description="Suggested review comments for the PR",
    )
    confidence: float = Field(
        ..., description="Confidence level of the review report (0 to 1)", ge=0, le=1
    )
