from tortoise import fields

from app.models.base import BaseModel


class Like(BaseModel):
    user = fields.ForeignKeyField(
        'models.User', on_delete=fields.CASCADE, related_name="likes",
    )
    post = fields.ForeignKeyField(
        'models.Post', on_delete=fields.CASCADE, related_name="users_likes",
    )

