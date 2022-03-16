from uuid import uuid4

from pytest import fixture

from playerstars_domain import CountryRegion, StateRegion


@fixture
def state_list():
    return ['Amazonas',
            'Amapá',
            'Bahia',
            'Ceará',
            'Maranhão',
            'Pernambuco',
            'Piauí']


@fixture
def country_list():
    return ['Argentina',
            'Argélia',
            'Brasil',
            'Chile',
            'China',
            'Mexico',
            'Paraguay']


def test_create_region_country_with_id(country_list):
    region_id = str(uuid4())
    region = CountryRegion(name='América Latina',
                           minimum_bet=1,
                           countries=country_list,
                           entity_id=region_id)
    assert region is not None
    assert region.entity_id == region_id


def test_create_region_country_with_countries(country_list):
    region = CountryRegion(name='América Latina',
                           minimum_bet=1,
                           countries=country_list)
    assert region is not None
    assert region.countries is not None
    assert len(region.countries) == 7
    assert 'Brasil' in region.countries


def test_create_region_state_with_states(state_list):
    region = StateRegion(name='Nordeste',
                         minimum_bet=1,
                         states=state_list)
    assert region is not None
    assert region.states is not None
    assert len(region.states) == 7
    assert 'Bahia' in region.states


def test_create_region_state_with_id(state_list):
    region_id = str(uuid4())
    region = StateRegion(name='Nordeste',
                         minimum_bet=1,
                         states=state_list,
                         entity_id=region_id)
    assert region
    assert region.entity_id == region_id


def test_country_region_from_json():
    america_norte_id = str(uuid4())
    json_data = dict(entity_id=america_norte_id,
                     name='America do Norte',
                     minimum_bet=2,
                     countries=[
                         'Estados Unidos',
                         'Canada',
                         'Mexico'])

    region = CountryRegion.from_json(json_data)
    assert region
    assert region.name == 'America do Norte'
    assert region.entity_id == america_norte_id
    assert region.minimum_bet == 2

    assert 'Estados Unidos' in region.countries
    assert 'Canada' in region.countries
    assert 'Mexico' in region.countries


def test_state_region_from_json():
    region_id = str(uuid4())
    json_data = dict(entity_id=region_id,
                     name='Sudeste',
                     minimum_bet=1,
                     states=['Rio de Janeiro', 'Sao Paulo', 'Minas Gerais'])

    region = StateRegion.from_json(json_data)
    assert region
    assert region.entity_id == region_id
    assert region.name == 'Sudeste'
    assert region.minimum_bet == 1
    assert region.states
    assert len(region.states) == 3

    assert 'Rio de Janeiro' in region.states
    assert 'Sao Paulo' in region.states
    assert 'Minas Gerais' in region.states
