from fastapi import APIRouter

from mergemind.models.api import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/", response_model=HealthResponse, summary="Check API health")
async def health() -> HealthResponse:
    return HealthResponse(status="ok")
