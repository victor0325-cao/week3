import uuid
import datetime
import logging
import asyncio
import httpx

from typing import Union, Any
from fastapi import Request, Depends, HTTPException, APIRouter, Query

from config import config

from schemas.exceptions import ParamInvalid, AuthInvalid, ServerError
from schemas.alg import *

from api.auth import verify_secret

from . import utils

router = APIRouter(
    dependencies=[
        Depends(verify_secret),
    ]
)

@router.post("/logon", response_model=AdvisorFrom)
async def create_adviser(adviser: AdviserForm):
    await utils.AdvisorDAL.add()
    return AdviserForm()

@router.put("/info", response_model)
