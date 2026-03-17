import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.router import router

origins = ["http://localhost:8000"]


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
    uvicorn.run("auth.app:app", host="0.0.0.0", port=8001, reload=True)


if __name__ == "__main__":
    start()
