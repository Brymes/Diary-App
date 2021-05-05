import graphene

from graphql import GraphQLError
from graphene_django import DjangoObjectType

from graphql_jwt.decorators import login_required
# from graphql_jwt.shortcuts import create_refresh_token, get_token

from django.contrib.auth import get_user_model
# FIXME from .models import User


class UserType(DjangoObjectType):

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "password", "first_name", "email")


class CreateUser(graphene.Mutation):

    class Arguments:
        first_name = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        username = graphene.String(required=True)

    # Note:: This defines the response of the mutation
    user = graphene.Field(UserType)
    # token = graphene.String()
    # refresh_token = graphene.String()

    @classmethod
    def mutate(cls, root, info, password, email, first_name, username):
        user = get_user_model()(
            username=username,
            email=email,
            first_name=first_name
        )

        user.set_password(password)
        user.save()

        # token = get_token(user)
        # refresh_token = create_refresh_token(user)

        return CreateUser(user=user)
        #   , token=token, refresh_token=refresh_token)


class Query(graphene.ObjectType):

    user = graphene.Field(UserType, email=graphene.String(required=True))
    self_user = graphene.Field(UserType)

    def resolve_user(self, info, email):

        return get_user_model().objects.get(username=email)

    def resolve_self_user(self, info):
        user = info.context.user

        # Check to to ensure you're signed-in to see yourself
        if user.is_anonymous:
            raise Exception('Authentication Failure: Your must be signed in')
        return user


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
