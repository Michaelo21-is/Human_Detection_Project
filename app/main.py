from fastapi import FastAPI
from app.database import engine, Base
from app.Routers.AuthRouter import router as AuthRouter
from app.Routers.LLMRouter import router as LLMRouter
app = FastAPI()

# adding models table if not exist in the postgress
Base.metadata.create_all(bind=engine)

app.include_router(AuthRouter)
app.include_router(LLMRouter)