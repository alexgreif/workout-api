from fastapi import APIRouter

from app.api.users import router as user_router
from app.api.exercises import router as exercise_router
from app.api.auth import router as auth_router


router = APIRouter()

router.include_router(user_router)
router.include_router(exercise_router)
router.include_router(auth_router)
