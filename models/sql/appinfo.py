from mydatabase import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class AppInfo(Base):
    __tablename__ = "appinfo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
