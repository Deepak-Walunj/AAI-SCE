from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from contextlib import asynccontextmanager
from app.core.logging import setup_logging, get_logger
from app.core.database import database
from app.api.deps import initialize_dependencies
from app.core.exceptions import AppException
from app.core.handlers import app_exception_handler, validation_exception_handler, generic_exception_handler
from app.core.config import settings
import uuid
import structlog
from app.api.auth.router import router as auth_router
from app.api.candidate.router import router as candidate_router
from app.api.admin.router import router as admin_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging()
    logger = get_logger(__name__)
    
    try:
        # Connect to database and ensure it's healthy
        await database.connect()
        logger.info("Database connection established and healthy")
        
        # Initialize all dependencies
        await initialize_dependencies()
        logger.info("Dependencies initialized successfully")
        
        yield
        
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        raise
    
    # Shutdown
    database.disconnect()
    logger.info("Application shutdown complete")

app = FastAPI(
    title="AAI Project Backend",
    description="Backend API for AAI Project",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the AAI Project Backend API!",
        "available_routes": [
            f"{settings.API_PREFIX}/auth",
            f"{settings.API_PREFIX}/candidate",
            f"{settings.API_PREFIX}/admin",
            "/health"
        ]
    }

# Register exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request ID middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=request_id)
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

# API routes
app.include_router(auth_router, prefix=f"{settings.API_PREFIX}/auth", tags=["auth"])
app.include_router(candidate_router, prefix=f"{settings.API_PREFIX}", tags=["candidate"])
app.include_router(admin_router, prefix=f"{settings.API_PREFIX}", tags=["admin"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
