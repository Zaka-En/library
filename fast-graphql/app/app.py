from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from app.schema import schema
from strawberry.subscriptions import GRAPHQL_WS_PROTOCOL, GRAPHQL_TRANSPORT_WS_PROTOCOL
from app.dependencies import get_context
from app.broadcast import broadcast
from contextlib import asynccontextmanager

origins = [
  "http://localhost:5173",
  "http://localhost:5174",
  "http://127.0.0.1:5173",
  "http://127.0.0.1:5174",
]
# app.add_event_handler("startup", broadcast.connect)
# app.add_event_handler("shutdown", broadcast.disconnec

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

  app.include_router(graphql_app, prefix='/graphql')

  return app

app = create_app()