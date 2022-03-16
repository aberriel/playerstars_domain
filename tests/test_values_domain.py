from playerstars_domain import AwardDivisionException, Values
from playerstars_domain.values.validator_maps import ValidatorMaps
import pytest
from tests.util import generic_serialize_roundtrip_test

validator_maps = ValidatorMaps(game_id='game_id', class_name='ValidatorClass')


def make_values():
    return Values(
        entity_id='id123',
        red_bet_sizes=[1, 3, 5],
        gold_bet_sizes=[2, 4, 6],
        max_players_team=5,
        time_to_check_championship_viability=30,
        championship_award_first_place_perc=70,
        championship_award_second_place_perc=20,
        championship_award_third_place_perc=10,
        interval_between_championship_levels=30,
        validator_maps=[validator_maps])


def make_values_json():
    return {
        'entity_id': 'id123',
        'red_bet_sizes': [1, 3, 5],
        'gold_bet_sizes': [2, 4, 6],
        'max_players_team': 5,
        'time_to_check_championship_viability': 30,
        'championship_award_first_place_perc': 70,
        'championship_award_second_place_perc': 20,
        'championship_award_third_place_perc': 10,
        'interval_between_championship_levels': 30,
        'validator_maps': [{'game_id': 'game_id', 'class_name': 'ValidatorClass'}]
    }


def make_values_with_award_division_error():
    return Values(
        entity_id='id123',
        red_bet_sizes=[1, 3, 5],
        gold_bet_sizes=[2, 4, 6],
        max_players_team=5,
        time_to_check_championship_viability=30,
        championship_award_first_place_perc=70,
        championship_award_second_place_perc=40,
        championship_award_third_place_perc=20,
        interval_between_championship_levels=30,
        validator_maps=[validator_maps])


def test_bet_sizes():
    sizes = make_values()
    assert sizes
    assert sizes.to_json() == make_values_json()


def test_award_division_error():
    with pytest.raises(AwardDivisionException) as exc:
        make_values_with_award_division_error()
    assert 'Awards has to sum 100, but the sum is 130' in str(exc.value)


def test_first_championship_place_award_zero():
    with pytest.raises(AwardDivisionException) as exc:
        Values(
            entity_id='id123',
            red_bet_sizes=[1, 3, 5],
            gold_bet_sizes=[2, 4, 6],
            max_players_team=5,
            time_to_check_championship_viability=30,
            championship_award_first_place_perc=0,
            championship_award_second_place_perc=70,
            championship_award_third_place_perc=30,
            interval_between_championship_levels=30,
            validator_maps=[validator_maps])
    assert 'First tournament place award cannot be zero or negative' \
           in str(exc.value)


def test_first_championship_place_award_negative():
    with pytest.raises(AwardDivisionException) as exc:
        Values(
            entity_id='id123',
            red_bet_sizes=[1, 3, 5],
            gold_bet_sizes=[2, 4, 6],
            max_players_team=5,
            time_to_check_championship_viability=30,
            championship_award_first_place_perc=-30,
            championship_award_second_place_perc=90,
            championship_award_third_place_perc=40,
            interval_between_championship_levels=30,
            validator_maps=[validator_maps])
    assert 'First tournament place award cannot be zero or negative' \
           in str(exc.value)


def test_second_championship_place_award_negative():
    with pytest.raises(AwardDivisionException) as exc:
        Values(
            entity_id='id123',
            red_bet_sizes=[1, 3, 5],
            gold_bet_sizes=[2, 4, 6],
            max_players_team=5,
            time_to_check_championship_viability=30,
            championship_award_first_place_perc=120,
            championship_award_second_place_perc=-20,
            championship_award_third_place_perc=0,
            interval_between_championship_levels=30,
            validator_maps=[validator_maps])
    assert 'Second tournament place award cannot be negative' \
           in str(exc.value)


def test_third_championship_place_award_negative():
    with pytest.raises(AwardDivisionException) as exc:
        Values(
            entity_id='id123',
            red_bet_sizes=[1, 3, 5],
            gold_bet_sizes=[2, 4, 6],
            max_players_team=5,
            time_to_check_championship_viability=30,
            championship_award_first_place_perc=70,
            championship_award_second_place_perc=50,
            championship_award_third_place_perc=-20,
            interval_between_championship_levels=30,
            validator_maps=[validator_maps])
    assert 'Third tournament place award cannot be negative' in str(exc.value)


def test_first_championship_place_award_less_than_second_place():
    with pytest.raises(AwardDivisionException) as exc:
        Values(
            entity_id='id123',
            red_bet_sizes=[1, 3, 5],
            gold_bet_sizes=[2, 4, 6],
            max_players_team=5,
            time_to_check_championship_viability=30,
            championship_award_first_place_perc=40,
            championship_award_second_place_perc=50,
            championship_award_third_place_perc=10,
            interval_between_championship_levels=30,
            validator_maps=[validator_maps])
    assert 'First tournament place award cannot be ' \
           'less than second place or third place award' in str(exc.value)


def test_first_championship_place_award_less_than_third_place():
    with pytest.raises(AwardDivisionException) as exc:
        Values(
            entity_id='id123',
            red_bet_sizes=[1, 3, 5],
            gold_bet_sizes=[2, 4, 6],
            max_players_team=5,
            time_to_check_championship_viability=30,
            championship_award_first_place_perc=30,
            championship_award_second_place_perc=20,
            championship_award_third_place_perc=50,
            interval_between_championship_levels=30,
            validator_maps=[validator_maps])
    assert 'First tournament place award cannot be ' \
           'less than second place or third place award' in str(exc.value)


def test_second_championship_place_award_less_than_third_place():
    with pytest.raises(AwardDivisionException) as exc:
        Values(
            entity_id='id123',
            red_bet_sizes=[1, 3, 5],
            gold_bet_sizes=[2, 4, 6],
            max_players_team=5,
            time_to_check_championship_viability=30,
            championship_award_first_place_perc=50,
            championship_award_second_place_perc=20,
            championship_award_third_place_perc=30,
            interval_between_championship_levels=30,
            validator_maps=[validator_maps])
    assert 'Second tournament place award cannot be ' \
           'less than third place award' in str(exc.value)


def test_user_roundtrip():
    generic_serialize_roundtrip_test(Values, make_values())
