from contextlib import asynccontextmanager
from typing import Annotated

import strawberry
import uvicorn
from fastapi import Depends, FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from strawberry.subscriptions import GRAPHQL_TRANSPORT_WS_PROTOCOL, GRAPHQL_WS_PROTOCOL

from app.broadcast import broadcast
from app.dependencies import get_context, verify_user
from app.models.user import (
    LoginResponse,
    LogoutRequest,
    LogoutResponse,
    User,
    UserPayload,
)
from app.schema.mutations import Mutation

# Initialize the schema with queries, mutations, and subscriptions
from app.schema.queries import Query
from app.schema.subscriptions import Subscription
from app.services.auth_service import AuthService

schema = strawberry.Schema(mutation=Mutation, query=Query, subscription=Subscription)

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://localhost:3000",
    "http://frontend:3000",
    "http://frontend.localhost",
    "https://frontend:3000",
    "https://frontend.localhost",
    "https://frontend.ezaka.es",
    "http://frontend.ezaka.es",
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broadcast.connect()
    yield
    await broadcast.disconnect()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    graphql_app = GraphQLRouter(
        schema,
        subscription_protocols=[GRAPHQL_WS_PROTOCOL, GRAPHQL_TRANSPORT_WS_PROTOCOL],
        context_getter=get_context,
    )

    @app.post("/login", response_model=LoginResponse)
    async def login(user: Annotated[User, Depends(verify_user)]):

        user_payload = UserPayload(
            id=user.id, name=user.name, email=user.email, rol=user.rol
        )

        access_token, refresh_token = await AuthService.get_tokens(
            user_payload=user_payload
        )

        return LoginResponse(access_token=access_token, refresh_token=refresh_token)

    @app.post("/refresh", response_model=LoginResponse)
    async def refresh(response: Response, request: Request):

        access_token, message = await AuthService.refresh_token(
            request.cookies.get("refresh_token", "")
        )

        response.set_cookie("access_token", access_token)

        return LoginResponse(
            access_token=access_token,
            refresh_token=request.cookies.get("refresh_token", ""),
        )

    @app.post("/logout", response_model=LogoutResponse)
    async def logout(params: LogoutRequest):
        success = await AuthService.revoke_token(token=params.token)

        return LogoutResponse(success=success, user_id=params.user_id)

    @app.middleware("http")
    async def debug_500(request: Request, call_next):
        print(f"Request headers : {request.headers}")
        response = await call_next(request)
        print(f"Response headers : {response.headers}")
        return response

    app.include_router(graphql_app, prefix="/graphql")

    return app


app = create_app()


def start():
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


if "__name__" == "__main__":
    start()
