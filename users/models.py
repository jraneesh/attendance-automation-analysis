from sqlalchemy import Boolean, Column, String, Integer
from utils.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    password = Column(String)
    access_token = Column(String)
    refresh_token = Column(String)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)