from sqlalchemy import Boolean, String, Integer, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
import uuid

engine = create_engine("mysql+pymysql://root:admin@tracky_db:3316/tracky", echo=True)

class Base(DeclarativeBase):
    pass

# Table
class test(Base):
    __tablename__ = "test"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creating the db
Base.metadata.create_all(bind = engine)