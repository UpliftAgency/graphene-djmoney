import json

from django.contrib.auth import get_user_model
from graphene_django.utils.testing import GraphQLTestCase
from graphql_relay import to_global_id

from test_app import models
from test_app.schema import schema

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
    formatted
    formatSpecified: formatted(format: "¤#,##0.00")
    formatType: formatted(formatType: "name")
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
        for title, amount in (("Product 1", 123.456), ("Product 2", 234.987)):
            products.append(
                models.Product.objects.get_or_create(
                    creator=user, title=title, cost=amount
                )[0]
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
        formatted = gql_product["cost"].pop("formatted")
        assert formatted.replace("\xa0", "") == "US$123.46"
        assert gql_product == {
            "id": to_global_id("Product", products[0].id),
            "cost": {
                "asString": "123.46 USD",
                "amount": 123.46,
                "amountWith1Digit": "123.5",
                "amountStr": "123.46",
                "currency": {
                    "code": "USD",
                    "name": "US Dollar",
                    "numeric": "840",
                    "symbol": "$",
                    "prefix": "$",
                },
                "formatSpecified": "US$123.46",
                "formatType": "123.46 U.S. dollars",
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
        formatted_updated = updated_product["cost"].pop("formatted")
        assert formatted_updated.replace("\xa0", "") == "£456.78"
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
            "formatSpecified": "£456.78",
            "formatType": "456.78 British pounds",
        }
