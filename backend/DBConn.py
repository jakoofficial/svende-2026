from sqlalchemy import Boolean, String, Integer, Float, ForeignKey, create_engine
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
    password: Mapped[str] = mapped_column(String(60))
    budgets: Mapped[list["budgets"]] = relationship(back_populates="creator")

class budgets(Base):
    __tablename__ = "Budgets"

    budgetID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    budgetName: Mapped[str] = mapped_column(String(60), nullable=False)
    creatorID: Mapped[str] = mapped_column(ForeignKey("Users.userID"))
    creator: Mapped["users"] = relationship(back_populates="budgets")
    created: Mapped[str] = mapped_column(String(60), nullable=False)
    lastUpdated: Mapped[str] = mapped_column(String(60), nullable=False)
    items: Mapped[list["budgetItems"]] = relationship(back_populates="budget")

class budgetItems(Base):
    __tablename__ = "BudgetItems"
    itemID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    budgetID: Mapped[int] = mapped_column(ForeignKey("Budgets.budgetID"))
    budget: Mapped[budgets] = relationship(back_populates="items")
    itemName: Mapped[str] = mapped_column(String(60), nullable=False)
    itemValue: Mapped[float] = mapped_column(Float, nullable=False)
    itemDescription: Mapped[str] = mapped_column(String(120), nullable=False)

# class userGroups(Base):
#     __tablename__ = "UserGroups"


# class groups(Base):
#     __tablename__ = "BudgetGroups"


# class sessionLog(Base):
#     __tablename__ = "SessionLog"

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creating the db
Base.metadata.create_all(bind = engine)