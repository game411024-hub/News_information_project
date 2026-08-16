from cache import news_cache
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.sql import select,update
from sqlalchemy.ext.asyncio import AsyncSession
from toutiao_backend.models.news import Category, News
from schemas.base import NewsItemBase
# 获取新闻分类
async def get_categories(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ):
    # 获取缓存数据
    news_categories = await news_cache.get_news_cache()
    if news_categories:
        return news_categories
    #---------------------------------------------------
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    # return result.scalars().all()
    data_categories = result.scalars().all()
    #旁路缓存数据Redis，提高查询速度
    # 写入缓存
    if data_categories:
        stmt = jsonable_encoder(data_categories)
        await news_cache.set_cache_categories(stmt)
    #返回数据
    return data_categories


# 获取新闻列表
async def get_news_list(
        db: AsyncSession,#数据库连接
        category_id: int,#分类ID
        skip: int = 0,#跳过几条数据
        page_size: int = 10#每页10条数据
    ):
    # 获取缓存数据
    page = (skip // page_size) + 1#页码
    news_list = await news_cache.get_news_list_cache(category_id, page, page_size)
    if news_list:
        return news_list
    # 获取数据库里面新闻数据，offset表示跳过几条数据，limit表示每页10条数据
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(page_size)
    result = await db.execute(stmt)
    stmt = result.scalars().all()
    # 写入缓存
    if stmt:
        #先把ORM数据转换为字典
        dict_stmt = [NewsItemBase.model_validate(news).model_dump(mode="json",by_alias=False) for news in stmt]
        await news_cache.set_news_list_cache(category_id, page, page_size, dict_stmt)
    return stmt


# 获取新闻总数
async def get_news_total(
        db: AsyncSession,
        category_id: int
    ):
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()

#获取新闻详情
async def get_news_detail(
        db: AsyncSession,
        news_id: int
    ):
    #获取缓存数据
    news_detail = await news_cache.get_news_detail_cache(news_id)
    if news_detail:
        return news_detail

    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    scalar_data = result.scalar_one_or_none()
    #写入缓存
    if scalar_data:#jsonable_encoder的意思是把ORM数据转换为字典
        str_data = jsonable_encoder(scalar_data)
        str_data.pop("views", None)
        await news_cache.set_news_detail_cache(news_id,str_data)
    return jsonable_encoder(scalar_data)

# 更新新闻浏览量
async def update_news_views(
        db: AsyncSession,
        news_id: int
):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()
    #获取返回views的数值
    stmt = select(News.views).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# 统一的"ORM对象列表 → 前端字典列表"转换函数
# 缓存回填和未命中返回都使用它，保证两条路径返回的结构一致（驼峰键）
def related_news_to_dict(related_news):
    return [{
        "id": news_detail.id,
        "title": news_detail.title,
        "content": news_detail.content,
        "image": news_detail.image,
        "author": news_detail.author,
        "publishTime": news_detail.publish_time.isoformat(),# ISO格式时间字符串
        "categoryId": news_detail.category_id,
    } for news_detail in related_news]


#获取同类推荐新闻
async def get_related_news(
        db: AsyncSession,
        news_id: int ,
        category_id: int,
        limit: int = 5,
):
    # 获取同类新闻缓存数据
    related_news = await news_cache.get_similar_news_cache(news_id, category_id, limit)
    if related_news:
        return related_news
    stmt = select(News).where(
        News.category_id == category_id, News.id != news_id
    ).order_by(
        News.views.desc(),
        News.publish_time.desc(),
    ).limit(limit)
    result = await db.execute(stmt)
    related_news = result.scalars().all()
    # 写入同类新闻缓存数据缓存
    if related_news:
        # dict_related_news = jsonable_encoder(related_news)
        # 原代码用 jsonable_encoder 转出的键是下划线（publish_time、category_id），
        # 与下方返回的驼峰结构不一致 → 命中缓存时前端拿到的字段名会变
        dict_related_news = related_news_to_dict(related_news)  # 统一转换函数：缓存里直接存最终返回的驼峰结构
        await news_cache.set_similar_news_cache(news_id, category_id, limit, dict_related_news)
    # 原代码：手写列表推导式返回（驼峰结构），与缓存命中返回的 jsonable_encoder 结构（下划线）不一致
    # return [{
    #     "id": news_detail.id,
    #     "title": news_detail.title,
    #     "content": news_detail.content,
    #     "image": news_detail.image,
    #     "author": news_detail.author,
    #     "publishTime": news_detail.publish_time,
    #     "categoryId": news_detail.category_id,
    # } for news_detail in related_news
    # ]
    return related_news_to_dict(related_news)  # 与缓存命中路径共用同一转换，结构必然一致


