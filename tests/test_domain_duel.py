from datetime import datetime
from unittest.mock import MagicMock

from playerstars_domain import (
    CoinType,
    ComponentResult,
    Console,
    Duel,
    DuelComponentResult,
    DuelMemberType,
    DuelStatus,
    DuelType,
    Game)
from playerstars_domain.duel import (DefiantNotFound, DuelNotDuelingException)
from playerstars_domain.utils.datetime_helper import aware_utc
from tests.util import generic_serialize_roundtrip_test

import pytest


def make_game_data():
    return Game(name='Need for Speed', logo_path='/images/nfs.jpg')


def make_console_data():
    game = make_game_data()
    return Console(name='Xbox One',
                   logo_path='/images/xbox_one.jpg',
                   tag_name='nick#1',
                   games=[game])


def make_duel():
    game = make_game_data()
    console = make_console_data()
    creation_datetime = aware_utc(datetime(1986, 12, 16, 15, 39, 2))
    time_start = aware_utc(datetime(1986, 12, 16, 15, 40, 8))
    return Duel(entity_id='duel123',
                challenger='a1b2c3',
                challenged='q1w2e3r4',
                creation_datetime=creation_datetime,
                member_type=DuelMemberType.PLAYER,
                duel_type=DuelType.INDIVIDUAL,
                game=game,
                console=console,
                star_type=CoinType.RED_STAR,
                bet_size=3,
                time_start=time_start,
                challenged_accept=False,
                time_to_finish_duel=300,
                time_to_accept_invitation=5)


def test_create_duel():
    duel_data = make_duel()
    assert duel_data


def make_duel_result():
    duel_result = DuelComponentResult(
        result=ComponentResult.LOSER,
        submission_datetime=aware_utc(datetime(2020, 1, 5, 14, 15, 16)))
    return duel_result


def test_challenger_confirmed():
    duel_data = make_duel()
    duel_data.challenger_confirmed()
    assert duel_data.challenger_confirmation


def test_challenged_confirmed():
    duel = make_duel()
    duel.challenged_confirmed()
    assert duel.challenged_confirmation


def test_bet_size():
    duel = make_duel()
    duel.increase_bet_size(30)
    assert duel.bet_size == 33
    duel.decrease_bet_size(20)
    assert duel.bet_size == 13


def test_bet_size_value_error():
    duel = make_duel()
    with pytest.raises(ValueError) as exc:
        duel.decrease_bet_size(5000)
    assert str(exc.value) == 'Não é possivel ter apostas negativas'


def test_submit_result():
    duel = make_duel()
    duel.status = DuelStatus.DUELING
    duel.submit_result(defiant_id='q1w2e3r4', result=ComponentResult.LOSER)

    assert duel.challenger_duel_result is None
    assert duel.challenged_duel_result is not None
    assert duel.challenged_duel_result.result == ComponentResult.LOSER

    duel.submit_result(defiant_id='a1b2c3', result=ComponentResult.WINNER)
    assert duel.challenger_duel_result is not None
    assert duel.challenger_duel_result.result == ComponentResult.WINNER


def test_submit_result_defiant_not_found_error():
    duel = make_duel()
    duel.status = DuelStatus.DUELING
    with pytest.raises(DefiantNotFound) as exc:
        duel.submit_result(defiant_id='123', result=ComponentResult.LOSER)
    assert 'Defiant 123 not found' in str(exc.value)


def test_submit_result_status_error():
    duel = make_duel()
    with pytest.raises(DuelNotDuelingException) as exc:
        duel.submit_result(defiant_id='q1w2e3r4', result=ComponentResult.WINNER)
    assert 'Duel not in progress status' in str(exc.value)


def test_duel_result():
    duel_result = make_duel_result()
    assert duel_result


def test_duel_result_to_string():
    duel_result = make_duel_result()
    assert duel_result.to_string() == '2020-01-05T14:15:16+00:00 - LOSER'


def test_duel_result_repr():
    duel_result = make_duel_result()
    assert str(duel_result) == \
        'Result: LOSER | ' \
        'Submission Datetime: 2020-01-05T14:15:16+00:00 | ' \
        'Result Image Path: No Image'


def test_duel_roundtrip():
    duel = make_duel()
    generic_serialize_roundtrip_test(Duel, duel)


def test_duel_result_roundtrip():
    duel_result = make_duel_result()
    generic_serialize_roundtrip_test(DuelComponentResult, duel_result)


def test_duel_save():
    duel = Duel(
        challenger=MagicMock(),
        game=MagicMock(),
        console=MagicMock())
    duel.adapter = MagicMock()
    saved_id = duel.save_graphql()
    duel.adapter.save.assert_called_with(duel, False)
    assert saved_id == duel.adapter.save()
