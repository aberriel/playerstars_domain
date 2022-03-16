from clapy_basic_classes import BasicEntity, BasicValue
from marshmallow import fields, post_load


class RecurrenceInterval(BasicValue):
    def __init__(self,
                 unit: str = 'MONTH',
                 length: int = 1):
        self.unit = unit
        self.length = length

    class Schema(BasicValue.Schema):
        unit = fields.String(required=True, allow_none=False, default='MONTH')
        length = fields.Integer(required=True, allow_none=False, default=1)

        @post_load
        def post_load(self, data, many, partial):
            return RecurrenceInterval(**data)


class TrialInfo(BasicValue):
    def __init__(self,
                 period: int,
                 enabled: bool = False,
                 hold_setup_fee: bool = True):
        self.period = period
        self.enabled = enabled
        self.hold_setup_fee = hold_setup_fee

    class Schema(BasicValue.Schema):
        period = fields.Integer(required=True, allow_none=False)
        enabled = fields.Boolean(
            required=True,
            allow_none=False,
            default=False)
        hold_setup_fee = fields.Boolean(
            required=True,
            allow_none=False,
            default=True)

        @post_load
        def post_load(self, data, many, partial):
            return TrialInfo(**data)


class Product(BasicEntity):
    def __init__(self,
                 description: str,
                 price: int,
                 star_value: int,
                 star_type: str,
                 duration: int = 0,
                 entity_id: str = None,
                 name: str = None,
                 trial: TrialInfo = None,
                 interval: RecurrenceInterval = None):
        super(Product, self).__init__(entity_id=entity_id)
        self.name = name
        self.description = description
        self.star_value = star_value
        self.star_type = star_type
        self.price = price
        self.duration = duration
        self.trial = trial
        self.interval = interval

    class Schema(BasicEntity.Schema):
        name = fields.String(required=False, allow_none=True)
        description = fields.String(required=True, allow_none=False)
        price = fields.Integer(required=True, allow_none=False)
        star_value = fields.Integer(required=True, allow_none=False)
        star_type = fields.String(required=True, allow_none=False)
        duration = fields.Integer(required=True, allow_none=False)
        trial = fields.Nested(
            TrialInfo.Schema,
            required=False,
            allow_none=True)
        interval = fields.Nested(
            RecurrenceInterval.Schema,
            required=False,
            allow_none=True)

        @post_load
        def post_load(self, data, many, partial):
            return Product(**data)


class ProductPurchased(BasicValue):
    def __init__(self,
                 description: str,
                 price: int,
                 star_value: int,
                 star_type: str,
                 duration: int = 0,
                 name: str = None):
        super(ProductPurchased, self).__init__()
        self.name = name
        self.description = description
        self.star_value = star_value
        self.star_type = star_type
        self.price = price
        self.duration = duration

    class Schema(BasicValue.Schema):
        description = fields.String(required=True, allow_none=False)
        price = fields.Integer(required=True, allow_none=False)
        star_value = fields.Integer(required=True, allow_none=False)
        star_type = fields.String(required=True, allow_none=False)
        duration = fields.Integer(required=True, allow_none=False)
        name = fields.String(required=False, allow_none=True)

        @post_load
        def post_load(self, data, many, partial):
            return ProductPurchased(**data)
