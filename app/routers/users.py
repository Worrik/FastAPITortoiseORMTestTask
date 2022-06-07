from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from starlette.responses import Response

from app.models.user import Login, SuccesfulLogin, User, UserInPydantic
from app.services.login import manager

router = APIRouter(prefix="/user")


@router.post("/login")
async def login(response: Response, login: Login) -> SuccesfulLogin:
    """
    Login user
    """
    user = await User.get_or_none(email=login.email)

    if not user:
        raise HTTPException(detail="Incorrect email or password",
                            status_code=400)

    if not user.check_password(login.password):
        raise HTTPException(detail="Incorrect email or password",
                            status_code=400)

    access_token = manager.create_access_token(
        data={'sub': user.id}
    )
    manager.set_cookie(response, access_token)
    return SuccesfulLogin(access_token=access_token)


@router.post("/register")
async def register(response: Response, user: UserInPydantic) -> SuccesfulLogin:
    """
    Register user
    """
    if await User.filter(email=user.email).exists():
        raise HTTPException(detail="User already exists",
                            status_code=400)

    db_user = User(**user.dict())
    db_user.set_password(user.password)
    await db_user.save()

    access_token = manager.create_access_token(
        data={'sub': db_user.id}
    )
    manager.set_cookie(response, access_token)
    return SuccesfulLogin(access_token=access_token)

