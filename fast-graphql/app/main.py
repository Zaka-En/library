from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from app.schema import schema
from app.database import get_db

def get_context():
  db = next(get_db())
  return {"db": db}


app = FastAPI()

# Configurar CORS
app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5173","http://frontend:5173","http://localhost:3000", "http://frontend:3000"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

graphql_app = GraphQLRouter(
  schema,
  context_getter=get_context
)

app.include_router(graphql_app, prefix='/graphql')


if __name__ == "__main__":
  import uvicorn
  uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)