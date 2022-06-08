import datetime
from typing import Optional
from fastapi import APIRouter
from tortoise.functions import Count

from app.models.like import Like
from app.utils.custom_db_functions import Date

router = APIRouter(prefix="/analitics")


@router.get("/")
async def get_analitics(
        date_from: Optional[datetime.date] = None,
        date_to: Optional[datetime.date] = None
):
    query = (Like.all()
                 .annotate(date=Date('created_at'),
                           count_likes=Count('id'))
                 .group_by('date'))
    if date_from:
        query = query.filter(date__gte=date_from)

    if date_to:
        query = query.filter(date__lte=date_to)

    return await query.values('date', 'count_likes')

