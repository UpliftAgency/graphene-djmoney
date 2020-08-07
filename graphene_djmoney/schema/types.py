from django.utils.functional import cached_property

import graphene
from graphene.types import InputObjectType, ObjectType, Scalar
from graphql.language import ast
from graphene_django.converter import convert_django_field
from moneyed.localization import CurrencyFormatter

from djmoney.models.fields import MoneyField
from djmoney.money import Money as DJMoney, get_current_locale
from djmoney.settings import BASE_CURRENCY, DECIMAL_PLACES

__all__ = ("Money", "MoneyInput", "StringMoney")

_cf = CurrencyFormatter()


class StringMoney(Scalar):
    @staticmethod
    def serialize(money):
        if money is None or money == 0:
            money = DJMoney(amount=0, currency=BASE_CURRENCY)

        if isinstance(money, DJMoney):
            return "{0:.{1}f} {2}".format(money.amount, DECIMAL_PLACES, money.currency)

        raise NotImplementedError

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return StringMoney.parse_value(node.value)

    @staticmethod
    def parse_value(value):
        if isinstance(value, DJMoney):
            return value

        amount, currency = value.split(" ")
        return DJMoney(amount=float(amount), currency=currency)


class Currency(ObjectType):
    code = graphene.String(
        description="A ISO-421 3-letter currency. See https://en.wikipedia.org/wiki/ISO_4217#Active_codes",
        required=True,
    )
    name = graphene.String(
        description="A human readable name, e.g. US Dollar", required=True
    )
    numeric = graphene.String(
        description="A ISO-421 numeric code. See https://en.wikipedia.org/wiki/ISO_4217#Active_codes",
        required=True,
    )
    symbol = graphene.String(
        description="The currency's symbol, e.g. $ for USD", required=True
    )
    prefix = graphene.String(
        description="The currency's prefix, e.g. $ for USD", required=True
    )
    suffix = graphene.String(
        description="The currency's symbol, e.g. € for EUR", required=True
    )

    def resolve_symbol(self, info, **kwargs):
        return "".join(get_sign_definition(self)).strip()

    def resolve_prefix(self, info, **kwargs):
        return get_sign_definition(self)[0].strip()

    def resolve_suffix(self, info, **kwargs):
        return get_sign_definition(self)[1].strip()


class Money(ObjectType):
    as_string = StringMoney(required=True)

    def resolve_as_string(self, info, **kwargs):
        return self

    amount = graphene.Float(description="The numerical amount.", required=True)
    amount_str = graphene.String(
        description="The string version of the numerical amount.",
        required=True,
    )

    def resolve_amount_str(self, info, **kwargs):
        return self.amount

    currency = graphene.Field(Currency, required=True)

    def resolve_currency(self, info, **kwargs):
        return dict(
            code=self.currency.code,
            name=self.currency.name,
            numeric=self.currency.numeric,
        )

    format_amount = graphene.Field(graphene.String, decimals=graphene.Int(), required=True)

    def resolve_format_amount(self, info, *, decimals: int, **kwargs):
        return "{0:.{1}f}".format(self.amount, decimals)


class MoneyInput(InputObjectType):
    amount = graphene.String(description="The numerical amount.", required=True)
    currency = graphene.String(description="The ISO-421 3-letter currency code.", required=True)

    def __str__(self):
        return "{0} {1}".format(self.amount, self.currency)

    @property
    def money(self):
        return DJMoney(self.amount, self.currency)


@convert_django_field.register(MoneyField)
def convert_field_to_graphql_money(field, registry=None):
    return graphene.Field(Money, description=field.help_text, required=(not field.null))


def get_sign_definition(money_dict):
    if "_sign_definition" not in money_dict:
        try:
            money_dict["_sign_definition"] = _cf.get_sign_definition(money_dict["code"], get_current_locale())
        except IndexError:
            money_dict["_sign_definition"] = ("", "")
    return money_dict["_sign_definition"]
