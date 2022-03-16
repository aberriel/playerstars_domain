from playerstars_domain import Console, Game, GameType
from pytest import fixture, raises
from uuid import uuid4

from playerstars_domain.console.console import GameNotFoundException


@fixture
def game_1():
    return Game(entity_id='7e273e96',
                name='sonic',
                logo_path='/images/sonic.png',
                game_type=GameType.INDIVIDUAL)


@fixture
def game_2():
    return Game(entity_id='d399786a',
                name='fifa',
                logo_path='/images/fifa.png',
                game_type=GameType.COLLECTIVE)


@fixture
def game_3():
    return Game(entity_id='c2e0222f-e44a-49c2-9ea1-0bb48c1f55ae',
                name='megaman',
                logo_path='/images/megaman.png',
                victories=100,
                game_type=GameType.BOTH)


@fixture
def game_list(game_1, game_2, game_3):
    return [game_1, game_2, game_3]


@fixture
def console(game_list):
    console = Console(entity_id='1701db37-a488-49e3-b039-1e0909fbf561',
                      name='Atari',
                      logo_path='/user/fifa.png',
                      tag_name='nick#123',
                      games=game_list)
    return console


def test_console_with_id(game_list):
    console_id = str(uuid4())
    console = Console(name='Atari',
                      logo_path='/images/atari.png',
                      tag_name='nick#123',
                      games=game_list,
                      entity_id=console_id)
    assert console
    assert console.entity_id == console_id


def test_console(game_list):
    console = Console(name='Master Sytem',
                      logo_path='/images/mastersystem.jog',
                      tag_name=None,
                      games=game_list)
    assert console


def test_console_repr(console):
    assert console.__repr__()
    assert console.__repr__() == "Console: Atari, Games: sonic, fifa, megaman"


def test_console_attributes(console):
    assert console.name == 'Atari'
    assert console.logo_path == '/user/fifa.png'


def test_console_to_json(game_list):
    console = Console(name='Mega Drive',
                      logo_path='/images/megadrive.png',
                      tag_name='nick#123',
                      games=game_list)
    console_id = console.entity_id

    game_sonic = next((x for x in game_list if x.name == 'sonic'), None)
    game_sonic_id = game_sonic.entity_id
    game_fifa = next((x for x in game_list if x.name == 'fifa'), None)
    game_fifa_id = game_fifa.entity_id
    game_megaman = next((x for x in game_list if x.name == 'megaman'), None)
    game_megaman_id = game_megaman.entity_id

    assert console.to_json() == dict(
        name='Mega Drive',
        logo_path='/images/megadrive.png',
        tag_name='nick#123',
        games=[{'entity_id': game_sonic_id,
                'logo_path': '/images/sonic.png',
                'name': 'sonic',
                'points': 0,
                'victories': 0,
                'game_type': 'INDIVIDUAL',
                'tutorial': None,
                'mask': None,
                'active': False},
               {'entity_id': game_fifa_id,
                'logo_path': '/images/fifa.png',
                'name': 'fifa',
                'points': 0,
                'victories': 0,
                'game_type': 'COLLECTIVE',
                'tutorial': None,
                'mask': None,
                'active': False},
               {'entity_id': game_megaman_id,
                'logo_path': '/images/megaman.png',
                'name': 'megaman',
                'points': 0,
                'victories': 100,
                'game_type': 'BOTH',
                'tutorial': None,
                'mask': None,
                'active': False}],
        entity_id=console_id)


def test_console_from_json():
    nintendo64_id = str(uuid4())
    mario64_id = str(uuid4())
    fzero_id = str(uuid4())
    zelda_id = str(uuid4())

    json_data = dict(entity_id=nintendo64_id,
                     name='Nintendo 64',
                     logo_path='/images/nintendo64.png',
                     tag_name='nick#123',
                     games=[{'entity_id': mario64_id,
                             'name': 'Mario 64',
                             'logo_path': '/images/mario64.png',
                             'game_type': 'INDIVIDUAL',
                             'points': 0},
                            {'entity_id': fzero_id,
                             'name': 'F-Zero',
                             'logo_path': '/images/fzero.png',
                             'game_type': 'COLLECTIVE',
                             'points': 0},
                            {'entity_id': zelda_id,
                             'name': 'Zelda',
                             'logo_path': '/images/zelda.png',
                             'game_type': 'BOTH',
                             'points': 0}])

    console = Console.from_json(json_data)
    assert console
    assert console.entity_id == nintendo64_id
    assert console.name == 'Nintendo 64'
    assert console.logo_path == '/images/nintendo64.png'
    assert console.tag_name == 'nick#123'
    assert console.games
    assert len(console.games) == 3

    game_mario64 = next((x for x in console.games if x.name == 'Mario 64'), None)
    assert game_mario64
    assert game_mario64.entity_id == mario64_id
    assert game_mario64.logo_path == '/images/mario64.png'
    assert game_mario64.game_type == GameType.INDIVIDUAL

    game_zelda = next((x for x in console.games if x.name == 'Zelda'), None)
    assert game_zelda
    assert game_zelda.entity_id == zelda_id
    assert game_zelda.logo_path == '/images/zelda.png'
    assert game_zelda.game_type == GameType.BOTH


def test_find_game_by_id(console):
    sonic = console.find_game_by_id('7e273e96')
    assert sonic is not None
    assert sonic.name == 'sonic'


def test_find_game_not_found(console):
    with raises(GameNotFoundException):
        console.find_game_by_id(str(uuid4()))


def test_get_game_victories_by_id(console):
    assert console.get_game_victories_by_id("c2e0222f-e44a-49c2-9ea1-0bb48c1f55ae") == 100
    assert not console.get_game_victories_by_id("c2e0222f-e44a-49c2-9ea1-0bb48c1fae")


def test_get_individual_games(console, game_1, game_3):
    game_list = console.get_individual_games()
    assert game_list == [game_1, game_3]


def test_get_collective_games(console, game_2, game_3):
    game_list = console.get_collective_games()
    assert game_list == [game_2, game_3]
