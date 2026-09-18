from contextlib import asynccontextmanager
import logging

from DBConn import *
from security import *
from datetime import datetime, timedelta
from typing import List

from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, Body, Header
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app:FastAPI):
    db = SessionLocal()
    logger = logging.getLogger('uvicorn.error')
    logger.setLevel(logging.INFO)
    # u:users = db.query(users).first() # type: ignore
    # logger.info(u.budgets[0].budgetName)
    try:
        yield
    finally:
        pass

app = FastAPI(lifespan=lifespan) # type: ignore

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

#User
@app.post("/createUser")
def create_user(username: str = Body(), password: str = Body(), db: Session = Depends(get_db)):
    checkuser = db.query(users).filter(users.username == username).first()
    if checkuser: return "Username is already in use!"
    
    user = users()
    user.username = username
    user.password = get_password_hash(password)
    db.add(user)
    db.commit()

@app.get("/getUser")
def get_user(username: str = Header(), db: Session = Depends(get_db)):
    #Get the users information
    user = db.query(users).filter(users.username == username).first()
    if user:
        return user.userID
    return "No user found"

@app.post("/login")
def login(username: str = Body(), password: str = Body(), db: Session = Depends(get_db)):
    user = db.query(users).filter(users.username == username).first()
    if user and verify_password(password, user.password):
        #Continue the log in process
        #Calculate the datetime
        datenow = datetime.now()
        dateextend = timedelta(hours=1)
        dateend = datenow + dateextend
        #Create the session
        session = sessionLog()
        session.user = user.userID
        session.created = datenow.strftime("%d/%m/%Y, %H:%M:%S")
        session.ends = dateend.strftime("%d/%m/%Y, %H:%M:%S")
        
        db.add(session)
        db.commit()
        db.refresh(session)
        
        return [user.userID, session.session_key]
    else:
        return "No user found!";

@app.delete("/logout")
def logout(session:str = Body(), db: Session = Depends(get_db)):
    token = db.query(sessionLog).filter(sessionLog.session_key == session).first()
    if token:
        db.delete(token)
        db.commit()
    return "Session ended"


#Budget
@app.post("/createBudget")
def create_budget(budgetName: str = Body(), db: Session = Depends(get_db)):
    pass

@app.delete("/deleteBudget")
def remove_budget(budgetID: int = Header(), db: Session = Depends(get_db)):
    pass

@app.get("/getBudgetByID")
def get_budget_by_id(budgetID: int = Body(), db: Session = Depends(get_db)):
    pass

@app.post("/addItemBudget")
def add_item_to_budget(budgetID: int = Body(), items: List[int] = Body(), db: Session = Depends(get_db)):
    pass

@app.delete("/removeItemFromBudget")
def remove_item_from_budget(budgetID: int = Header(), itemID: int = Header(), db: Session = Depends(get_db)):
    pass

#Item