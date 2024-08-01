from sqlalchemy import Text, Boolean, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from storage import database


class ReplyConfig(database.Base):
    __tablename__ = "reply"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, unique=True, autoincrement=True
    )
    group_id: Mapped[str] = mapped_column(Text, nullable=False)
    enable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    rate: Mapped[float] = mapped_column(Float, nullable=False, default=0)
