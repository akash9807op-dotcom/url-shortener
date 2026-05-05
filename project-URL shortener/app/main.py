from fastapi import FastAPI,Request,Depends,status,HTTPException
from sqlalchemy.orm import Session
from . import schemas
from .utils import generate_key,base62_encode,base62_decode,rate_limiting
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import logging
from sqlalchemy import select
from .custom_exception import Database_Server_Exception
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
load_dotenv()
app=FastAPI()
app.exception_handler(Database_Server_Exception)

from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column

class Base(DeclarativeBase):
    pass
class Url(Base):
    __tablename__ = "url"

    id: Mapped[int] = mapped_column(
        Sequence("url_id_seq", start=100001),
        primary_key=True
    )

    value: Mapped[str] = mapped_column()



DATABASE_URL=f"postgresql+asyncpg://{os.getenv('user')}:{os.getenv('password')}@{os.getenv('host')}:{os.getenv('port')}/{os.getenv('dbname')}"
engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False
)
async def get_db():
    async with SessionLocal() as session:
        yield session






logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger=logging.getLogger(__name__)


base=os.getenv('base')

@app.get("/")
async def root(request:Request):
    return {"status":True,"data":"This is Root page"}

@app.post("/miniurl/",status_code=201)
async def url_shortner(request:Request,payload:schemas.UrlIn,db:AsyncSession=Depends(get_db)):
    user_url=str(payload.url)
    # rate_limiting(request,1)
    obj=Url(value=user_url)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    new_url=base+base62_encode(obj.id)
    # logger.info(f"Shortening URL: {user_url}")  # Log what's happening
    return {"status": True, "data": new_url}


@app.get("/miniurl/{key}")
async def get_url(key:str,db:AsyncSession=Depends(get_db)):
    id=base62_decode(key)
    result = await db.execute(select(Url.value).where(Url.id == id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404)
    return {"status":True,"data":obj}




# def counter():
#     cnt=1
#     def wrapper():
#         nonlocal cnt
#         cnt+=1
#         print("ineer functiopn start")
#         print(cnt)
#         print("Innner Fuction end ")
#     return wrapper
# counting=counter()


# from fastapi import FastAPI,Request,HTTPException
# from pydantic import HttpUrl,ValidationError
# from . import schemas
# from .utils import generate_key,base62_encode,base62_decode
# import psycopg2
# from fastapi.responses import HTMLResponse,RedirectResponse
# import uvicorn
# from psycopg2 import pool
# import os
# import logging
# from dotenv import load_dotenv
# load_dotenv()
# app=FastAPI()
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# )
# logger=logging.getLogger(__name__)

# base=os.getenv('base')
# database_url=f"dbname={os.getenv('dbname')}  user={os.getenv('user')} password={os.getenv('password')} host={os.getenv('host')} port={os.getenv('port')}"
# db_pool=pool.ThreadedConnectionPool(
#     minconn=4,
#     maxconn=12,
#     dsn=database_url
# )

# @app.get("/")
# def root(request:Request):
#     return {"success":True,"data":"This is Root page"}

# @app.post("/miniurl/")
# async def url_shortner(payload:schemas.UrlIn):
#     conn=db_pool.getconn()
#     cur=conn.cursor()
#     try:
#         url = str(payload.url)

#         cur.execute("INSERT INTO URL (VALUE) VALUES (%s) RETURNING *;",(url,))
#         key=cur.fetchone()
#         conn.commit()
#         new_url=base+base62_encode(key[0])
#         logger.info(f"Shortening URL: {url}")  # Log what's happening
#         return {"success": True, "data": new_url}
#     except Exception as e:
#         logger.error(f"Database error: {e}")
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cur.close()
#         db_pool.putconn(conn)
# @app.get("/miniurl/{key}")
# async def get_url(key:str):
#     id=base62_decode(key)
#     conn=db_pool.getconn()
#     cur=conn.cursor()
#     try:
#         cur.execute("SELECT VALUE FROM URL WHERE id=%s;",(id,))
#         value=cur.fetchone()
#         logger.info(f"RETRIVING URL KEY: {key}")  # Log what's happening

#         if value:
#             value=str(value[0])
#             return {"success":True,"data":value}
#             # return RedirectResponse(url=value,status_code=302)

#         raise HTTPException(status_code=404)
#     except Exception as e:
#         logger.error(f"Database error: {e}")
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cur.close()
#         db_pool.putconn(conn)