from fastapi import FastAPI
from fastapi.requests
from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import schema

app = FastAPI()

graphql_app = GraphQLRouter(schema, graphiql=True) # Enable GraphiQL UI
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def homepage():
    return {"message": "Welcome to the My Orders Service!"}