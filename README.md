# graphene-djmoney

![python package](https://github.com/UpliftAgency/graphene-djmoney/actions/workflows/pythonpackage.yml/badge.svg)

[![Build Status](https://travis-ci.org/UpliftAgency/graphene-djmoney.svg?branch=master)](https://travis-ci.org/UpliftAgency/graphene-djmoney) [![PyPI version](https://badge.fury.io/py/graphene-djmoney.svg)](https://badge.fury.io/py/graphene-djmoney)

## Introduction

GraphQL Money types for Django using graphene and django-money (djmoney). If you use `django`, `graphene_django`, and `django-money`, this library is for you.

Supported on:

* Python 3.7+ (likely earlier versions too, needs tested)
* Django 2+
* graphene-django 2+
* django-money 1+

Here's how it works. Automagically get this query:

```graphql
query Products {
    products {
        id
        cost {
            ...moneyFragment
        }
    }
}

fragment moneyFragment on Money {
    asString  # "123.45 USD"
    amount    # 123.45
    amountStr # "123.45"
    currency {
        code  # "USD"
        name  # "US Dollar"
        # These are not as commonly used, see tests:
        numeric
        symbol
        prefix
    }
}
```

With this code:

```python
# yourapp/models.py
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from djmoney.models.fields import MoneyField


class User(AbstractUser):
    pass


class Product(models.Model):
    creator = models.ForeignKey(User, related_name="products", on_delete=models.CASCADE)
    title = models.CharField(max_length=2000)
    cost = MoneyField(
        max_digits=settings.CURRENCY_MAX_DIGITS,
        decimal_places=settings.CURRENCY_DECIMAL_PLACES,
        default_currency=settings.BASE_CURRENCY,
        null=True,
        blank=True,
    )

# yourapp/schema/types.py

import graphene
from graphene_django import DjangoObjectType

from yourapp import models


class Product(DjangoObjectType):
    class Meta:
        model = models.Product
        interfaces = (graphene.relay.Node,)
        fields = ("id", "cost")

# yourapp/schema/__init__.py

import graphene

from .. import models
from .types import Product

class Queries(graphene.ObjectType):

    products = graphene.List(graphene.NonNull(types.Product), required=True)

    def resolve_products(self, info, **kwargs):
        return models.Product.objects.all()


schema = graphene.Schema(query=Queries, types=[Product])

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

### Changelog

**0.2.0**

    - #5, #6, #7 Upgrade to py-moneyed 2.0, add babel format support (new field, `formatted`)
    - **Breaking change**: removes `suffix` from schema, since babel doesn't support out of the box.


**0.1.3**

    Initial release, sort of.

## Contributing

Running tests:

```bash
poetry run pytest
```

Still TODO. For now, please open a pull request or issue.
