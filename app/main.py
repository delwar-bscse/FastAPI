from fastapi import FastAPI
from . routers import user, course, auth
from . import models
from . database import engine

# Initialize all tables in database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include all routers
app.include_router(user.router)
app.include_router(course.router)
app.include_router(auth.router)