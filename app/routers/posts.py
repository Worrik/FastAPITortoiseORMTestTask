from typing import List
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from app.models.like import Like

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


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostInPydantic) -> PostPydantic:
    if await Post.filter(title=post.title).exists():
        raise HTTPException(detail="Post already exists",
                            status_code=400)

    await Post.create(**post.dict())


@router.put("/{id}/like", status_code=status.HTTP_202_ACCEPTED)
async def like_post(id: int, user=Depends(manager)):
    post = await Post.get(id=id)
    if not await Like.filter(user=user, post=post).exists():
        await Like.create(user=user, post=post)


@router.put("/{id}/unlike", status_code=status.HTTP_202_ACCEPTED)
async def unlike_post(id: int, user=Depends(manager)):
    post = await Post.get(id=id)
    await Like.filter(user=user, post=post).delete()

@router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_post(id: int):
    post = await Post.get(id=id)
    await post.delete()

