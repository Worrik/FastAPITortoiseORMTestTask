from pypika.terms import CustomFunction
from tortoise.expressions import Function

class Date(Function):
    database_func = CustomFunction("DATE", ["date"])
