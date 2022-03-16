from playerstars_domain import UserAdmin
from pytest import raises, fixture
from tests.util import generic_serialize_roundtrip_test
from uuid import uuid4


@fixture
def user():
    return UserAdmin(name='Luan', email='luan.papai@stormsec.com.br')


def test_user_with_id():
    user_id = str(uuid4())
    user = UserAdmin(
        name='Anselmo Lira',
        email='anselmo.lira@stormsec.com.br',
        entity_id=user_id)
    assert user
    assert user.entity_id == user_id


def test_user_to_json(user):
    user_entity_id = user.entity_id
    assert user.to_json() == dict(
        entity_id=user_entity_id,
        name='Luan',
        email='luan.papai@stormsec.com.br')


def test_missing_value():
    with raises(TypeError) as excinfo:
        UserAdmin(name='Luxan')

    assert "missing 1 required positional argument: 'email'" in str(excinfo.value)


def test_extra_value():
    with raises(TypeError) as excinfo:
        UserAdmin(name='Anselmo', email='anselmo@gmail.com', alias='sesel')
    assert "unexpected keyword argument 'alias'" in str(excinfo.value)


def test_user_roundtrip(user):
    generic_serialize_roundtrip_test(UserAdmin, user)
