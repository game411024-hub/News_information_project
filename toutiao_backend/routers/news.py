from crud import cache_news
from toutiao_backend.config.db_conf import get_db
from fastapi import APIRouter, Depends, HTTPException
# from toutiao_backend.crud import news
from fastapi import Query
from sqlalchemy.ext.asyncio import AsyncSession





router = APIRouter(prefix="/api/news", tags=["news"])


"""
    新闻模块
"""
# 获取新闻分类
@router.get("/categories")
async def get_categories(db: AsyncSession = Depends(get_db),skip: int = 0,
        limit: int = 100

):
    categories = await cache_news.get_categories(db, skip=skip, limit=limit)

    # categories = await news.get_categories(db, skip=skip, limit=limit)
    # 先获取数据库里面新闻分类数据->先定义模型类->封装查询数据的方法
    return {
            "code":200,
            "message":"获取分类成功",
            "data":categories
            }

# 获取新闻列表
@router.get("/list")
async def get_news_list(
        db: AsyncSession = Depends(get_db),
        category_id: int = Query(..., alias="categoryId"), #设置别名
        page: int = 1,
        page_size: int = Query(default=10,ga=0,le=100,alias="pageSize")

):
    offset = (page - 1) * page_size                                         #计算偏移量
    news_list = await cache_news.get_news_list(db, category_id, offset, page_size)   #获取新闻列表
    total_count = await cache_news.get_news_total(db, category_id)                      #获取新闻总数
    # news_list = await news.get_news_list(db, category_id, offset, page_size)   #获取新闻列表
    # total_count = await news.get_news_total(db, category_id)                      #获取新闻总数
    # 跳过的 + 获取的条数 < 总数
    has_more = offset + len(news_list) < total_count                        #判断是否有更多
    return {
        "code":200,
        "message":"获取新闻列表成功",
        "data":{
            "list":news_list,
            "total":total_count,
            "hasMore":has_more

        }
    }

# 获取新闻详情
@router.get("/detail")
async def get_news_detail(
        db: AsyncSession = Depends(get_db),
        news_id: int = Query(..., alias="id")
):
    # news_detail = await news.get_news_detail(db, news_id)
    news_detail = await cache_news.get_news_detail(db, news_id)
    if not news_detail:
        raise HTTPException(
            status_code=404,
            detail="新闻不存在！"
        )
    # result = await news.update_news_views(db, news_detail.id)
    views_data = await cache_news.update_news_views(db, news_detail["id"])
    if views_data is None:
        raise HTTPException(
            status_code=404,
            detail="暂无数据，请联系管理员！"
        )
    related_news = await cache_news.get_related_news(db, news_detail["id"], news_detail["category_id"])
    # related_news = await news.get_related_news(db, news_detail.id, news_detail.category_id)
    return {
          "code": 200,
          "message": "success",
          "data": {
            "id": news_detail["id"],
            "title":news_detail["title"],
            "content": news_detail["content"],
            "image": news_detail["image"],
            "author": news_detail["author"],
            "publishTime": news_detail["publish_time"],
            "categoryId": news_detail["category_id"],
            "relatedNews": related_news
          }
    }

