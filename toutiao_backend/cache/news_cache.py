from typing import List, Dict, Any, Optional

from config.cache_config import get_json_cache, set_cache

CATEGORY_KEY = "news:categories"
NEWS_LIST_PREFIX = "news:list:"
#读取新闻类缓存
async def get_news_cache():
    return await get_json_cache(CATEGORY_KEY)

#存入新闻类缓存
async def set_cache_categories(
        data:List[Dict[str,Any]],
        expire:int = 7200
):
    return await set_cache(CATEGORY_KEY, data, expire)


#存入新闻列表缓存
async def set_news_list_cache(
        category_id:Optional[int],#分类ID
        page:int,#页码
        size:int,#每页大小
        news_list:List[Dict[str,Any]]#新闻列表
):
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{size}"
    return await set_cache(key, news_list, expire=1800)

#读取新闻列表缓存
async def get_news_list_cache(
        category_id:Optional[int],#分类ID
        page:int,#页码
        size:int,#每页大小
):
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{size}"
    return await get_json_cache(key)

#存入新闻详情缓存
async def set_news_detail_cache(
        news_id:Optional[int],#新闻ID
        news_detail:Dict[str,Any]#新闻详情
):
    news_detail_id =news_id if news_id is not None else "all"
    key = f"news:detail:{news_detail_id}"
    return await set_cache(key, news_detail, expire=1800)

#读取新闻详情缓存
async def get_news_detail_cache(
        news_id:Optional[int]#新闻ID
):
    news_detail_id = news_id if news_id is not None else "all"
    key = f"news:detail:{news_detail_id}"
    return await get_json_cache(key)

#存入同类新闻缓存
async def set_similar_news_cache(
        news_id:Optional[int],#新闻ID
        category_id:Optional[int],#分类ID
        size:int,#每页大小
        similar_news:List[Dict[str,Any]]#同类新闻
):
    similar_news_id = news_id if news_id is not None else "all"
    category_id = category_id if category_id is not None else "all"
    key = f"news:similar:{category_id}:{similar_news_id}:{size}"
    return await set_cache(key, similar_news, expire=1800)

#读取同类新闻缓存
async def get_similar_news_cache(
        news_id:Optional[int],#新闻ID
        category_id:Optional[int],#分类ID
        size:int,#每页大小
):
    similar_news_id = news_id if news_id is not None else "all"
    category_id = category_id if category_id is not None else "all"
    key = f"news:similar:{category_id}:{similar_news_id}:{size}"
    return await get_json_cache(key)





