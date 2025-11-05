# Overal blueprint for GraphQL schema. combines queries and mutations and types into a runnable graphql API.

import strawberry
from .queries import customer, orders_by_customer
from .mutations import create_customer, create_order

@strawberry.type
class Query: # Root query type
    customer = customer
    orders_by_customer = orders_by_customer

@strawberry.type
class Mutation: # Root mutation type
    create_customer = create_customer
    create_order = create_order

schema = strawberry.Schema(query=Query, mutation=Mutation) # Build schema       