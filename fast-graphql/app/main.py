from fastapi import FastAPI, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from app.schema import schema
from app.database import  get_db_session
import uvicorn
from strawberry.subscriptions import GRAPHQL_WS_PROTOCOL, GRAPHQL_TRANSPORT_WS_PROTOCOL
from app.schema.types import broadcast
from app.services.user_service import UserService
from app.services.author_service import AuthorService
from app.services.book_service import BookService
from typing import Annotated
from app.schema.types import broadcast


async def get_user_service(session = Depends(get_db_session)):
  return UserService(session=session)

async def get_author_service(session= Depends(get_db_session)):
  return AuthorService(session=session,broadcast=broadcast)

async def get_book_service(session=Depends(get_db_session)):
  return BookService(session=session)

async def get_context(
  request: Request,
  response: Response,
  user_service: Annotated[UserService,Depends(get_user_service)],
  author_service: Annotated[AuthorService,Depends(get_author_service)],
  book_service: Annotated[BookService,Depends(get_book_service)]):
  return {
    "request": request,
    "response": response,
    "user_service": user_service,
    "author_service": author_service,
    "book_service": book_service
  }


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
  uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
  #uvicorn.run("app.main:app", host="127.0.0.1", port=8000, workers=3)