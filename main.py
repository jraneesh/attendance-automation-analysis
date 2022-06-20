from fastapi import FastAPI
from users import auth
from attendance import getdata
from totalattendance import main

app = FastAPI()
app.include_router(auth.router)
app.include_router(getdata.router)
app.include_router(main.router)

@app.get("/")
async def root():
    return {"message": "Attendance Automation Analysis API"}
