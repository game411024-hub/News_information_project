import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

"""
SQLAlchemy 异步连接池配置
"""
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "news_app")

ASYNC_DATABASE_URL = (
    f"mysql+aiomysql://{MYSQL_USER}:{quote_plus(MYSQL_PASSWORD)}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8"
)
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True, #可选，是否打印SQL语句
    pool_size=10,#连接池大小
    max_overflow=20,#连接池溢出时最大连接数
)

#创建异步会话工厂，创建异步会话
Async_Local_Session = async_sessionmaker(
    bind = async_engine,#原材料从哪个仓库拿（连哪个数据库）
    #指定会话类
    class_=AsyncSession,#我要做的是"全麦面包"（异步会话），不是"白面包"（普通同步会话）
    expire_on_commit=False,#面包出炉后别急着扔掉，还能再用
)

#依赖项
async def get_db():#创建数据库连接
    async with Async_Local_Session() as session:#创建一个异步会话
        try:
            yield session#返回一个数据库连接
            await session.commit()#提交事务
        except Exception:#异常处理
            await session.rollback()#回滚事务
            raise
        finally:#释放资源
            await session.close()



