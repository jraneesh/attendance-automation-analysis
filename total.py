import json
import os
from totalattendance.models import TotalAttendance as TD
from attendance.models import TodayAttendance as today
from utils.database import SessionLocal, engine, Base
from utils.students import get_timetable
from sqlalchemy import and_
from datetime import datetime
from dateutil.tz import gettz
import pandas as pd

Base.metadata.create_all(bind=engine)
try:
    db = SessionLocal()
except:
    print("db opening error")

sections = ["A","B","C"]
depts = ["CSE","CIVIL","EEE","IT","ECE","MECH","EIE"]
years = [1,2,3,4]
dt = datetime.now(tz=gettz('Asia/Kolkata'))
export_data = []

def update_attendance(S,p):
    s_attendance = db.query(TD).filter(and_(TD.student==S.student,TD.dept==S.dept,TD.year==S.year,TD.section==S.section)).first()
    attd = list(map(int,[S.p1,S.p2,S.p3,S.p4,S.p5,S.p6,S.p7]))
    for i in range(7):
        if p[i]=="S1":
            s_attendance.s1 += attd[i]
            s_attendance.s1t+=1
        elif p[i]=="S2":
            s_attendance.s2 += attd[i]
            s_attendance.s2t+=1
        elif p[i]=="S3":
            s_attendance.s3 += attd[i]
            s_attendance.s3t+=1
        elif p[i]=="S4":
            #print(pi)
            s_attendance.s4 += attd[i]
            s_attendance.s4t+=1
        elif p[i]=="S5":
            s_attendance.s5 += attd[i]
            s_attendance.s5t+=1
        elif p[i]=="S6":
            s_attendance.s6 += attd[i]
            s_attendance.s6t+=1
        elif p[i]=="S7":
            s_attendance.s7 += attd[i]
            s_attendance.s7t+=1
        elif p[i]=="S8":
            s_attendance.s8 += attd[i]
            s_attendance.s8t+=1
        elif p[i]=="S9":
            s_attendance.s9 += attd[i]
            s_attendance.s9t+=1
        elif p[i]=="SX":
            s_attendance.sX += attd[i]
            s_attendance.sXt+=1
        else:
            pass
    s_attendance.percentage = ((s_attendance.s1+s_attendance.s2+s_attendance.s3+s_attendance.s4+s_attendance.s5+s_attendance.s6+s_attendance.s7+s_attendance.s8+s_attendance.s9+s_attendance.sX)/(s_attendance.s1t+s_attendance.s2t+s_attendance.s3t+s_attendance.s4t+s_attendance.s5t+s_attendance.s6t+s_attendance.s7t+s_attendance.s8t+s_attendance.s9t+s_attendance.sXt))*100
    s_attendance.updated = dt.date()
    db.commit()
    attd.insert(0,s_attendance.student)
    export_data.append(attd)
    return None

#update for all sections
#All Departments
#1-4 years
#A-C sections
#below one is only for testing
export_file = open(os.getcwd()+"/storage/CSE/3/B/"+dt.strftime("%Y_%m_%d")+"_data.csv",'a')
periods = get_timetable(depts[0],years[2],sections[1],dt.weekday())
TA = list(db.query(today).filter(and_(today.dept==depts[0],today.year==years[2],today.section==sections[1])).all())
for Student in TA:
    update_attendance(Student,periods)
export_df = pd.DataFrame(export_data)
export_df.to_csv(export_file, index=False, header=False)
db.close()
stats = {"count":0, "partial":[], "absent":[]}
for i,row in export_df.iterrows():
    sum = row[1:].sum()
    if sum==7:
        stats["count"]+=1
    elif sum==0:
        stats["absent"].append(row[0])
    else:
        stats["partial"].append(row[0])
json_file = os.getcwd()+"/storage/CSE/3/B/stats.json"
with open(json_file,'w') as f:
    f.write(json.dumps(stats))
    f.close()