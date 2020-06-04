from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType
from graphene_djmoney.schema import Money

from test_app import models


class User(DjangoObjectType):
    """GraphQL type for the User model."""

    class Meta:
        model = get_user_model()
        interfaces = (graphene.relay.Node,)
        fields = ("id", "email", "username")


class Product(DjangoObjectType):
    class Meta:
        model = models.Product
        interfaces = (graphene.relay.Node,)
        fields = ["id", "cost"]
