import graphene

from apps.links import schema as links_schema

class Query(links_schema.Query, graphene.ObjectType):
    pass

class Mutation(links_schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query = Query, mutation = Mutation)
