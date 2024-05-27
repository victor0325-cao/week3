import jwt
import httpx
import json
import time
import datetime
import logging

from fastapi import Request, Security, Header, BackgroundTasks
from fastapi.security.api_key import APIKeyHeader

from config import config

from schemas.exceptions import AuthInvalid, SignatureInvalid

secret_header = APIKeyHeader(name="x-secret", auto_error=True)

async def verify_secret(secret: str = Security(secret_header)):
    if secret != config.app.secret:
        raise AuthInvalid
