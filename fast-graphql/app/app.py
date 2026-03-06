from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from app.schema import schema
from strawberry.subscriptions import GRAPHQL_WS_PROTOCOL, GRAPHQL_TRANSPORT_WS_PROTOCOL
from app.dependencies import get_context, verify_user
from app.broadcast import broadcast
from contextlib import asynccontextmanager
from typing import Annotated
from app.models.user import User, UserPayload, LoginResponse, LogoutResponse, LogoutRequest
from app.services.auth_service import AuthService

import uvicorn

origins = [
  "http://localhost:5173",
  "http://localhost:5174",
  "http://127.0.0.1:5173",
  "http://127.0.0.1:5174",
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
      id=user.id,
      name=user.name,
      email=user.email,
      rol=user.rol
    )

    access_token, refresh_token = await AuthService.get_tokens(user_payload=user_payload)

    return LoginResponse(
      access_token=access_token,
      refresh_token=refresh_token
    )

  @app.post("/logout", response_model=LogoutResponse)
  async def logout(params: LogoutRequest) :
    success = await AuthService.revoke_token(token=params.token)

    return LogoutResponse(
      success=success,
      user_id=params.user_id
    )

    
  app.include_router(graphql_app, prefix='/graphql')


  return app

app = create_app()

def start():
  uvicorn.run(app, host="127.0.0.1" , port=8001, reload=True)
