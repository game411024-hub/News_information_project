from config.db_conf import get_db
from crud import favorites
from fastapi import APIRouter, Depends, Query, HTTPException,status
from models.users import User
from pydantic import BaseModel
from schemas.favorites import CheckIsFavorite, AddNewsId, FavoriteResponse, FavoriteListResponse
from sqlalchemy.ext.asyncio import AsyncSession
from utils.Response import success_response
from utils.auth import authenticate_current_user


"""
    收藏模块
"""
router = APIRouter(prefix="/api/favorite", tags=["favorites"])


#检查新闻收藏状态
@router.get("/check")
async def check_favorite(
    db: AsyncSession = Depends(get_db),
    news_id: int = Query(..., alias="newsId"),
    auth_token_user:User = Depends(authenticate_current_user),
):
    """
    检查新闻收藏状态
    """
    user_favorites = await favorites.is_favorite(db,auth_token_user.id,news_id)
    #->返回是否喜欢的判断，如果收藏了对应的新闻就返回true，否则返回false
    data = CheckIsFavorite(isFavorite=user_favorites)
    return  success_response(message="获取成功！",data=data)

#添加收藏
@router.post("/add")
async def add_favorite(
    news_id:AddNewsId,
    db: AsyncSession = Depends(get_db),
    auth_token_user:User = Depends(authenticate_current_user),
):
    """
    添加收藏
    """
    orm_favorite_result = await favorites.add_favorite(db,auth_token_user.id,news_id.newsId)
    if not orm_favorite_result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="添加收藏失败！"
        )
    data =FavoriteResponse.model_validate(orm_favorite_result)
    return success_response(message="收藏成功",data=data)

#取消收藏
@router.delete("/remove")
async def remove_favorite(
    news_id:int = Query(..., alias="newsId"),
    db: AsyncSession = Depends(get_db),
    auth_token_user:User = Depends(authenticate_current_user),
):
    """
    取消收藏
    """
    orm_remove_result = await favorites.remove_favorite(db,auth_token_user.id,news_id)
    if not orm_remove_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="未找到此收藏！"
        )

    return success_response(message="取消收藏成功",data=None)

#获取收藏列表
@router.get("/list")
async def get_favorite_list(
    db: AsyncSession = Depends(get_db),
    auth_token_user:User = Depends(authenticate_current_user),
    page: int = Query(1, ge=1, title="页码"),
    page_size: int = Query(10,ge=1,le = 100, title="每页条数"),

):
    """
    获取收藏列表
    """
    total, favorites_list = await favorites.get_favorite_list(db,auth_token_user.id,page,page_size)
    has_more = total > page * page_size#是否有更多
    data = FavoriteListResponse(list=favorites_list,total=total,hasMore=has_more)
    return success_response(message="获取成功",data=data)

#清空收藏
@router.delete("/clear")
async def clear_favorite(
    db: AsyncSession = Depends(get_db),
    auth_token_user:User = Depends(authenticate_current_user),
):
    """
    清空收藏
    """
    count = await favorites.clear_favorite(db,auth_token_user.id)
    return success_response(message=f"成功删除{count}条收藏记录")

