from fastapi import APIRouter

from app.presentation.routers.v1.auth.router import router as auth_router
from app.presentation.routers.v1.servers.router import router as servers_router
from app.presentation.routers.v1.subscription.router import router as subscription_router
from app.presentation.routers.v1.users.router import router as users_router


router_v1 = APIRouter()
router_v1.include_router(auth_router, prefix="/auth", tags=["auth"])
router_v1.include_router(servers_router, prefix="/servers", tags=["servers"])
router_v1.include_router(subscription_router, prefix="/subscription", tags=["subscription"])
router_v1.include_router(users_router, prefix="/users", tags=["users"])
