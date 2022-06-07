from fastapi import APIRouter
from tortoise.functions import Count

from app.models.like import Like
from app.utils.custom_db_functions import Date

router = APIRouter(prefix="/analitics")


@router.get("/")
async def get_analitics():
    query = (Like.all()
                 .annotate(date=Date('created_at'),
                           count_likes=Count('id'))
                 .group_by('date'))
    return await query.values('date', 'count_likes')

