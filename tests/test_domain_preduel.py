from playerstars_domain import PreDuel
from tests.util import generic_serialize_roundtrip_test
from playerstars_domain.duel import DuelMemberType
from playerstars_domain.player import CoinType
from playerstars_domain.duel.pre_duel import Status


pre_duel = PreDuel(
    status=Status.AWAITING,
    star_type=CoinType.GOLDEN_STAR,
    duel_type=DuelMemberType.PLAYER,
    game_entity_id='12344556',
    console_entity_id='098751',
    challenger='098765',
    challenged='123890',
    ack=False,
    star_amount=10,
    duel_id='schrubles')


def test_pre_duel():
    assert pre_duel


def test_generic_roundtrip():
    generic_serialize_roundtrip_test(PreDuel, pre_duel)
