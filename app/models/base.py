import pydantic
from tortoise import fields, models

class BaseModel(models.Model):
    """
    An abstract base class model
    """
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class PydanticBaseModel(pydantic.BaseModel):
    """
    An abstract base class model for pydantic
    """
    id: int
    created_at: str
    updated_at: str

