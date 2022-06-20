import json,os

def check_students(dept,year,section,ikeys):
    file_location = "./storage/"+dept+"/"+str(year)+"/"+section+"/students.txt"
    with open(file_location,'r') as f:
        temp = f.readlines()
    sList = [s.rstrip('\n') for s in temp]
    f.close()
    check = True
    for k in ikeys:
        if k not in sList:
            check = False
            return check
    return check

def get_subjects(dept,year,section):
    file_location = os.getcwd()+"/storage/"+dept+"/"+str(year)+"/"+section+"/subjects.json"
    f = open(file_location,'r')
    subjects = dict(json.loads(f.read()))
    f.close()
    return subjects

def get_timetable(dept,year,section,day):
    file_location = os.getcwd()+"/storage/"+dept+"/"+str(year)+"/"+section+"/timetable.json"
    f = open(file_location,'r')
    tt = dict(json.loads(f.read()))
    f.close()
    return tt[str(day)]

def get_stats(dept,year,section):
    file_location = os.getcwd()+"/storage/"+dept+"/"+str(year)+"/"+section+"/stats.json"
    f = open(file_location,'r')
    stats = dict(json.loads(f.read()))
    f.close()
    return stats