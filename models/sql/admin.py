from mydatabase import Base

from datetime import datetime

from sqlalchemy import String,DateTime

from sqlalchemy.orm import Mapped,mapped_column

class Admin(Base):

    __tablename__="admin"

    id:Mapped[str] = mapped_column(String(255),primary_key=True)
    name:Mapped[str] = mapped_column(String(30))
    phone_number: Mapped[str] = mapped_column(String(10))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash:Mapped[str] = mapped_column(String(255))
    last_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)