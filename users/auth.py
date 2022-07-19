from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from . import models, schemas
from utils.database import SessionLocal, engine
from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from dotenv import load_dotenv
from utils import token

load_dotenv('./.env')
router = APIRouter()
models.Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users",  tags=["users"])
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    current_user = db.query(models.User).filter(models.User.name == user.name).first()
    if current_user:
        raise HTTPException(status_code=400, detail="User already registered")
    else:
        hashed_password = pwd_context.hash(user.password)
        db_user = models.User(name=user.name, password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"message": "User Added, please Verify with the Operator"}


@router.post("/login", response_model=schemas.AuthToken, tags=["users"])
async def read_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    current_user = db.query(models.User).filter(models.User.id == user.id).first()
    if current_user is not None:
        if pwd_context.verify(user.password, current_user.password) is True:
            current_user.access_token = token.encode_token(0,18,current_user.name,'access_token')
            current_user.refresh_token = token.encode_token(7,0,current_user.id,'refresh_token')
            db.commit()
            return { "id":current_user.id, "access_token": current_user.access_token, "refresh_token": current_user.refresh_token }
        else:
            raise HTTPException(status_code=401, detail="Authentication Error")
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.post('/refreshToken', tags=["users"])
async def refresh(user: schemas.UserLogin, db: Session = Depends(get_db) ):
    try:
        id = token.decode_token(user.password,'refresh_token')
        if id != user.id:
            return JSONResponse(content={"response":"Unathenticated Request"})
        current_user = db.query(models.User).filter(models.User.id == id).first()
        if current_user is None or current_user.refresh_token!=user.password:
            return JSONResponse(content={"response":"Unathenticated Request"})
        current_user.access_token = token.encode_token(0,18,current_user.name,'access_token')
        db.commit()
        return { "id":current_user.id, "access_token": current_user.access_token, "refresh_token": current_user.refresh_token }
    except Exception as e:
        raise HTTPException(status_code=401,detail="Unauthorized request")


@router.post('/validToken', tags=["users"])
async def validity(user: schemas.Token, db: Session = Depends(get_db) ):
    try:
        name = token.decode_token(user.token,'access_token')
        current_user = db.query(models.User).filter(models.User.name == name).first()
        if current_user is None or current_user.access_token!=user.token:
            return JSONResponse(status_code=404,content={"response":"Invalid Token"})
        return JSONResponse(status_code=200, content={"response":"Valid Token"})
    except Exception as e:
        raise HTTPException(status_code=401,detail="Unauthorized request")

