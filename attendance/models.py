from sqlalchemy import Boolean, Column, String, Integer, Date
from utils.database import Base

class TodayAttendance(Base):
    __tablename__ = "attendance"
    sno = Column(Integer, primary_key=True, index=True)
    student = Column(String)
    year = Column(Integer)
    dept = Column(String)
    date = Column(Date)
    section = Column(String)
    p1 = Column(Boolean, default=False)
    p2 = Column(Boolean, default=False)
    p3 = Column(Boolean, default=False)
    p4 = Column(Boolean, default=False)
    p5 = Column(Boolean, default=False)
    p6 = Column(Boolean, default=False)
    p7 = Column(Boolean, default=False)
    msg = Column(String)