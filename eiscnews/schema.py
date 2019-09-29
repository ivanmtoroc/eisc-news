import graphene
import graphql_jwt

from apps.links import schema as links_schema
from apps.users import schema as users_schema


class Query(
        links_schema.Query,
        users_schema.Query,
        graphene.ObjectType
    ):
    pass

class Mutation(
        links_schema.Mutation,
        users_schema.Mutation,
        graphene.ObjectType
    ):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query = Query, mutation = Mutation)
