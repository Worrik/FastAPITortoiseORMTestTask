import datetime
import pydantic


class AnaliticsQuery(pydantic.BaseModel):
    """
    AnaliticsQuery
    """
    date_from: datetime.date
    date_to: datetime.date

