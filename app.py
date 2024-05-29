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
from fastapi.middleware.gzip import GZipMiddleware
#from pyutil.middleware.monitor import CloudWatchMetricsMiddleware

# 配置
from config import config
from schemas.exceptions import include_app

# route
from api import api_router

app = FastAPI()

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("app:app", port=3045, host="0.0.0.0")
