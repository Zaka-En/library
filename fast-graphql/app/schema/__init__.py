import strawberry
from .queries import Query, Subscription
from .mutations import Mutation


schema = strawberry.Schema(mutation=Mutation, query=Query, subscription=Subscription)