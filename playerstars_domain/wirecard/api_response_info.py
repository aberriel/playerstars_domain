from clapy_basic_classes import BasicValue
from marshmallow import fields, post_load
from typing import List


class InfoDetail(BasicValue):
    def __init__(self, code: str, description: str):
        self.code = code
        self.description = description

    class Schema(BasicValue.Schema):
        code = fields.String(required=True, allow_none=False)
        description = fields.String(required=True, allow_none=False)

        @post_load
        def post_load(self, data, many, partial):
            return InfoDetail(**data)


class ApiResponseInfo(BasicValue):
    def __init__(self,
                 message: str = None,
                 alerts: List[InfoDetail] = None,
                 errors: List[InfoDetail] = None):
        self.message = message
        self.alerts = alerts or []
        self.errors = errors or []

    class Schema(BasicValue.Schema):
        message = fields.String(required=False, allow_none=True)
        alerts = fields.Nested(
            InfoDetail.Schema,
            required=False,
            allow_none=True,
            many=True)
        errors = fields.Nested(
            InfoDetail.Schema,
            required=False,
            allow_none=True,
            many=True)

        @post_load
        def post_load(self, data, many, partial):
            return ApiResponseInfo(**data)
