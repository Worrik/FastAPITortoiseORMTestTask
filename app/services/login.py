from datetime import datetime
from fastapi_login import LoginManager
from app.config.base import SECRET
from app.models.user import User

manager = LoginManager(
    SECRET,
    "/login", 
    use_cookie=True,
)


@manager.user_loader()
async def load_user(user_id: int) -> User:
    user = await User.get(id=user_id)
    user.last_active = datetime.now()
    await user.save()
    return user

