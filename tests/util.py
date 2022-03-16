from playerstars_domain import (
    Console,
    Game,
    GamePoints,
    MemberStatus,
    MemberType,
    OperationType,
    Player,
    PlayerConsoles,
    PlayerStatus,
    SourceOperationType,
    StarTransaction,
    User,
    TeamMember)
from playerstars_domain.player.star_transaction import CoinType
from datetime import datetime, timezone, date


def generic_serialize_roundtrip_test(cls, obj):
    json_data = obj.to_json()
    loaded = cls.from_json(json_data)

    print('json_data: ' + str(json_data))
    print('loaded json: ' + str(loaded.to_json()))
    assert obj == loaded


transaction_1 = StarTransaction(
    value=8,
    source_id='84be0af2-e722-4c42-9b51-78a6d832908d',
    operation_type=OperationType.CREDIT,
    coin_type=CoinType.RED_STAR,
    source=SourceOperationType.FINANCIAL_TRANSACTION,
    operation_date=datetime(2019, 2, 3, 13, 21, 45, tzinfo=timezone.utc))
transaction_2 = StarTransaction(
    value=9,
    source_id='85d59fa9-dde5-4f46-98aa-9ad268c8a8d0',
    operation_type=OperationType.CREDIT,
    coin_type=CoinType.GOLDEN_STAR,
    source=SourceOperationType.FINANCIAL_TRANSACTION,
    operation_date=datetime(2019, 2, 3, 13, 43, 21, tzinfo=timezone.utc))
transaction_3 = StarTransaction(
    value=1,
    source_id='ef28f5e3-c99c-47a7-b0c5-c2cc4d55d975',
    operation_type=OperationType.DEBIT,
    coin_type=CoinType.GOLDEN_STAR,
    source=SourceOperationType.DUEL,
    operation_date=datetime(2019, 2, 4, 19, 2, 35, tzinfo=timezone.utc))
transaction_4 = StarTransaction(
    value=2,
    source_id='16ba80d0-950a-4ae1-ac97-e8e2775f77a4',
    operation_type=OperationType.CREDIT,
    coin_type=CoinType.RED_STAR,
    source=SourceOperationType.DUEL,
    operation_date=datetime(2019, 2, 4, 21, 12, 21, tzinfo=timezone.utc))
transaction_5 = StarTransaction(
    value=5,
    source_id='a14e88c8-bd77-4c7b-9e74-26588bbcf4cd',
    operation_type=OperationType.DEBIT,
    coin_type=CoinType.RED_STAR,
    source=SourceOperationType.TEAM_DUEL,
    operation_date=datetime(2019, 2, 7, 7, 15, 2, tzinfo=timezone.utc))
transaction_6 = StarTransaction(
    value=1,
    source_id='53a36c3d-091b-4855-8fa1-1c13ada7941b',
    operation_type=OperationType.DEBIT,
    coin_type=CoinType.GOLDEN_STAR,
    source=SourceOperationType.FINANCIAL_TRANSACTION,
    operation_date=datetime(2019, 2, 15, 9, 11, 51, tzinfo=timezone.utc))

star_transaction_list = [
    transaction_1, transaction_2, transaction_3,
    transaction_4, transaction_5, transaction_6]


def star_transaction_list_json():
    json_result = []
    for star_transaction in star_transaction_list:
        transaction_json = star_transaction.to_json()
        json_result.append(transaction_json)
    return json_result


def game_list():
    game_1 = Game(entity_id='3c8fffe3-b137-4a16-bdea-4d942d08d979',
                  name='Need for Speed',
                  logo_path='/images/nfs.jpg')
    game_2 = Game(entity_id='8ba3af50-6506-462e-b941-389e2a85f1eb',
                  name='Fifa 19',
                  logo_path='/images/fifa19.jog')
    game_3 = Game(entity_id='9f6ba271-6b48-4365-9175-f8c473948ff2',
                  name='Fortnite',
                  logo_path='images/fortnite.jpg')
    game_4 = Game(entity_id='47f82c44-cdbc-42a6-8afc-fe31937a34e0',
                  name='CS Go',
                  logo_path='/images/csgo.jpg')
    game_5 = Game(entity_id='bdbc658d-8850-41e5-9df8-e6e461f6eba6',
                  name='Fifa 18',
                  logo_path='/images/fifa18.jpg')
    game_list_ = [game_1, game_2, game_3, game_4, game_5]
    return game_list_


def gamepoints():
    _gamepoints = []
    for game in game_list():
        _gamepoints.append(GamePoints(game.entity_id, 0))
    return _gamepoints


def console_list():
    con_1 = Console(
        entity_id='308995bd-6c03-4a60-be06-c599df86a384',
        name='Xbox One',
        logo_path='/images/xbox_one.jpg',
        tag_name='nick#1',
        games=game_list())
    con_2 = Console(
        entity_id='b71cc315-516a-4fcd-a1be-f26d251a96be',
        name='Nintendo Switch',
        logo_path='/images/n_switch.jpg',
        tag_name='nick#2',
        games=game_list())
    con_3 = Console(
        entity_id='eee9f78c-f89c-4e28-a8cd-969521dbfe9f',
        name='Playstation 4',
        logo_path='/images/ps4.jpg',
        tag_name='nick#3',
        games=game_list())
    con_4 = Console(
        entity_id='2b1b0626-eb8c-4141-ae76-72373584d984',
        name='Playstation 3',
        logo_path='/images/ps3.jpg',
        tag_name='nick#4',
        games=game_list())

    return [
        PlayerConsoles(con_1.entity_id, 'oie', gamepoints()),
        PlayerConsoles(con_2.entity_id, None, gamepoints()),
        PlayerConsoles(con_3.entity_id, None, gamepoints()),
        PlayerConsoles(con_4.entity_id, None, gamepoints())]


def console_list_json():
    return [x.to_json() for x in console_list()]


def user_data():
    return User(
        name='Anselmo Lira',
        email='anselmo.lira@stormsec.com.br',
        date_birth=date(1986, 12, 16),
        street='Avenida Brasil',
        street_number='500',
        street_complement='apt 607',
        neighborhood='pechinchão',
        city='Rio de Janeiro',
        state='Rio de Janeiro',
        country='Brasil',
        postal_code='25525-001',
        phone_number='(21) 2222-3333',
        cpf='123.456.789-01',
        nickname='zyzukab'
    )


player_without_consoles = Player(
    entity_id='d3da6fb9-d9d6-4fd2-b33a-adbd7435d4aa',
    user=user_data(), consoles=[], star_reservations=[])


player_with_consoles = Player(
    entity_id='1848b60b-7707-40b6-9e15-42c7198f103a',
    user=user_data(), consoles=console_list(), star_reservations=[])


player_with_star_transactions = Player(
    entity_id='2a50ec44-0ced-4b9a-94a9-64d7c90fb8bd',
    user=user_data(), consoles=console_list(),
    star_transactions=star_transaction_list, terms=True,
    red_star_balance=5, golden_star_balance=7, star_reservations=[])


def favorite_list():
    user_1 = User(name='Felipe Duarte',
                  email='f.duarte@stormsec',
                  date_birth=date(1990, 6, 5),
                  street='Avenida Brasil',
                  street_number='500',
                  street_complement='apt 607',
                  neighborhood='pechinchão',
                  city='Rio de Janeiro',
                  state='Rio de Janeiro',
                  country='Brasil',
                  postal_code='25520-012',
                  phone_number='(21) 98144-1317',
                  cpf='123.456.789-01',
                  nickname='zyzukab')
    player_1 = Player(user=user_1,
                      consoles=console_list(),
                      red_star_balance=0,
                      golden_star_balance=0,
                      player_status=PlayerStatus.OFFLINE,
                      star_reservations=[])

    user_2 = User(name='Luan Garcia',
                  email='luan.garcia@stormsec',
                  date_birth=date(1988, 12, 25),
                  street='Avenida Brasil',
                  street_number='500',
                  street_complement='apt 607',
                  neighborhood='pechinchão',
                  city='Rio de Janeiro',
                  state='Rio de Janeiro',
                  country='Brasil',
                  postal_code='23335-115',
                  phone_number='(21) 99155-2323',
                  cpf='123.456.789-01',
                  nickname='zyzukab')
    player_2 = Player(user=user_2,
                      consoles=console_list(),
                      red_star_balance=0,
                      golden_star_balance=0,
                      player_status=PlayerStatus.OFFLINE)

    user_3 = User(name='Rogério da Silva',
                  email='r.silva@stormsec',
                  date_birth=date(1994, 12, 12),
                  street='Avenida Brasil',
                  street_number='500',
                  street_complement='apt 607',
                  neighborhood='pechinchão',
                  city='Rio de Janeiro',
                  state='Rio de Janeiro',
                  country='Brasil',
                  postal_code='22666-171',
                  phone_number='98666-0171',
                  cpf='123.456.789-01',
                  nickname='zyzukab')
    player_3 = Player(user=user_3,
                      consoles=console_list(),
                      red_star_balance=0,
                      golden_star_balance=0,
                      player_status=PlayerStatus.OFFLINE,
                      star_reservations=[])
    player_id_list = [
        player_1.entity_id,
        player_2.entity_id,
        player_3.entity_id]
    return player_id_list


def player_1():
    user = User(name='Felipe Duarte',
                email='felipe.duarte@stormsec.com.br',
                date_birth=date(1990, 6, 5),
                street='Avenida Brasil',
                street_number='500',
                street_complement='apt 607',
                neighborhood='pechinchão',
                city='Rio de Janeiro',
                state='Rio de Janeiro',
                country='Brasil',
                postal_code='25520-012',
                phone_number='(21) 98144-1317',
                cpf='123.456.789-01',
                nickname='felipao')
    player = Player(entity_id='a1b2c3',
                    user=user,
                    consoles=console_list(),
                    red_star_balance=150,
                    golden_star_balance=150,
                    player_status=PlayerStatus.AVAILABLE)
    return player


def player_2():
    user = User(name='Luan Garcia',
                email='luan.garcia@stormsec.com.br',
                date_birth=date(1988, 12, 25),
                street='Avenida Brasil',
                street_number='500',
                street_complement='apt 607',
                neighborhood='pechinchão',
                city='Rio de Janeiro',
                state='Rio de Janeiro',
                country='Brasil',
                postal_code='23335-115',
                phone_number='(21) 99155-2323',
                cpf='123.456.789-01',
                nickname='chefao')
    player = Player(entity_id='q1w2e3',
                    user=user,
                    consoles=console_list(),
                    red_star_balance=400,
                    golden_star_balance=400,
                    player_status=PlayerStatus.AVAILABLE)
    return player


def player_3():
    user = User(name='Rogério da Silva',
                email='rogerio.silva@stormsec.com.br',
                date_birth=date(1994, 12, 12),
                street='Avenida Brasil',
                street_number='500',
                street_complement='apt 607',
                neighborhood='pechinchão',
                city='Rio de Janeiro',
                state='Rio de Janeiro',
                country='Brasil',
                postal_code='22666-171',
                phone_number='98666-0171',
                cpf='123.456.789-01',
                nickname='rogerinho')
    player = Player(entity_id='abc123',
                    user=user,
                    consoles=console_list(),
                    red_star_balance=200,
                    golden_star_balance=200,
                    player_status=PlayerStatus.AVAILABLE)
    return player


def player_4():
    user = User(name='Anselmo Lira',
                email='a.lira@stormsec.com.br',
                date_birth=date(1986, 12, 16),
                street='Avenida Brasil',
                street_number='500',
                street_complement='apt 607',
                neighborhood='pechinchão',
                city='Rio de Janeiro',
                state='Rio de Janeiro',
                country='Brasil',
                postal_code='25525-001',
                phone_number='(21) 2222-3333',
                cpf='123.456.789-01',
                nickname='zyzukab')
    player = Player(entity_id='rrtt22',
                    user=user,
                    consoles=console_list(),
                    red_star_balance=180,
                    golden_star_balance=180,
                    player_status=PlayerStatus.AVAILABLE)
    return player


def player_5():
    user = User(name='Luciano',
                email='luciano@stormgroup.com.br',
                date_birth=date(1990, 1, 1),
                street='Rua José de Figueiredo',
                street_number='320',
                street_complement='Unidades 29 e 30',
                neighborhood='Barra da Tijuca',
                city='Rio de Janeiro',
                state='Rio de Janeiro',
                country='Brasil',
                postal_code='25525-001',
                phone_number='(21) 2211-3344',
                cpf='123.456.789-02',
                nickname='lulu')
    player = Player(entity_id='2r3t4g',
                    user=user,
                    consoles=console_list(),
                    red_star_balance=411,
                    golden_star_balance=72,
                    player_status=PlayerStatus.BUSY)
    return player


def player_6():
    user = User(name='Thiago',
                email='thiago@stormgroup.com.br',
                date_birth=date(1970, 3, 1),
                street='Rua José de Figueiredo',
                street_number='320',
                street_complement='Unidades 29 e 30',
                neighborhood='Barra da Tijuca',
                city='Rio de Janeiro',
                state='Rio de Janeiro',
                country='Brasil',
                postal_code='25525-001',
                phone_number='(21) 2213-3345',
                cpf='123.456.789-03',
                nickname='thiagao')
    player = Player(entity_id='fkkg62',
                    user=user,
                    consoles=console_list(),
                    red_star_balance=811,
                    golden_star_balance=272,
                    player_status=PlayerStatus.BUSY)
    return player


def captain():
    return TeamMember(
        player_id=player_1().entity_id,
        status=MemberStatus.ACCEPTED,
        member_type=MemberType.CAPTAIN)


def member_list_with_2():
    member_1 = TeamMember(
        player_id=player_2().entity_id,
        member_type=MemberType.MEMBER,
        status=MemberStatus.INVITED)

    member_2 = TeamMember(
        player_id=player_3().entity_id,
        member_type=MemberType.MEMBER,
        status=MemberStatus.INVITED)

    return [member_1, member_2]
