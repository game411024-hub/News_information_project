import os
import json
from pathlib import Path

import redis.asyncio as redis
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD") or None



# Redis连接配置
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD,
    decode_responses=True
)
#设置 和 读取（字符串 和 列表或字典）
#读取：字符串
async def get_cache(key:str):
    try:
        return redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败：{e}")
        return None
#读取：字符串 和 列表或字典
async def get_json_cache(key:str):
    try:
        data =await redis_client.get(key)
        if data:
            return json.loads(data)# 反序列化
        """
        序列化（json.dumps()）：把 Python 对象（比如字典、列表）变成 字符串（JSON 格式的文
        本）。
        反序列化（json.loads()）：把 字符串（JSON 格式的文本）变回 Python 对象。
        """
        return None
    except Exception as e:
        print(f"获取缓存失败：{e}")
        return None

#设置缓存setex（key, expire, value）
async def set_cache(key:str, value:str, expire:int):
    try:
        if isinstance(value,(list,dict)):
            value = json.dumps(value, ensure_ascii=False)
            await redis_client.setex(key, expire, value)
            return True
    except Exception as e:
        print(f"设置缓存失败：{e}")
        return False
