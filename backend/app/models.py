from sqlalchemy import (
    Column, Integer, String, DateTime, Time, ForeignKey
)
from sqlalchemy.orm import relationship

from app.database import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    price = Column(Integer, nullable=True)  # cents; optional

    appointments = relationship("Appointment", back_populates="service")


class Mechanic(Base):
    __tablename__ = "mechanics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    working_hours = relationship(
        "WorkingHours", back_populates="mechanic", cascade="all, delete-orphan"
    )
    appointments = relationship("Appointment", back_populates="mechanic")


class WorkingHours(Base):
    __tablename__ = "working_hours"

    id = Column(Integer, primary_key=True, index=True)
    mechanic_id = Column(Integer, ForeignKey("mechanics.id"), nullable=False)
    day_of_week = Column(Integer, nullable=False)  # 0 = Monday ... 6 = Sunday
    start_time = Column(Time, nullable=False)       # e.g. 09:00
    end_time = Column(Time, nullable=False)         # e.g. 17:00

    mechanic = relationship("Mechanic", back_populates="working_hours")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    mechanic_id = Column(Integer, ForeignKey("mechanics.id"), nullable=False)
    customer_name = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    service = relationship("Service", back_populates="appointments")
    mechanic = relationship("Mechanic", back_populates="appointments")