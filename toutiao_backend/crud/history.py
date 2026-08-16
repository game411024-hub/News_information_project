from datetime import datetime
from models.history import History
from models.news import News
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete


#添加浏览记录
async def add_history(
        db: AsyncSession,
        user_id: int,
        news_id: int
):

    """
    :return: 添加浏览记录，如果当前用户已浏览过该新闻则更新浏览时间，如果没有浏览过该新闻就添加新的浏览记录
    """
    #查询当前用户是否浏览过该新闻
    query_stmt = await db.execute(select(History).where(History.user_id == user_id,History.news_id == news_id))
    result_stmt = query_stmt.scalar_one_or_none()
    #如果没有就添加记录
    if not result_stmt:
        obj = History(user_id = user_id,news_id = news_id)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj
    #如果有就更新该用户浏览时间
    result_stmt.view_time = datetime.now()
    await db.commit()
    return result_stmt

#获取浏览历史列表和浏览总数
async def get_history_list_total(
        db: AsyncSession,
        user_id: int,
        page: int ,
        page_size: int
):
    #联表查询用户浏览历史
    #【知识点】select() 决定"返回哪些列"，join 只决定"行怎么匹配"
    #  - join + where：把结果过滤成"当前用户浏览过的新闻"（join 不负责带出字段）
    #  - order_by：按浏览时间倒序排列
    #  - 这里 select 了 2 列：News 实体 + history 表的 view_time 列（label 起别名 viewTime）
    #    所以每行 Row 有 2 个元素：(News对象, 浏览时间值)
    offset = (page-1)*page_size
    select_stmt = (((select(News,History.view_time.label("viewTime"))
                   .join(History,News.id == History.news_id)
                   .where(History.user_id == user_id))
                   .order_by(History.view_time.desc())).offset(offset).limit(page_size))
    # 对比：如果只 select(News)，即使联表了，每行 Row 也只有 1 个元素（News 对象）
    #       view_time 不在结果里 -> 后续解包 2 个变量会报错，且拼不出浏览时间
    # select_stmt = (((select(News)
    #                .join(History,News.id == History.news_id)
    #                .where(History.user_id == user_id))
    #                .order_by(History.view_time.desc())).offset(offset).limit(page_size))
    result = await db.execute(select_stmt)
    #【知识点】多列查询必须用 result.all() 获取完整 Row 列表
    #  - scalars() 只提取每行第一列（News），会丢失 view_time，且导致下面解包报错
    rows = result.all()
    #【知识点】select 列数 = 每行 Row 的元素数 = 解包变量的个数
    #  - 这里查了 2 列，每行解包成 news(News对象) 和 view_time(浏览时间)
    #  - news.__dict__ 展开成新闻字段字典，再补上 "viewTime" 键 -> 得到一条"新闻+浏览时间"数据
    rows_list = [{**news.__dict__,"viewTime": view_time} for news,view_time in rows]
    #浏览总数
    total = await db.execute(select(func.count()).select_from(History).where(History.user_id == user_id))
    total_count = total.scalar_one_or_none()
    return rows_list, total_count


#删除单条浏览记录
async def delete_history(
        db: AsyncSession,
        user_id: int,
        news_id: int
):
    """
    :return: 删除当前用户浏览过的某条新闻
    """
    #先查询，判断是否有该条数据，如果有就删除，如果没有就返回信息
    query_data = await db.execute(select(History).where(History.user_id == user_id,History.news_id == news_id))
    await db.commit()
    result = query_data.scalar_one_or_none()
    if not result:
        return False
    #删除当前用户浏览过的某条新闻
    stmt = await db.execute(delete(History).where(History.user_id == user_id,History.news_id == news_id))
    return stmt.rowcount > 0

#删除当前用户的所有浏览记录
async def delete_all_history(
        db: AsyncSession,
        user_id: int
):
    """
    :return: 删除当前用户的所有浏览记录
    """
    stmt = await db.execute(delete(History).where(History.user_id == user_id))
    await db.commit()
    return stmt.rowcount > 0





