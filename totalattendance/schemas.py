from pydantic import BaseModel

class Dept(BaseModel):
    dept : str

    class Config:
        orm_mode = True

class Year(Dept):
    year: int

class Section(Year):
    section: str

class Student(Section):
    id: str