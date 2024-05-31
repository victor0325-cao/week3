# 官方库
import os
import json
import time
import uuid
import logging
import datetime
import uvicorn
import asyncio
import binascii

# web框架
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

# 配置
from config import config
from schemas.exceptions import include_app

# route
from api import api_router

from pyutil.log.log import init as init_log, _request_id_ctx_var

app = FastAPI()

@app.middleware("http")
async def add_process_time(request: Request, call_next):
    start_time = time.time()
    logging.info(
        "Request: "
        f"{request.headers.get('x-forwarded-for', request.client.host)} - "
        f"{request.method} "
        f"{request.url.path} "
    )

    response = await call_next(request)

    logging.info(
        "Response: "
        f"{request.headers.get('x-forwarded-for', request.client.host)} - "
        f"{request.method} "
        f"{request.url.path} "
        f"{response.status_code} "
        f"{int((time.time() - start_time) * 1000)}ms"
    )

    return response

@app.middleware("http")
async def dispatch_request_id(request: Request, call_next):
    request_id = request.headers.get("x-request-id", f"{uuid.uuid4()}{int(time.time() * 1000)}")
    token = _request_id_ctx_var.set(request_id)
    response = await call_next(request)
    _request_id_ctx_var.reset(token)

    return response

app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    init_log(config.log)


@app.on_event("shutdown")
async def shutdown_event():
    pass

if __name__ == "__main__":
    uvicorn.run("app:app", port=3045, host="0.0.0.0")
