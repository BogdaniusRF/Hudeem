import asyncio
from sqlalchemy import ForeignKey, String, BigInteger, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declarative_base
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.sql import func
import os
from pgvector.sqlalchemy import Vector
from dotenv import load_dotenv
load_dotenv()
# You'll need to specify your PostgreSQL connection URL
# Example format: 'postgresql+asyncpg://username:password@localhost:5432/database_name'
# Uncomment and adjust the following line according to your setup:
#from config import DB_URL

DB_name='postgres'
DBpassword = os.getenv("Postgres_Psw")
if not DBpassword:
    raise ValueError("Не удалось загрузить пароль из переменной окружения Postgres_Psw.")


DB_URL = f'postgresql+asyncpg://v_user:{DBpassword}@localhost:5433/{DB_name}'


# Change the engine to use PostgreSQL with asyncpg driver
engine = create_async_engine(
    url=DB_URL,
    echo=True
)

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs,DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)


class ChatHistory(Base):
    __tablename__ = "chat_history"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    question: Mapped[str] = mapped_column(String)
    response: Mapped[str] = mapped_column(String)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    question_vector: Mapped[Vector] = mapped_column(Vector(1024), nullable=True)
    response_vector: Mapped[Vector] = mapped_column(Vector(1024), nullable=True)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)