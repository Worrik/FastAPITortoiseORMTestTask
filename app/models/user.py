import pydantic
from tortoise import fields
from tortoise.contrib.pydantic.creator import pydantic_model_creator

import crypt

from app.models.base import BaseModel


class User(BaseModel):
    """
    User model
    """
    first_name = fields.CharField(max_length=100)
    last_name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=128)

    last_login = fields.DatetimeField(null=True)
    last_active = fields.DatetimeField(null=True)

    liked_posts: fields.ReverseRelation

    def check_password(self, password):
        """
        Check if password is correct
        """
        return crypt.crypt(
            password,
            self.password
        ) == self.password

    def set_password(self, password):
        """
        Set password
        """
        self.password = crypt.crypt(password, crypt.METHOD_MD5)

    class Meta:
        table = "users"

UserPydantic = pydantic_model_creator(User, name="User", exclude=("password",))
UserInPydantic = pydantic_model_creator(
    User, name="UserIn",
    exclude=("id", "last_login", "last_active", "created_at", "updated_at"),
)


class Login(pydantic.BaseModel):
    email: str
    password: str


class SuccesfulLogin(pydantic.BaseModel):
    access_token: str

