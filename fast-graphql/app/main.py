from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from app.schema import schema
from app.database import  SessionLocal
import uvicorn
from strawberry.subscriptions import GRAPHQL_WS_PROTOCOL, GRAPHQL_TRANSPORT_WS_PROTOCOL
from app.schema.types import broadcast


async def get_context():
  return {"db_factory": SessionLocal}

app = FastAPI()

# Configurar CORS
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

graphql_app = GraphQLRouter(
  schema,
  subscription_protocols=[GRAPHQL_WS_PROTOCOL, GRAPHQL_TRANSPORT_WS_PROTOCOL],
  context_getter=get_context
)

app.include_router(graphql_app, prefix='/graphql')
app.add_event_handler("startup", broadcast.connect)
app.add_event_handler("shutdown", broadcast.disconnect)


if __name__ == "__main__":
  #uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
  uvicorn.run("app.main:app", host="127.0.0.1", port=8000, workers=3)