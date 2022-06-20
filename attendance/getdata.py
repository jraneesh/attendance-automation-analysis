from sqlalchemy.orm import Session
from . import models,schemas
from .models import TodayAttendance as TD
from users import models as um
from totalattendance.schemas import Section as Section
from utils.database import SessionLocal, engine
from fastapi import APIRouter, HTTPException, Depends, Security
from utils.token import decode_token
from utils.students import check_students
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import and_
from dotenv import load_dotenv
import os

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

@router.post("/attendance", tags=["attendance"])
async def getData(data: schemas.TodayAttendance, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Security(auth_scheme)):
    teacher_name = decode_token(token.credentials,'access_token')
    authorized = db.query(um.User).filter(um.User.name==teacher_name).first()
    if authorized is None:
        raise HTTPException(status_code=401, detail="Not Authorized")
    else:
        if authorized.name!=teacher_name:
            raise HTTPException(status_code=404,detail="User Error")
        else:
            if check_students(data.dept,data.year,data.section, data.attendance.keys()) is False:
                raise HTTPException(status_code=400, detail="Student data error")
            else:
                if data.pid == 1:
                    try:
                        for id, value in data.attendance.items():
                            exist_student = db.query(TD).filter(and_(TD.student==id, TD.year==data.year, TD.dept==data.dept, TD.section==data.section, TD.date==data.dt)).first()
                            if exist_student is None:
                                try:
                                    attendance = TD(student=id,year=data.year,dept=data.dept,section= data.section, date=data.dt,p1=value)
                                    db.add(attendance)
                                except:
                                    raise HTTPException(status_code=406,detail="Processing Error")
                            else:
                                exist_student.p1= value
                        db.commit()
                    except Exception as e:
                        print(e)
                        raise HTTPException(status_code=406,detail="Processing Error")
                elif data.pid == 2:
                    try:
                        for id, value in data.attendance.items():
                            exist_student = db.query(TD).filter(and_(TD.student==id, TD.year==data.year, TD.dept==data.dept, TD.section==data.section, TD.date==data.dt)).first()
                            if not exist_student:
                                raise HTTPException(status_code=500, detail="Student not found")
                            else:
                                exist_student.p2= value
                        db.commit()
                    except Exception as e:
                        raise HTTPException(status_code=406,detail="Processing Error")
                elif data.pid == 3:
                    try:
                        for id, value in data.attendance.items():
                            exist_student = db.query(TD).filter(and_(TD.student==id, TD.year==data.year, TD.dept==data.dept, TD.section==data.section, TD.date==data.dt)).first()
                            if not exist_student:
                                raise HTTPException(status_code=500, detail="Student not found")
                            else:
                                exist_student.p3= value
                        db.commit()
                    except:
                        raise HTTPException(status_code=406,detail="Processing Error")
                elif data.pid == 4:
                    try:
                        for id, value in data.attendance.items():
                            exist_student = db.query(TD).filter(and_(TD.student==id, TD.year==data.year, TD.dept==data.dept, TD.section==data.section, TD.date==data.dt)).first()
                            if not exist_student:
                                raise HTTPException(status_code=500, detail="Student not found")
                            else:
                                exist_student.p4= value
                        db.commit()
                    except:
                        raise HTTPException(status_code=406,detail="Processing Error")
                elif data.pid == 5:
                    try:
                        for id, value in data.attendance.items():
                            exist_student = db.query(TD).filter(and_(TD.student==id, TD.year==data.year, TD.dept==data.dept, TD.section==data.section, TD.date==data.dt)).first()
                            if not exist_student:
                                raise HTTPException(status_code=500, detail="Student not found")
                            else:
                                exist_student.p5= value
                        db.commit()
                    except:
                        raise HTTPException(status_code=406,detail="Processing Error")
                elif data.pid == 6:
                    try:
                        for id, value in data.attendance.items():
                            exist_student = db.query(TD).filter(and_(TD.student==id, TD.year==data.year, TD.dept==data.dept, TD.section==data.section, TD.date==data.dt)).first()
                            if not exist_student:
                                raise HTTPException(status_code=500, detail="Student not found")
                            else:
                                exist_student.p6= value
                        db.commit()
                    except:
                        raise HTTPException(status_code=406,detail="Processing Error")
                elif data.pid == 7:
                    try:
                        for id, value in data.attendance.items():
                            exist_student = db.query(TD).filter(and_(TD.student==id, TD.year==data.year, TD.dept==data.dept, TD.section==data.section, TD.date==data.dt)).first()
                            if not exist_student:
                                raise HTTPException(status_code=500, detail="Student not found")
                            else:
                                exist_student.p7= value
                        db.commit()
                    except:
                        raise HTTPException(status_code=406,detail="Processing Error")
                else:
                    raise HTTPException(status_code=400, detail="Period doesn't Exist")
    return  {"msg":"success"}

@router.post("/setmsg",tags=["attendance"])
async def setMSG(data: schemas.setMsg, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Security(auth_scheme)):
    if token.credentials!=os.environ["CHATRAH_KEY"]:
        raise HTTPException(status_code=401,detail="API Key error")
    else:
        student = db.query(TD).filter(and_(TD.student==data.sid, TD.year==data.year, TD.dept==data.dept, TD.section==data.section)).first()
        if student is None:
            raise HTTPException(status_code=404,detail="Student not Found")
        else:
            try:
                student.msg=data.msg
                db.commit()
                return {"msg": "Success"}
            except:
                raise HTTPException(status_code=406,detail="Unable to process")

@router.post("/leavereason",tags=["attendance"])
async def leave_reasons(data: Section, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Security(auth_scheme)):
    teacher_name = decode_token(token.credentials,'access_token')
    authorized = db.query(um.User).filter(um.User.name==teacher_name).first()
    if authorized is None:
        raise HTTPException(status_code=401, detail="Not Authorized")
    else:
        absentees = db.query(TD).with_entities(TD.student,TD.msg).filter(and_(TD.dept==data.dept,TD.year==data.year,TD.section==data.section,TD.p1==0)).all()
        if absentees is None:
            raise HTTPException(status_code=404,detail="Data not Available(Deleted at the End of Day)")
        return dict(absentees)