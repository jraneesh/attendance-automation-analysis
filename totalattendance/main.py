from sqlalchemy.orm import Session
from . import models,schemas
from .models import TotalAttendance as TD
from users.models import User
from utils.database import SessionLocal, engine
from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.responses import JSONResponse
from utils.token import decode_token
from utils.students import get_subjects,get_stats
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import and_
from dotenv import load_dotenv
import os,json

load_dotenv('./.env')
router = APIRouter()
models.Base.metadata.create_all(bind=engine)
auth_scheme = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def per(num,den):
    try:
        return round((num/den)*100,2)
    except:
        return 0

def getStudentAttd(db,data):
    student = db.query(TD).filter(and_(TD.student==data.id, TD.year==data.year, TD.dept==data.dept, TD.section==data.section)).first()
    if student is None:
        return JSONResponse(status_code=404,content={"msg":"Student not Found"})
    else:
        sub = get_subjects(data.dept,data.year,data.section)
        res = {"id":data.id,"class":str(data.year)+"/"+data.dept+"/"+data.section,"updated":student.updated.strftime("%Y-%m-%d"),"total_percent":round(student.percentage,2)}
        res[sub["S1"]] = per(student.s1,student.s1t)
        res[sub["S2"]] = per(student.s2,student.s2t)
        res[sub["S3"]] = per(student.s3,student.s3t)
        res[sub["S4"]] = per(student.s4,student.s4t)
        res[sub["S5"]] = per(student.s5,student.s5t)
        res[sub["S6"]] = per(student.s6,student.s6t)
        res[sub["S7"]] = per(student.s7,student.s7t)
        res[sub["S8"]] = per(student.s8,student.s8t)
        res[sub["S9"]] = per(student.s9,student.s9t)
        res[sub["SX"]] = per(student.sX,student.sXt)
        return json.dumps(res)


@router.post("/checkattendance", tags=["student"])
async def checkstudentattendance(data: schemas.Student, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Security(auth_scheme)):
    if token.credentials==os.environ["CHATRAH_KEY"]:
        return getStudentAttd(db,data)
    else:
        teacher_name = decode_token(token.credentials,'access_token')
        authorized = db.query(User).filter(User.name==teacher_name).first()
        if authorized is None:
            raise HTTPException(status_code=401, detail="Not Authorized")
        else:
            resp = getStudentAttd(db,data)
            return JSONResponse(status_code=200,content=json.loads(resp))


@router.post("/dailystats", tags=["administration"])
async def class_stats(data: schemas.Section, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Security(auth_scheme)):
    teacher_name = decode_token(token.credentials,'access_token')
    authorized = db.query(User).filter(User.name==teacher_name).first()
    if authorized is None:
        raise HTTPException(status_code=401, detail="Not Authorized")
    else:
        try:
            stats = get_stats(data.dept,data.year,data.section)
            return stats
        except Exception as e:
            raise HTTPException(status_code=500,detail="Processing Error")

@router.post("/classattendance",tags=["administration"])
async def class_attendance(data: schemas.Section, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Security(auth_scheme)):
    teacher_name = decode_token(token.credentials,'access_token')
    authorized = db.query(User).filter(User.name==teacher_name).first()
    if authorized is None:
        raise HTTPException(status_code=401, detail="Not Authorized")
    else:
        attd = db.query(TD).with_entities(TD.student,TD.percentage).filter(and_(TD.dept==data.dept,TD.year==data.year,TD.section==data.section)).all()
        if attd is None:
            raise HTTPException(status_code=406,detail="Processing Error")
        return dict(attd)

@router.post("/lowattendance/section",tags=["administration"])
async def low_attendance_by_section(data: schemas.Section, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Security(auth_scheme)):
    teacher_name = decode_token(token.credentials,'access_token')
    authorized = db.query(User).filter(User.name==teacher_name).first()
    if authorized is None:
        raise HTTPException(status_code=401, detail="Not Authorized")
    else:
        absentees = db.query(TD).with_entities(TD.student,TD.percentage).filter(and_(TD.dept==data.dept,TD.year==data.year,TD.section==data.section,TD.percentage<65)).all()
        if absentees is None:
            raise HTTPException(status_code=406,detail="Processing Error")
        return dict(absentees)

@router.post("/lowattendance/year",tags=["administration"])
async def low_attendance_by_year(data: schemas.Year, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Security(auth_scheme)):
    teacher_name = decode_token(token.credentials,'access_token')
    authorized = db.query(User).filter(User.name==teacher_name).first()
    if authorized is None:
        raise HTTPException(status_code=401, detail="Not Authorized")
    else:
        absentees = db.query(TD).with_entities(TD.student,TD.percentage).filter(and_(TD.dept==data.dept,TD.year==data.year,TD.percentage<65)).all()
        if absentees is None:
            raise HTTPException(status_code=406,detail="Processing Error")
        return dict(absentees)

@router.post("/lowattendance/dept",tags=["administration"])
async def low_attendance_by_dept(data: schemas.Dept, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Security(auth_scheme)):
    teacher_name = decode_token(token.credentials,'access_token')
    authorized = db.query(User).filter(User.name==teacher_name).first()
    if authorized is None:
        raise HTTPException(status_code=401, detail="Not Authorized")
    else:
        absentees = db.query(TD).with_entities(TD.student,TD.percentage).filter(and_(TD.dept==data.dept,TD.percentage<65)).all()
        if absentees is None:
            raise HTTPException(status_code=406,detail="Processing Error")
        return dict(absentees)