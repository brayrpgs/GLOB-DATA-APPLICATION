from fastapi import FastAPI
from os import getenv

# Import routers de cada módulo
from app.routes.issues_routes import router as issue_router
from app.routes.issue_type_routes import router as issue_type_router
from app.routes.proyect_routes import router as project_router
from app.routes.sprint_routes import router as sprint_router
from app.routes.user_project_routes import router as user_project_router
from app.routes.membership_plan_routes import router as membership_plan_router
from app.routes.payment_info_routes import router as payment_info_router
from app.routes.recover_password_routes import router as recover_password_router
from app.routes.user_routes import router as user_router

app = FastAPI(title="GLOB-DATA")

# Ruta raíz
@app.get("/")
def read_root():
    return {"Hello": getenv("PGADMIN_DEFAULT_EMAIL", "No email configured")}

# Incluir todos los routers
app.include_router(issue_router, prefix="/issues", tags=["Issues"])
app.include_router(issue_type_router, prefix="/issue-types", tags=["Issue Types"])
app.include_router(project_router, prefix="/projects", tags=["Projects"])
app.include_router(sprint_router, prefix="/sprints", tags=["Sprints"])
app.include_router(user_project_router, prefix="/user-projects", tags=["User Projects"])
app.include_router(membership_plan_router, prefix="/membership-plans", tags=["Membership Plans"])
app.include_router(payment_info_router, prefix="/payment-info", tags=["Payment Info"])
app.include_router(recover_password_router, prefix="/recover-passwords", tags=["Recover Password"])
app.include_router(user_router, prefix="/users", tags=["Users"])
