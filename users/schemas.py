from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    password: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    token: str

class UserLogin(BaseModel):
    id : int
    password: str

class AuthToken(BaseModel):
    id: int
    access_token: str
    refresh_token: str
