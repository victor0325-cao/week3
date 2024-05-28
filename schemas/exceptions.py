from pydantic import BaseModel

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

__all__ = ['ServerError', 'AuthInvalid', 'ParamInvalid', 'HeaderInvalid', 'SignatureInvalid', "TimeIntervalIsTooLong", "EndTimeMustBeGreaterThanStartTime"]

class HttpError(BaseModel):
    code: int
    msg:  str

class Resp:
    @classmethod
    def error(self, http_error: HttpError):
        return JSONResponse(
            status_code = 400,
            content = http_error.dict(),
        )

    @classmethod
    def success(self, data={}):
        return JSONResponse(
            status_code=200,
            content={
                "data": data,
            }
        )

def make_error(code, msg):
    return HttpError(
        code = code,
        msg  = msg,
    )

class ServerError(Exception):
    msg_detail = ""

    def __init__(self, msg_d=""):
        ServerError.msg_detail = msg_d

    @staticmethod
    def handler(request, exc):
        return Resp.error(make_error(10000, f"ServerError {ServerError.msg_detail}"))

class AuthInvalid(Exception):
    msg_detail = ""

    def __init__(self, msg_d=""):
        AuthInvalid.msg_detail = msg_d

    @staticmethod
    def handler(request, exc):
        return Resp.error(make_error(10001, f"AuthInvalid {AuthInvalid.msg_detail}"))

class ParamInvalid(Exception):
    msg_detail = ""
    
    def __init__(self, msg_d=""):
        ParamInvalid.msg_detail = msg_d

    @staticmethod
    def handler(request, exc):
        return Resp.error(make_error(10002, f"ParamInvalid {ParamInvalid.msg_detail}"))

class HeaderInvalid(Exception):

    @staticmethod
    def handler(request, exc):
        return Resp.error(make_error(10003, "HeaderInvalid"))

class SignatureInvalid(Exception):
    
    @staticmethod
    def handler(request, exc):
        return Resp.error(make_error(10004, "SignatureInvalid"))

class TimeIntervalIsTooLong(Exception):

    @staticmethod
    def handler(request, exc):
        return Resp.error(make_error(10006, "TimeIntervalIsTooLong"))

class EndTimeMustBeGreaterThanStartTime(Exception):

    @staticmethod
    def handler(request, exc):
        return Resp.error(make_error(10005, "EndTimeMustBeGreaterThanStartTime"))


def include_app(app):
    all_classes = globals()

    for exception in __all__:
        exception_class = all_classes[exception]
        app.add_exception_handler(exception_class, exception_class.handler)


