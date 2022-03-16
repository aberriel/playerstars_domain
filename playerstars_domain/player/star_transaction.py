from clapy_basic_classes import BasicEntity, BasicValue
from datetime import datetime
from enum import Enum
from marshmallow import fields, post_load
from marshmallow_enum import EnumField


class CoinType(Enum):
    RED_STAR = 'RED_STAR'
    GOLDEN_STAR = 'GOLDEN_STAR'


class OperationType(Enum):
    CREDIT = 'CREDIT'
    DEBIT = 'DEBIT'


class SourceOperationType(Enum):
    DUEL = 'DUEL'
    FINANCIAL_TRANSACTION = 'FINANCIAL_TRANSACTION'
    TEAM_DUEL = 'TEAM_DUEL'
    CHAMPIONSHIP = 'CHAMPIONSHIP'


class StarTransaction(BasicEntity):
    value = None
    source_id = None
    operation_type = None
    coin_type = None
    source = None
    operation_date = None

    def __init__(self,
                 source_id: str,
                 value: int = None,
                 operation_type: OperationType = OperationType.DEBIT,
                 coin_type: CoinType = CoinType.GOLDEN_STAR,
                 source: SourceOperationType = SourceOperationType.DUEL,
                 operation_date: datetime = None,
                 entity_id: str = None):
        super(StarTransaction, self).__init__(entity_id=entity_id)
        self.value = value
        self.operation_type = operation_type
        self.operation_date = operation_date or datetime.now()
        self.coin_type = coin_type
        self.source = source
        self.source_id = source_id

    class Schema(BasicValue.Schema):
        value = fields.Integer(required=False, allow_none=True)
        source_id = fields.String(required=True, allow_none=False)
        operation_type = EnumField(
            OperationType,
            required=True,
            allow_none=False)
        coin_type = EnumField(CoinType, required=True, allow_none=False)
        source = EnumField(
            SourceOperationType,
            required=True,
            allow_none=False)
        operation_date = fields.DateTime(
            required=True,
            allow_none=False,
            format='iso')

        @post_load
        def post_load(self, data, many, partial):
            return StarTransaction(**data)
