from datetime import datetime
from mydatabase import Base
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    phone_number: Mapped[str] = mapped_column(String(10))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash:Mapped[str] = mapped_column(String(255))
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    market_opt: Mapped[bool] = mapped_column(Boolean, default=False)
    last_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)