from datetime import datetime, timezone
from playerstars_domain import (
    CoinType,
    OperationType,
    SourceOperationType,
    StarTransaction
)
from pytest import fixture
from uuid import uuid4


@fixture
def star_transaction():
    operation_date = datetime(2019, 8, 21, 13, 11, 7, tzinfo=timezone.utc)
    star_transaction = StarTransaction(value=2,
                                       operation_date=operation_date,
                                       coin_type=CoinType.GOLDEN_STAR,
                                       operation_type=OperationType.DEBIT,
                                       source=SourceOperationType.DUEL,
                                       source_id=str(uuid4()))
    return star_transaction


def test_star_transaction(star_transaction):
    assert star_transaction


def test_star_transaction_with_id():
    operation_date = datetime(2019, 8, 21, 13, 11, 7, tzinfo=timezone.utc)
    star_transaction = StarTransaction(value=2,
                                       operation_date=operation_date,
                                       coin_type=CoinType.GOLDEN_STAR,
                                       operation_type=OperationType.DEBIT,
                                       source=SourceOperationType.DUEL,
                                       source_id=str(uuid4()))
    assert star_transaction


def test_star_transaction_to_json(star_transaction):
    operation_date = datetime(2019, 8, 21, 13, 11, 7, tzinfo=timezone.utc)
    star_transaction = StarTransaction(
        value=2,
        operation_date=operation_date,
        coin_type=CoinType.GOLDEN_STAR,
        operation_type=OperationType.DEBIT,
        source=SourceOperationType.DUEL,
        source_id='68dc45c5-43eb-4351-bead-4319aba7af85')
    assert star_transaction.to_json() == dict(
        value=2,
        operation_date='2019-08-21T13:11:07+00:00',
        coin_type='GOLDEN_STAR',
        operation_type='DEBIT',
        source='DUEL',
        source_id='68dc45c5-43eb-4351-bead-4319aba7af85'
    )
