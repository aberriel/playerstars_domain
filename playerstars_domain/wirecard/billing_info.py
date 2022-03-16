from clapy_basic_classes import BasicValue
from marshmallow import fields, post_load
from typing import List


class CreditCard(BasicValue):
    def __init__(self,
                 holder_name: str,
                 expiration_month: str = None,
                 expiration_year: str = None,
                 number: str = None,
                 first_six_digits: str = None,
                 last_four_digits: str = None,
                 brand: str = None,
                 vault: str = None):
        self.holder_name = holder_name
        self.number = number
        self.expiration_month = expiration_month
        self.expiration_year = expiration_year
        self.first_six_digits = first_six_digits
        self.last_four_digits = last_four_digits
        self.brand = brand
        self.vault = vault

    class Schema(BasicValue.Schema):
        holder_name = fields.String(required=True, allow_none=False)
        expiration_month = fields.String(required=False, allow_none=True)
        expiration_year = fields.String(required=False, allow_none=True)
        number = fields.String(required=False, allow_none=True)
        first_six_digits = fields.String(required=False, allow_none=True)
        last_four_digits = fields.String(required=False, allow_none=True)
        brand = fields.String(required=False, allow_none=True)
        vault = fields.String(required=False, allow_none=True)

        @post_load
        def post_load(self, data, many, partial):
            return CreditCard(**data)


class BillingInfo(BasicValue):
    def __init__(self,
                 credit_card: CreditCard = None,
                 credit_cards: List[CreditCard] = None):
        self.credit_card = credit_card
        self.credit_cards = credit_cards

    class Schema(BasicValue.Schema):
        credit_card = fields.Nested(
            CreditCard.Schema,
            required=False,
            allow_none=True)
        credit_cards = fields.Nested(
            CreditCard.Schema,
            many=True,
            required=False,
            allow_none=True)

        @post_load
        def post_load(self, data, many, partial):
            return BillingInfo(**data)
