import graphene

import machines.schema


class Query(machines.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)