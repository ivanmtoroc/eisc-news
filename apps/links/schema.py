import graphene
from graphene_django import DjangoObjectType

from apps.users.schema import UserType
from .models import Link, Vote

class LinkType(DjangoObjectType):
    class Meta:
        model = Link

class VoteType(DjangoObjectType):
    class Meta:
        model = Vote

class Query(graphene.ObjectType):
    links = graphene.List(
                    LinkType,
                    first = graphene.Int(),
                    skip = graphene.Int(),
                )
    votes = graphene.List(VoteType)

    def resolve_links(self, info, first = None, skip = None, **kwargs):
        links = Link.objects.all()

        if skip:
            links = links[skip:]

        if first:
            links = links[:first]

        return links

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()

class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    posted_by = graphene.Field(UserType)

    class Arguments:
        url = graphene.String()
        description = graphene.String()

    def mutate(self, info, url, description):
        user = info.context.user

        link = Link(
            url = url,
            description = description,
            posted_by = user,
        )
        link.save()

        return CreateLink(
            id = link.id,
            url = link.url,
            description = link.description,
            posted_by = link.posted_by,
        )

class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    link = graphene.Field(LinkType)

    class Arguments:
        link_id = graphene.Int()

    def mutate(self, info, link_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Tienes que esta loggeado para poder votar!')

        link = Link.objects.filter(id = link_id).first()
        if not link:
            raise Exception('Link invalido!')

        Vote.objects.create(
            user = user,
            link = link,
        )

        return CreateVote(user = user, link = link)

class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    create_vote = CreateVote.Field()
