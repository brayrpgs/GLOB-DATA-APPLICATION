from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
from app.routes.membership_routes import router as membership_routes
from app.routes.issues_routes import router as issue_router
from app.routes.issue_type import router as issue_type
from app.routes.sprint_routes import router as sprint
from app.routes.project_routes import router as proyect
from app.routes.user_project_routes import router as proyect_routes


from app.middlewares.RequestValidationMiddleware import request_validation_middleware

from app.database.conection import init_pool, close_pool

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code that runs on startup
    await init_pool()
    try:
        yield
    finally:
        # Ensure the DB pool is closed on shutdown
        await close_pool()

app = FastAPI(title="GLOB-DATA-APPLICATION", lifespan=lifespan)


def custom_openapi():
    """Attach a Bearer auth schema to the generated OpenAPI so Swagger UI
    shows the "Authorize" button and can send an Authorization: Bearer <JWT>
    header on requests.
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        routes=app.routes,
    )
    components = openapi_schema.setdefault("components", {})
    security_schemes = components.setdefault("securitySchemes", {})
    security_schemes["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "Enter: **Bearer <JWT>**",
    }
    openapi_schema.setdefault("security", [{"BearerAuth": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Override the default OpenAPI generator so Swagger UI supports Bearer JWT
app.openapi = custom_openapi

# Add middleware
app.middleware("http")(request_validation_middleware)

# Mount routers
app.include_router(issue_router)
app.include_router(issue_type)
app.include_router(sprint)
app.include_router(proyect)
app.include_router(proyect_routes)
app.include_router(membership_routes)