from models.favorites import Favorite
from models.news import News
from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession


#是否是收藏
async def is_favorite(
        db: AsyncSession,
        user_id: int,
        news_id: int
):
    """
    :return: 返回是否喜欢的判断，如果收藏了对应的新闻就返回true，否则返回false
    """
    select_stmt = select(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    favorite = await db.execute(select_stmt)
    user_favorite = favorite.scalars().one_or_none()
    if user_favorite:
        return True
    else:
        return False

#添加收藏
async def add_favorite(
        db: AsyncSession,
        user_id: int,
        news_id: int
):
    """
    :return: 添加收藏成功收藏用户信息
    """
    orm_favorite =Favorite(user_id=user_id, news_id=news_id)
    db.add(orm_favorite)
    await db.commit()
    await db.refresh(orm_favorite)
    return  orm_favorite

#删除收藏
async def remove_favorite(
        db: AsyncSession,
        user_id: int,
        news_id: int
):
    """
    :return: 取消收藏成功返回true，否则返回false
    """
    delete_stmt = delete(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result =  await db.execute(delete_stmt)
    await db.commit()
    return result.rowcount > 0

#获取收藏列表
async def get_favorite_list(
        db: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int = 10
):
    """
    :return: 返回列表数据以及总条数
    """
    #查询总数
    query_total =await db.execute(select(func.count()).where(Favorite.user_id == user_id))
    total = query_total.scalar_one()
    #查询分页数据
    offset = (page - 1) * page_size
    select_stmt = (
        select(News, Favorite.created_at.label("favorite_time"),Favorite.id.label("favorite_id"))
                   .join(Favorite, News.id == Favorite.news_id)
                    .where(Favorite.user_id == user_id)
                    .order_by(Favorite.created_at.desc())
                    .offset(offset)
                    .limit(page_size)
    )
    result = await db.execute(select_stmt)
    rows = result.all()
    favorites_list = [{**news.__dict__, "favorite_time": favorite_time, "favorite_id": favorite_id} for news,favorite_time,favorite_id in rows]
    return total, favorites_list

#清空收藏
async def clear_favorite(
        db: AsyncSession,
        user_id: int
):
    """
    :return: 清空收藏返回删除的条数
    """
    delete_stmt = delete(Favorite).where(Favorite.user_id == user_id)
    result = await db.execute(delete_stmt)
    await db.commit()
    return result.rowcount or 0

