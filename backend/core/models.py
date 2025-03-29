from core.app import db
from sqlalchemy import BigInteger, Integer, String, DateTime, ForeignKey, Boolean
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column


class Tower(db.Model):
    __tablename__ = 'towers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit: Mapped[str] = mapped_column(String(10), nullable=False)
    floors: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(20), 
                                        nullable=False,
                                        default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(), 
        nullable=False,
        default=lambda: datetime.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(), 
        nullable=False,
        default=lambda: datetime.now(),
        onupdate=lambda: datetime.now())


class Apartment(db.Model):
    __tablename__ = 'apartments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    floor: Mapped[int] = mapped_column(Integer, nullable=False)
    tower_id: Mapped[int] = mapped_column(Integer, ForeignKey('towers.id'))
    unit: Mapped[str] = mapped_column(String(30), nullable=False)
    status: Mapped[str] = mapped_column(String(20), 
                                        nullable=False,
                                        default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(), 
        nullable=False,
        default=lambda: datetime.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(), 
        nullable=False,
        default=lambda: datetime.now(),
        onupdate=lambda: datetime.now())


class Vehicle(db.Model):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    plate: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    apartment_id: Mapped[int] = mapped_column(Integer, ForeignKey('apartments.id'))
    description: Mapped[str] = mapped_column(String(450), nullable=True)
    status: Mapped[str] = mapped_column(String(20), 
                                        nullable=False,
                                        default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(), 
        nullable=False,
        default=lambda: datetime.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(), 
        nullable=False,
        default=lambda: datetime.now(),
        onupdate=lambda: datetime.now())


class Entry(db.Model):
    __tablename__ = 'entries'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    plate: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    apartment_id: Mapped[int] = mapped_column(Integer, ForeignKey('apartments.id'))
    is_owner: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    description: Mapped[str] = mapped_column(String(450), nullable=True)
    status: Mapped[str] = mapped_column(String(20), 
                                        nullable=False,
                                        default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(), 
        nullable=False,
        default=lambda: datetime.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(), 
        nullable=False,
        default=lambda: datetime.now(),
        onupdate=lambda: datetime.now())
