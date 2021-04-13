import graphene
from graphene_djmoney.schema import MoneyInput

from .. import models
from .types import Product, User

class Queries(graphene.ObjectType):

    products = graphene.List(graphene.NonNull(types.Product), required=True)

    def resolve_products(self, info, **kwargs):
        return models.Product.objects.all()


class UpdateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        cost = MoneyInput(required=True)

    success = graphene.Boolean(required=True)
    product = graphene.Field(Product)

    def mutate(root, info, id, cost):
        models.Product.objects.filter(id=id).update(
            cost=cost.money,
        )
        product = models.Product.objects.get(id=id)
        return UpdateProduct(product=product, success=True)


class Mutations(graphene.ObjectType):
    update_product = UpdateProduct.Field()


schema = graphene.Schema(query=Queries, mutation=Mutations, types=[Product, User])
