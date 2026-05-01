from fastapi import FastAPI
from app.database import engine, Base
from app.Routers.AuthRouter import router as AuthRouter

app = FastAPI()

# adding models table if not exist in the postgress
Base.metadata.create_all(bind=engine)

app.include_router(AuthRouter)