from fastapi import APIRouter

from .order.views import router as order
from .users.views import router as users
from .advisor.views import router as advisor


api_router = APIRouter()

api_router.include_router(order, prefix="/order", tags=["order"])
api_router.include_router(users, prefix="/user", tags=["user"])
api_router.include_router(advisor, prefix="/advisor", tags=["advisor"])
