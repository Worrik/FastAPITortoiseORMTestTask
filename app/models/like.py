from tortoise import fields

from app.models.base import BaseModel


class Like(BaseModel):
    user_id = fields.ForeignKeyField('models.User', on_delete=fields.SET_NULL)
    post_id = fields.ForeignKeyField('models.Post', on_delete=fields.SET_NULL)

