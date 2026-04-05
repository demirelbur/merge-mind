from dotenv import load_dotenv
from fastapi import FastAPI

from mergemind.api.routes_health import router as health_router
from mergemind.api.routes_reviews import router as reviews_router

load_dotenv()  # Load environment variables from .env file

app = FastAPI(
    title="MergeMind API",
    version="1.0.0",
    description="Agentic PR review system for PBI-aware pull request analysis.",
)

# Include routers
app.include_router(health_router, prefix="/health")
app.include_router(reviews_router)
