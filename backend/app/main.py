"""FastAPI application factory and configuration."""
from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.db import init_db
from app.api import auth_routes, transaction_routes, insights_routes
from app.api import budget_routes, ai_routes

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Run startup tasks without relying on deprecated event hooks."""
    if settings.INIT_DB_ON_STARTUP:
        init_db()
    else:
        logger.info("Skipping database initialization on startup.")
    yield


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="AI-powered expense tracking and insights API",
        lifespan=lifespan,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_origin_regex=settings.CORS_ORIGIN_REGEX,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check endpoint
    @app.get("/")
    def health_check():
        return {
            "message": f"{settings.APP_NAME} is running",
            "version": settings.APP_VERSION
        }

    # Include API routers
    app.include_router(auth_routes.router)
    app.include_router(transaction_routes.router)
    app.include_router(insights_routes.router)
    app.include_router(budget_routes.router)
    app.include_router(ai_routes.router)

    return app


# Create application instance
app = create_app()
