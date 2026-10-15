from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, submissions, admin

# Create database tables automatically for development
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Interntrack RBAC Backend",
    description="Role-Based Access Control and Ownership Rules Assignment",
    version="1.0.0"
)

# Include routers
app.include_router(auth.router)
app.include_router(submissions.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Interntrack RBAC Backend API!"}

