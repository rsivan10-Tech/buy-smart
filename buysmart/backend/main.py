from datetime import datetime
import os
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Float, Integer, String, text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

POSTGRES_USER = os.getenv('POSTGRES_USER', 'buysmart_user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'buysmart_pass')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'buysmart_db')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'postgres')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

POSTGRES_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
SQLITE_URL = os.getenv('SQLITE_URL', 'sqlite+aiosqlite:///./local.db')

engine: Optional[AsyncEngine] = None
AsyncSessionLocal: Optional[sessionmaker] = None
Base = declarative_base()


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    city = Column(String(128), nullable=False, index=True)
    area_sqm = Column(Float, nullable=True)
    price_ils = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'), nullable=False)


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    city: str = Field(..., min_length=1, max_length=128)
    area_sqm: Optional[float] = None
    price_ils: Optional[float] = None


class ProjectRead(ProjectCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


app = FastAPI(title='Buy Smart Backend', version='0.2.0')


def configure_engine(url: str) -> AsyncEngine:
    return create_async_engine(url, echo=False, future=True)


@app.on_event('startup')
async def startup_event():
    global engine, AsyncSessionLocal

    # Primary engine: Postgres (dockerized)
    try:
        engine = configure_engine(POSTGRES_URL)
        AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with engine.begin() as conn:
            await conn.execute(text('SELECT 1'))
            await conn.run_sync(Base.metadata.create_all)
        print('Connected to Postgres:', POSTGRES_URL)
        return
    except Exception as e:
        print('Postgres unavailable, switching to SQLite fallback:', e)

    # Fallback engine: local SQLite
    engine = configure_engine(SQLITE_URL)
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('Connected to SQLite:', SQLITE_URL)


@app.get('/')
async def root():
    return {'message': 'שלום עולם - Buy Smart API הגיע'}


@app.get('/health')
async def health():
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(text('SELECT 1'))
            value = result.scalar_one()
            return {'db': 'ok' if value == 1 else 'fail'}
        except Exception as e:
            raise HTTPException(status_code=503, detail=f'DB health check failed: {e}')


@app.get('/api/welcome')
async def welcome():
    return {'message': 'ברוכים הבאים ל-Buy Smart'}


@app.post('/projects', response_model=ProjectRead, status_code=201)
async def create_project(project: ProjectCreate):
    try:
        async with AsyncSessionLocal() as session:
            db_project = Project(
                name=project.name,
                city=project.city,
                area_sqm=project.area_sqm,
                price_ils=project.price_ils,
            )
            session.add(db_project)
            await session.commit()
            await session.refresh(db_project)
            return db_project
    except Exception as e:
        raise HTTPException(status_code=503, detail=f'Database not available: {e}')


@app.get('/projects', response_model=List[ProjectRead])
async def list_projects():
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text('SELECT * FROM projects ORDER BY created_at DESC'))
            projects = result.scalars().all()
            return projects
    except Exception as e:
        raise HTTPException(status_code=503, detail=f'Database not available: {e}')


@app.get('/projects/{project_id}', response_model=ProjectRead)
async def get_project(project_id: int):
    try:
        async with AsyncSessionLocal() as session:
            project = await session.get(Project, project_id)
            if not project:
                raise HTTPException(status_code=404, detail='Project not found')
            return project
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail=f'Database not available: {e}')
