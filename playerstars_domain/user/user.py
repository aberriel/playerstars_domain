from clapy_basic_classes import BasicValue
from marshmallow import fields, post_load
from playerstars_domain.utils import ImageSizeException
from sys import getsizeof


class User(BasicValue):
    def __init__(self,
                 name: str,
                 email: str,
                 date_birth,
                 street: str,
                 street_number: str,
                 street_complement: str,
                 neighborhood: str,
                 city: str,
                 state: str,
                 country: str,
                 postal_code: str,
                 phone_number: str,
                 cpf: str,
                 nickname: str,
                 profile_image: str = None):
        super(User, self).__init__()
        self.name = name
        self.email = email
        self.date_birth = date_birth
        self.street = street
        self.street_number = street_number
        self.street_complement = street_complement
        self.neighborhood = neighborhood
        self.city = city
        self.state = state
        self.country = country
        self.postal_code = postal_code
        self.phone_number = phone_number
        self.cpf = cpf
        self.nickname = nickname
        self.profile_image = profile_image

        image_size = getsizeof(self.profile_image) / 1024
        if image_size > 100:
            raise ImageSizeException()

    def __repr__(self):
        return f'{self.name},\n' \
            f'email: {self.email}, ' \
            f'nascimento: {self.date_birth.strftime("%d/%m/%Y")}' \
            f'\nEndereço: {self.street} {self.street_number}, ' \
            f'{self.street_complement} - {self.neighborhood}, ' \
            f'{self.city},\n{self.state} , {self.country} - ' \
            f'{self.postal_code}' \
            f'\nTelefone: {self.phone_number}'

    class Schema(BasicValue.Schema):
        date_birth = fields.Date(
            required=True,
            allow_none=False,
            format='iso')
        email = fields.Email(required=True, allow_none=False)
        name = fields.String(required=True, allow_none=False)
        street = fields.String(required=True, allow_none=False)
        street_number = fields.String(default=None, missing=None)
        street_complement = fields.String(default=None, missing=None)
        neighborhood = fields.String(required=True, allow_none=False)
        city = fields.String(required=True, allow_none=False)
        state = fields.String(required=True, many=False)
        country = fields.String(required=True, many=False)
        postal_code = fields.String(required=True, allow_none=False)
        phone_number = fields.String(required=True, allow_none=False)
        cpf = fields.String(required=True, allow_none=False)
        nickname = fields.String(required=True, allow_none=False)
        profile_image = fields.String(required=False, allow_none=True)

        @post_load
        def post_load(self, data, many, partial):
            return User(**data)
