
import json

from django.contrib.auth import get_user_model
from graphql_relay import to_global_id
from graphene_django.utils.testing import GraphQLTestCase

from djmoney.money import Money
from test_app.schema import schema
from test_app import models


MONEY_FRAGMENT = """
fragment moneyFragment on Money {
    asString
    amount
    amountStr
    currency {
        code
        name
        numeric
        symbol
        prefix
    }
    amountWith1Digit: formatAmount(decimals: 1)
}
"""


class FieldsTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def test_query_and_mutation(self):
        user = get_user_model().objects.create_user(
            "user1", "user1@example.com", "password"
        )

        products = []
        for title, amount in (("Product 1", 100), ("Product 2", 200)):
            products.append(
                models.Product.objects.get_or_create(creator=user, title=title, cost=amount)[0]
            )

        response = self.query(
            """
            query {
                products {
                    id
                    cost {
                        ...moneyFragment
                    }
                }
            }

            %s
            """
            % MONEY_FRAGMENT
        )

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        gql_product = content["data"]["products"][0]
        assert gql_product == {
            "id": to_global_id("Product", products[0].id),
            "cost": {
                "asString": "100.00 USD",
                "amount": 100.0,
                "amountWith1Digit": "100.0",
                "amountStr": "100.00",
                "currency": {
                    "code": "USD",
                    "name": "US Dollar",
                    "numeric": "840",
                    "symbol": "$",
                    "prefix": "$",
                },
            },
        }

        response_mutate = self.query(
            """
            mutation($id:ID!, $moneyInput:MoneyInput!) {
                updateProduct(id:$id, cost:$moneyInput) {
                    product {
                        cost {
                            ...moneyFragment
                        }
                    }
                    success
                }
            }
            %s
            """
            % MONEY_FRAGMENT,
            variables={
                "id": products[0].id,
                "moneyInput": {"amount": "456.78", "currency": "GBP"},
            },
        )
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response_mutate)

        content = json.loads(response_mutate.content)
        updated_product = content["data"]["updateProduct"]["product"]
        assert updated_product["cost"] == {
            "asString": "456.78 GBP",
            "amount": 456.78,
            "amountWith1Digit": "456.8",
            "amountStr": "456.78",
            "currency": {
                "code": "GBP",
                "name": "British Pound",
                "numeric": "826",
                "symbol": "£",
                "prefix": "£",
            },
        }
