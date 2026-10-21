import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.config import settings
from app.core.database import Base, engine
from app.utils.seed_data import seed_database

# Import routers
from app.routes.auth import router as auth_router
from app.routes.students import router as students_router
from app.routes.companies import router as companies_router
from app.routes.drives import router as drives_router
from app.routes.experiences import router as experiences_router
from app.routes.analytics import router as analytics_router
from app.routes.admin import router as admin_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Application startup: Initialize tables & check seed data
    Base.metadata.create_all(bind=engine)
    try:
        seed_database()
    except Exception as e:
        print(f"Startup database check/seed notice: {e}")
    yield
    # Application shutdown cleanup (if any)

app = FastAPI(
    title="Placell API",
    description="AI-Powered Student Placement Experience and Career Analytics System (ES + ITPM + ASTMA)",
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development and local network demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers
api_prefix = settings.API_V1_STR
app.include_router(auth_router, prefix=api_prefix)
app.include_router(students_router, prefix=api_prefix)
app.include_router(companies_router, prefix=api_prefix)
app.include_router(drives_router, prefix=api_prefix)
app.include_router(experiences_router, prefix=api_prefix)
app.include_router(analytics_router, prefix=api_prefix)
app.include_router(admin_router, prefix=api_prefix)

@app.get(f"{api_prefix}/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": "2026-10-21T16:00:00Z",
        "modules": {
            "enterprise_systems": "ACTIVE",
            "ai_nlp_pipeline": "ACTIVE",
            "placement_readiness_engine": "ACTIVE",
            "analytics_engine": "ACTIVE"
        }
    }

# Static Frontend SPA serving for production deployment
FRONTEND_DIST = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "frontend",
    "dist"
)

if os.path.exists(FRONTEND_DIST):
    assets_dir = os.path.join(FRONTEND_DIST, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):
        # Allow API routes, Swagger UI, and OpenAPI to pass through normally
        if full_path.startswith("api") or full_path in ("docs", "redoc", "openapi.json"):
            raise HTTPException(status_code=404, detail="Not Found")
        file_path = os.path.join(FRONTEND_DIST, full_path)
        if full_path and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))
else:
    @app.get("/")
    def root():
        return {
            "system": "Placell",
            "description": "AI-Powered Student Placement Experience & Career Analytics System",
            "version": settings.PROJECT_VERSION,
            "docs_url": "/docs",
            "health": "OPERATIONAL"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
