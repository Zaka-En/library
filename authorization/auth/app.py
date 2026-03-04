from fastapi import FastAPI
from .api.router import router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

origins = [
  "http://localhost:8000"
]

def create_app() -> FastAPI:
  app = FastAPI()

  app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
  )

  app.include_router(router, prefix="/oauth")

  return app

app = create_app()

def start():
  uvicorn.run("auth.app:app", host="127.0.0.1" , port=8001, reload=True)


