import graphene
import users.schema
import diary.schema

from graphql_jwt import (
    ObtainJSONWebToken,
    Verify,
    Refresh
)


class Query(users.schema.Query, diary.schema.Query, graphene.ObjectType):
    pass


class Mutation(users.schema.Mutation, diary.schema.Mutation, graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    verify_token = Verify.Field()
    refresh_token = Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
