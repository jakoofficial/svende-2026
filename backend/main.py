from contextlib import asynccontextmanager
import logging

from sqlalchemy import select

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
def get_user(token: str = Body(), username: str = Header(), db: Session = Depends(get_db)):
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
def create_budget(token: str = Body(), budgetName: str = Body(), members: List[int] = Body(), db: Session = Depends(get_db)):
    token_valid = db.query(sessionLog).filter(sessionLog.session_key == token).first()
    if token_valid:
        creator = db.query(users).filter(users.userID == token_valid.user).first()
        if budgetName and creator:
            newbudget = budgets()
            newbudget.budgetName = budgetName
            newbudget.creator = creator
            newbudget.created = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            newbudget.lastUpdated = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            newbudget.items = []
            
            db.add(newbudget)
            db.commit()
            
            return "Budget has been created"
        else:
            if not budgetName:
                return "Budgets can be unnamed!"
            return "Something went wrong. Try again"
    else:
        return "Valid token not found!"

@app.delete("/deleteBudget")
def remove_budget(token: str = Body(),budgetID: int = Header(), db: Session = Depends(get_db)):
    token_valid = db.query(sessionLog).filter(sessionLog.session_key == token).first()
    if token_valid:
        budget = db.query(budgets).filter(budgets.budgetID == budgetID).first()
        if budget:
            db.delete(budget)
            db.commit()
            return "Budget removed!"
        return "No budget found!"
    return "No valid token found"

@app.get("/getBudgetByID")
def get_budget_by_id(token: str = Header(), budgetID: int = Header(), db: Session = Depends(get_db)):
    token_valid = db.query(sessionLog).filter(sessionLog.session_key == token).first()
    if token_valid:
        budget = db.query(budgets).filter(budgets.budgetID == budgetID).first()
        if budget:
            return budget
        return "No budget found"
    return "no valid token found"

@app.post("/addItemBudget")
def add_item_to_budget(token: str = Body(),budgetID: int = Body(), items: List[int] = Body(), db: Session = Depends(get_db)):
    token_valid = db.query(sessionLog).filter(sessionLog.session_key == token).first()
    if token_valid:
        budget = db.query(budgets).filter(budgets.budgetID == budgetID).first()
        if budget:
            itemList = db.scalars(select(budgetItems).where(budgetItems.itemID.in_(items))).all()
            budget.items.extend(itemList)
            
            db.commit()
            db.refresh(budget)
            return budget.items
        return "No budget found"
    return "no token"

@app.delete("/removeItemFromBudget")
def remove_item_from_budget(token: str = Body(),budgetID: int = Header(), itemID: int = Header(), db: Session = Depends(get_db)):
    token_valid = db.query(sessionLog).filter(sessionLog.session_key == token).first()
    pass

#Group
@app.post("/createGroup")
def create_group(token: str = Body(),groupname: str = Body(), members: List[int] = Body(), db: Session = Depends(get_db)):
    token_valid = db.query(sessionLog).filter(sessionLog.session_key == token).first()
    pass

@app.put("/updateGroup")
def update_group(token: str = Body(),groupID: int = Body(), members: List[int] = Body(), db: Session = Depends(get_db)):
    token_valid = db.query(sessionLog).filter(sessionLog.session_key == token).first()
    pass

@app.delete("/removeGroup")
def remove_group(token: str = Body(),groupID: int = Header(), db: Session = Depends(get_db)):
    token_valid = db.query(sessionLog).filter(sessionLog.session_key == token).first()
    if token_valid:
        group_check = db.query(groups).filter(groups.groupID == groupID).first()
        if group_check:
            db.delete(group_check)
            db.commit()
            return "Group removed"
        return "No group was found"
    return "No valid token"

#Item
@app.post("/createItem")
def create_item(token: str = Body(),itemName: str = Body(), itemDesc: str = Body(), itemPrice: float = Body(), dateAdded: str = Body(), db: Session = Depends(get_db)):
    token_valid = db.query(sessionLog).filter(sessionLog.session_key == token).first()
    pass

@app.put("/updateItem")
def update_item(token: str = Body(),itemName: str = Body(), itemDesc: str = Body(), itemPrice: float = Body(), db: Session = Depends(get_db)):
    token_valid = db.query(sessionLog).filter(sessionLog.session_key == token).first()
    pass

@app.delete("/removeItem")
def remove_item(token: str = Body(),itemID: int = Header(), db: Session = Depends(get_db)):
    token_valid = db.query(sessionLog).filter(sessionLog.session_key == token).first()
    pass