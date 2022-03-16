from .address import Address
from .billing_info import BillingInfo
from clapy_basic_classes import BasicValue
from datetime import date
from marshmallow import fields, post_load


class Subscriber(BasicValue):
    def __init__(self,
                 code: str,
                 id: str = None,
                 email: str = None,
                 fullname: str = None,
                 cpf: str = None,
                 phone_area_code: str = None,
                 phone_number: str = None,
                 address: Address = None,
                 billing_info: BillingInfo = None,
                 birthdate_day: int = None,
                 birthdate_month: str = None,
                 birthdate_year: int = None,
                 birthdate: date = None,
                 creation_date: str = None,
                 creation_time: str = None,
                 document: str = None,
                 document_type: str = None):
        super(Subscriber, self).__init__()
        self.id = id
        self.code = code
        self.email = email
        self.fullname = fullname
        self.cpf = cpf
        self.phone_area_code = phone_area_code
        self.phone_number = phone_number
        self.birthdate_day = int(birthdate_day) \
            if birthdate_day is not None else None
        self.birthdate_month = str(birthdate_month) \
            if birthdate_month is not None else None
        self.birthdate_year = int(birthdate_year) \
            if birthdate_year is not None else None
        self.address = address
        self.document_type = document_type
        self.document = document
        self.billing_info = billing_info
        self.creation_date = creation_date

        if birthdate is not None:
            self.birthdate_day = str(birthdate.day)
            self.birthdate_month = str(birthdate.month)
            self.birthdate_year = str(birthdate.year)

        if document is not None and document_type is not None \
           and document_type == 'CPF':
            self.cpf = document

    @classmethod
    def object_name(cls):
        return 'customers'

    @classmethod
    def post_params(cls, new_vault=True):
        return {
            'new_vault': str(new_vault).lower()
        }

    @classmethod
    def post_put_returns_object(cls):
        return False

    def prepate_to_update_customer(self):
        self.id = None

    class Schema(BasicValue.Schema):
        id = fields.String(required=False, allow_none=True)
        code = fields.String(required=True, allow_none=False)
        email = fields.String(required=False, allow_none=True)
        fullname = fields.String(required=False, allow_none=True)
        cpf = fields.String(required=False, allow_none=True)
        phone_area_code = fields.String(required=False, allow_none=True)
        phone_number = fields.String(required=False, allow_none=True)
        birthdate_day = fields.Integer(required=False, allow_none=True)
        birthdate_month = fields.String(required=False, allow_none=True)
        birthdate_year = fields.Integer(required=False, allow_none=True)
        address = fields.Nested(
            Address.Schema,
            required=False,
            allow_none=True)
        billing_info = fields.Nested(
            BillingInfo.Schema,
            required=False,
            allow_none=True)
        document = fields.String(required=False, allow_none=True)
        document_type = fields.String(required=False, allow_none=True)
        creation_date = fields.String(required=False, allow_none=True)
        creation_time = fields.String(required=False, allow_none=True)

        @post_load
        def post_load(self, data, many, partial):
            return Subscriber(**data)
