from tortoise import fields
from tortoise.contrib.pydantic.creator import pydantic_model_creator

from app.models.base import BaseModel


class Post(BaseModel):
    title = fields.CharField(max_length=255, unique=True, index=True)
    text = fields.TextField()
    users_likes = fields.ManyToManyField(
        "models.User", related_name="liked_posts", through="models.Like"
    )

    def likes(self) -> int:
        return len(self.users_likes)

    def __str__(self) -> str:
        return self.title

    class PydanticMeta:
        computed = ["likes"]
        exclude=("id", "created_at", "updated_at", "likes")


PostPydantic = pydantic_model_creator(Post, name="Post")
PostInPydantic = pydantic_model_creator(
    Post, name="PostIn", exclude_readonly=True
)

