from playerstars_domain import Lists
from pytest import fixture
from tests.util import generic_serialize_roundtrip_test


@fixture
def country_list():
    return ['Argentina', 'Argélia', 'Brasil', 'Chile', 'China', 'Uruguai']


@fixture
def state_list():
    return ['Amazonas',
            'Amapá',
            'Espírito Santo',
            'Minas Gerais',
            'Rio de Janeiro',
            'São Paulo']


@fixture
def new_lists(country_list, state_list):
    return Lists(countries=country_list, states=state_list)


@fixture
def lists_to_string():
    lists_str_1 = 'Countries: Argentina, Argélia, Brasil, '
    lists_str_2 = 'Chile, China, Uruguai / '
    lists_str_3 = 'States: Amazonas, Amapá, Espírito Santo, Minas Gerais, '
    lists_str_4 = 'Rio de Janeiro, São Paulo'
    lists_str = lists_str_1 + lists_str_2 + lists_str_3 + lists_str_4
    return lists_str


def test_lists():
    lists = Lists()
    assert lists
    assert not lists.countries
    assert not lists.states


def test_lists_with_countries(country_list):
    lists = Lists(countries=country_list)
    assert lists
    assert lists.countries is not None
    assert len(lists.countries) == 6


def test_lists_with_states(state_list):
    lists = Lists(states=state_list)
    assert lists
    assert lists.states is not None
    assert len(lists.states) == 6


def test_lists_repr(new_lists, lists_to_string):
    assert new_lists.__repr__() == lists_to_string


def test_lists_roundtrip(new_lists):
    generic_serialize_roundtrip_test(Lists, new_lists)
