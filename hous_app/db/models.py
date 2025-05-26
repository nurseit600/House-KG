from hous_app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Float, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from typing import Optional, List
from passlib.hash import bcrypt


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    username: Mapped[str] = mapped_column(String, nullable=True, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    tokens: Mapped[List["RefreshToken"]] = relationship("RefreshToken", back_populates="user",
                                                        cascade="all, delete-orphan")

    def set_passwords(self, password: str):
        self.password = bcrypt.hash(password)

    def check_password(self, password: str):
        return bcrypt.verify(password, self.password)

    def __str__(self):
        return f'{self.username}'


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    token: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="tokens")


class HouseFeatures(Base):
    __tablename__ = "house_features"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    area: Mapped[int] = mapped_column(Integer)
    year: Mapped[int] = mapped_column(Integer)
    garage: Mapped[int] = mapped_column(Integer)
    total_basement: Mapped[int] = mapped_column(Integer)
    bath: Mapped[int] = mapped_column(Integer)
    overall_quality: Mapped[int] = mapped_column(Integer)
    neighborhood: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    price: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
