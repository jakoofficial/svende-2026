from sqlalchemy import Boolean, String, Integer, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
import uuid

engine = create_engine("mysql+pymysql://root:admin@mysql:3306/tracky", echo=True)

class Base(DeclarativeBase):
    pass

# Table
class test(Base):
    __tablename__ = "test"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

class users(Base):
    __tablename__ = "users"

    userID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(60))
    password: Mapped[str] = mapped_column(String(60))

class budgets(Base):
    __tablename__ = "budgets"

    budgetID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

class userBudget(Base):
    __tablename__ = "userBudget"
    userID: Mapped[int] = mapped_column(ForeignKey("users.userID"))
    budgetID: Mapped[int] = mapped_column(ForeignKey("budgets.budgetID"))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creating the db
Base.metadata.create_all(bind = engine)