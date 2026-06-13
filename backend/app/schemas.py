from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, time


# ---------- Service ----------
class ServiceBase(BaseModel):
    name: str
    duration_minutes: int
    price: Optional[int] = None

class ServiceCreate(ServiceBase):
    pass

class ServiceResponse(ServiceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ---------- Mechanic ----------
class MechanicBase(BaseModel):
    name: str

class MechanicCreate(MechanicBase):
    pass

class MechanicResponse(MechanicBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ---------- WorkingHours ----------
class WorkingHoursBase(BaseModel):
    mechanic_id: int
    day_of_week: int          # 0 = Monday ... 6 = Sunday
    start_time: time          # "09:00:00"
    end_time: time            # "17:00:00"

class WorkingHoursCreate(WorkingHoursBase):
    pass

class WorkingHoursResponse(WorkingHoursBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ---------- Appointment ----------
class AppointmentBase(BaseModel):
    service_id: int
    mechanic_id: int
    customer_name: str

class AppointmentCreate(AppointmentBase):
    start_time: datetime      # client sends start; we compute end from service duration

class AppointmentResponse(AppointmentBase):
    id: int
    start_time: datetime
    end_time: datetime
    model_config = ConfigDict(from_attributes=True)


# ---------- Availability ----------
class AvailableSlot(BaseModel):
    start_time: datetime
    end_time: datetime