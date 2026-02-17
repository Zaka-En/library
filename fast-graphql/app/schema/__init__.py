import strawberry
from .queries import Query
from .mutations import Mutation
from .subscriptions import Subscription


schema = strawberry.Schema(mutation=Mutation, query=Query, subscription=Subscription)