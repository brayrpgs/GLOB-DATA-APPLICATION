from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes.issues_routes import router as issue_router
from app.routes.issue_type import router as issue_type
from app.routes.sprint_routes import router as sprint
from app.routes.project_routes import router as proyect
from app.routes.user_project_routes import router as proyect_routes


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

# Mount routers
app.include_router(issue_router)
app.include_router(issue_type)
app.include_router(sprint)
app.include_router(proyect)
app.include_router(proyect_routes)