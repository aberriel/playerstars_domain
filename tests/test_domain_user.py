from datetime import date
from playerstars_domain import User
from playerstars_domain.utils import ImageSizeException
from pytest import raises, fixture
from random import choice
from string import ascii_letters, digits


@fixture
def user():
    return User(name='Luan',
                email='luan.papai@stormsec.com.br',
                street='Avenida Brasil',
                street_number='500',
                street_complement='apt 607',
                neighborhood='pechinchão',
                city='Rio de Janeiro',
                date_birth=date(1990, 1, 1),
                state='Rio de Janeiro',
                country='Brasil',
                postal_code='90210',
                phone_number='5521992536475',
                cpf='123.456.789-01',
                nickname='zyzukab',
                profile_image='aaaaaaaaaaaaaaaaaaa')


def test_user_with_id():
    user = User(name='Anselmo Lira',
                email='anselmo.lira@stormsec.com.br',
                street='Avenida Brasil',
                street_number='500',
                street_complement='apt 607',
                neighborhood='pechinchão',
                city='Hogwarts',
                date_birth=date(1986, 12, 16),
                state='Dartmoor',
                country='England',
                postal_code='634',
                phone_number='5521991996565',
                cpf='123.456.789-01',
                nickname='zyzukab',
                profile_image='aaaaaaaaaaaaaaaaaaa')
    assert user


def test_user_profile_image_length_limit():
    encoded_image = ''.join(choice(ascii_letters + digits) for i in range(110000))
    with raises(ImageSizeException):
        User(name='Luan',
             email='luan.papai@stormsec.com.br',
             street='Avenida Brasil',
             street_number='500',
             street_complement='apt 607',
             neighborhood='pechinchão',
             city='Rio de Janeiro',
             date_birth=date(1990, 1, 1),
             state='Rio de Janeiro',
             country='Brasil',
             postal_code='90210',
             phone_number='5521992536475',
             cpf='123.456.789-01',
             nickname='zyzukab',
             profile_image=encoded_image)


def test_user_repr(user):
    resp = """Luan,
email: luan.papai@stormsec.com.br, nascimento: 01/01/1990
Endereço: Avenida Brasil 500, apt 607 - pechinchão, Rio de Janeiro,
Rio de Janeiro , Brasil - 90210
Telefone: 5521992536475"""
    assert str(user) == resp


def test_user_to_json(user):
    assert user.to_json() == dict(
        name='Luan',
        email='luan.papai@stormsec.com.br',
        street='Avenida Brasil',
        street_number='500',
        street_complement='apt 607',
        neighborhood='pechinchão',
        city='Rio de Janeiro',
        date_birth="1990-01-01",
        state='Rio de Janeiro',
        country='Brasil',
        postal_code='90210',
        phone_number='5521992536475',
        cpf='123.456.789-01',
        nickname='zyzukab',
        profile_image='aaaaaaaaaaaaaaaaaaa')


def test_missing_value():
    with raises(TypeError) as excinfo:
        User(name='Luan',
             street='Avenida Brasil',
             street_number='500',
             street_complement='apt 607',
             neighborhood='pechinchão',
             city='Rio de Janeiro',
             date_birth=date(1990, 1, 1),
             state='Rio de Janeiro',
             country='Brasil',
             postal_code='90210',
             phone_number='5521992536475',
             cpf='123.456.789-01',
             nickname='zyzukab',
             profile_image='aaaaaaaaaaaaaaaaaaa')

    assert "missing 1 required positional argument: 'email'" in str(excinfo.value)


def test_extra_value():
    with raises(TypeError) as excinfo:
        User(name='Luan',
             street='Avenida Brasil',
             street_number='500',
             street_complement='apt 607',
             neighborhood='pechinchão',
             city='Rio de Janeiro',
             date_birth=date(1990, 1, 1),
             state='Rio de Janeiro',
             country='Brasil',
             postal_code='90210',
             alias='lulu',
             phone_number='5521992536475',
             cpf='123.456.789-01',
             nickname='zyzukab',
             profile_image='aaaaaaaaaaaaaaaaaaa')

    assert "unexpected keyword argument 'alias'" in str(excinfo.value)
