from fastapi import APIRouter, status

from mergemind.models.api import RunReviewRequest, RunReviewResponse
from mergemind.services.review_service import ReviewService

router = APIRouter(prefix="/reviews", tags=["reviews"])

service = ReviewService()


@router.post(
    "/run",
    response_model=RunReviewResponse,
    status_code=status.HTTP_200_OK,
    summary="Run a PR review",
    description="Run a mock PR review and return a structured review report.",
)
async def run_review(request: RunReviewRequest) -> RunReviewResponse:
    return await service.run_review(request)
