from sqlalchemy import Boolean, String, Integer, DateTime, Float, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
import uuid

engine = create_engine("mysql+pymysql://root:admin@mysql:3306/tracky", echo=True)

class Base(DeclarativeBase):
    pass

# Table creations
class users(Base):
    __tablename__ = "Users"

    userID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(60))
    password: Mapped[str] = mapped_column(String(255))
    budgets: Mapped[list["budgets"]] = relationship(back_populates="creator")
    groups: Mapped[list["groups"]] = relationship(secondary="UserGroups", back_populates="userList")

class budgets(Base):
    __tablename__ = "Budgets"

    budgetID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    budgetName: Mapped[str] = mapped_column(String(60), nullable=False)
    creatorID: Mapped[str] = mapped_column(ForeignKey("Users.userID"))
    creator: Mapped["users"] = relationship(back_populates="budgets")
    created: Mapped[str] = mapped_column(String(60), nullable=False)
    lastUpdated: Mapped[str] = mapped_column(String(60), nullable=False)
    items: Mapped[list["budgetItems"]] = relationship(secondary="ItemToBudgets", back_populates="budget")
    groupID: Mapped[int] = mapped_column(ForeignKey("BudgetGroups.groupID"), nullable=True)
    group: Mapped["groups"] = relationship()

class itemsToBudgets(Base):
    __tablename__ = "ItemToBudgets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    itemID: Mapped[int] = mapped_column(ForeignKey("BudgetItems.itemID"))
    budgetID: Mapped[int] = mapped_column(ForeignKey("Budgets.budgetID"))

class budgetItems(Base):
    __tablename__ = "BudgetItems"
    itemID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    budget: Mapped[list["budgets"]] = relationship(secondary="ItemToBudgets", back_populates="items")
    itemName: Mapped[str] = mapped_column(String(60), nullable=False)
    itemValue: Mapped[float] = mapped_column(Float, nullable=False)
    itemDescription: Mapped[str] = mapped_column(String(120), nullable=False)

class userGroups(Base):
    __tablename__ = "UserGroups"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    group: Mapped[int] = mapped_column(ForeignKey("BudgetGroups.groupID"))
    user: Mapped[int] = mapped_column(ForeignKey("Users.userID"))

class groups(Base):
    __tablename__ = "BudgetGroups"
    groupID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    groupName: Mapped[str] = mapped_column(String(60), nullable=False)
    userList: Mapped[list["users"]] = relationship(secondary="UserGroups", back_populates="groups")

class sessionLog(Base):
    __tablename__ = "SessionLog"
    sessionID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user: Mapped[int] = mapped_column(ForeignKey("Users.userID"))
    session_key: Mapped[str] = mapped_column(String(32),
                                             default=lambda:str(uuid.uuid4().hex),
                                             unique=True,
                                             index=True
                                             )
    created: Mapped[str] = mapped_column(String(32), nullable=False)
    ends: Mapped[str] = mapped_column(String(32), nullable=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creating the db
Base.metadata.create_all(bind = engine)