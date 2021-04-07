import graphene

import awesomeblog.graphql.blog.schema


class Query(awesomeblog.graphql.blog.schema.BlogQueries, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
