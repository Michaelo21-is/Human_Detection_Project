from fastapi import FastAPI
from app.database import engine, Base
from app.Routers.AuthRouter import router as AuthRouter
from app.Routers.LLMRouter import router as LLMRouter
from app.Routers.VoiceRouter import router as VoiceRouter
from app.Routers.UserRouter import router as UserRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://michael-site.com",
        "https://www.michael-site.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# adding models table if not exist in the postgress
Base.metadata.create_all(bind=engine)

app.include_router(AuthRouter)
app.include_router(LLMRouter)
app.include_router(VoiceRouter)
app.include_router(UserRouter)
