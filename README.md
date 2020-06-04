# graphene-djmoney

[![Build Status](https://travis-ci.org/UpliftAgency/graphene-djmoney.svg?branch=master)](https://travis-ci.org/UpliftAgency/graphene-djmoney) [![PyPI version](https://badge.fury.io/py/graphene-djmoney.svg)](https://badge.fury.io/py/graphene)

## Introduction

Automagically get this query:

```graphql
query Products {
    products {
        id
        cost {
            ...moneyFieldInfo
        }
    }
}

fragment moneyFieldInfo on MoneyField {
    amount
    currency {
        code
        name
        symbol
    }
}
```

With this code:

```python
# yourapp/models.py
from django.db import models
from djmoney.models.fields import MoneyField


class Product(models.Model):
    """
    A bid and/or comments on a line item by a builder.
    """

    cost = MoneyField(
        max_digits=settings.CURRENCY_MAX_DIGITS,
        decimal_places=settings.CURRENCY_DECIMAL_PLACES,
        default_currency=settings.DEFAULT_CURRENCY,
        null=True,
        blank=True,
    )

# yourapp/graphql/types.py

import graphene
from graphene_django import DjangoObjectType

from yourapp import models


class Product(DjangoObjectType):
    class Meta:
        model = models.Product
        interfaces = (graphene.relay.Node,)
        fields = ("id", "cost")

# yourapp/schema.py

from .graphql import types

class Queries(graphene.ObjectType):

    products = graphene.List(graphene.NonNull(types.Product), required=True)


schema = graphene.Schema(query=Queries, types=types)

# yourapp/settings.py

INSTALLED_APPS += [
    "graphene_djmoney",
]

GRAPHENE = {
    "SCHEMA": "yourapp.schema.schema",
}

```

## Installation

```bash
pip install graphene-djmoney
```

## Contributing

Still TODO. For now, please open a pull request or issue.
