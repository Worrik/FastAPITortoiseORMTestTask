from typing import List
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends

from app.models.post import Post, PostInPydantic, PostPydantic
from app.services.login import manager

router = APIRouter(prefix="/posts")


@router.get("/")
async def get_posts() -> List[PostPydantic]:
    posts = await Post.all().prefetch_related('users_likes')
    return [PostPydantic.from_orm(post) for post in posts]


@router.get("/{id}")
async def get_post(id: int) -> PostPydantic:
    post = await Post.get(id=id)
    await post.fetch_related('users_likes')
    return await PostPydantic.from_tortoise_orm(post)


@router.post("/")
async def create_post(post: PostInPydantic) -> PostPydantic:
    if await Post.filter(title=post.title).exists():
        raise HTTPException(detail="Post already exists",
                            status_code=400)

    db_post = await Post.create(**post.dict())
    await db_post.fetch_related('users_likes')
    return PostPydantic.from_orm(db_post)


@router.put("/{id}/like")
async def like_post(id: int, user=Depends(manager)) -> PostPydantic:
    post = await Post.get(id=id)
    await post.users_likes.add(user)
    await post.fetch_related('users_likes')
    return await PostPydantic.from_tortoise_orm(post)


@router.put("/{id}/unlike")
async def unlike_post(id: int, user=Depends(manager)) -> PostPydantic:
    post = await Post.get(id=id)
    await post.users_likes.remove(user)
    await post.fetch_related('users_likes')
    return await PostPydantic.from_tortoise_orm(post)

@router.delete("/{id}")
async def delete_post(id: int) -> PostPydantic:
    post = await Post.get(id=id)
    await post.delete()
    return await PostPydantic.from_tortoise_orm(post)

