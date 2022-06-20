from pydantic import BaseModel
from datetime import date
from typing import Dict

class TodayAttendance(BaseModel):
    dt: date
    tid: int
    pid: int
    year: int
    dept: str
    section: str
    attendance: Dict[str,bool] 

    class Config:
        orm_mode = True

class setMsg(BaseModel):
    sid: str
    year: int
    dept: str
    section: str
    msg: str

    class Config:
        orm_mode = True