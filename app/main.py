from fastapi import FastAPI
from fastapi.param_functions import Depends
from tortoise.contrib.fastapi import register_tortoise
from app.routers import analitics, users, posts
from app.config.base import DATABASE_URL
from app.services.login import manager

app = FastAPI()

app.include_router(users.router, tags=["Users"])
app.include_router(
    posts.router,
    tags=["Posts"],
    dependencies=[Depends(manager)]
)
app.include_router(
    analitics.router,
    tags=["Analitics"]
)

register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

