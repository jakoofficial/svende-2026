from contextlib import asynccontextmanager
import logging

from DBConn import *
from security import *

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
def get_user(username: str = Body(), db: Session = Depends(get_db)):
    #Get the users information
    pass

@app.post("/login")
def login(username: str = Body(), password: str = Body(), db: Session = Depends(get_db)):
    user = db.query(users).filter(users.username == username).first()
    if verify_password(password, user.password):
        #Continue the log in process
        pass

@app.post("/createBudget")
def create_budget(budgetName: str = Body(), db: Session = Depends(get_db)):
    pass
