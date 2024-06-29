import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import  Integer, String

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "201224")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "swapi")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")

PG_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass

class SwapiPeople(Base):
    __tablename__ = "swapi_people"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    birth_year: Mapped[str] = mapped_column(String(256), unique=False, nullable=True)
    eye_color: Mapped[str] = mapped_column(String(256), unique=False, nullable=True)
    films: Mapped[str] = mapped_column(String(1024), unique=False, nullable=True)
    gender: Mapped[str] = mapped_column(String(256), unique=False, nullable=True)
    hair_color: Mapped[str] = mapped_column(String(256), unique=False, nullable=True)
    height: Mapped[str] = mapped_column(String(256), unique=False, nullable=True)
    homeworld: Mapped[str] = mapped_column(String(256), unique=False, nullable=True)
    mass: Mapped[str] = mapped_column(String(256), unique=False, nullable=True)
    name: Mapped[str] = mapped_column(String(256), unique=False, nullable=True)
    skin_color: Mapped[str] = mapped_column(String(256), unique=False, nullable=True)
    species: Mapped[str] = mapped_column(String(1024), unique=False, nullable=True)
    starships: Mapped[str] = mapped_column(String(1024), unique=False, nullable=True)
    vehicles: Mapped[str] = mapped_column(String(1024), unique=False, nullable=True)


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


