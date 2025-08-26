from fastapi import APIRouter
from .products.views import router as products_router
from .demo_auth.views import router as demo_auth_router
from .demo_auth.demo_jwt_auth import router as demo_auth_jwt_router

router = APIRouter()
router.include_router(demo_auth_jwt_router, prefix="/jwt", tags=["JWT"])
router.include_router(demo_auth_router, prefix="/auth", tags=["Demo Auth"])
router.include_router(products_router, prefix="/products")
