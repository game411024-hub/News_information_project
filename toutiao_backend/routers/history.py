from config.db_conf import get_db
from fastapi import APIRouter, Query, HTTPException, Depends, status, Path
from models.users import User
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession
from utils.Response import success_response
from utils.auth import authenticate_current_user
from crud import history
from schemas.history import AddHistoryResponse, AddHistory,HistoryListResponse

"""
浏览模块
"""

router = APIRouter(prefix="/api/history", tags=["history"])

#添加浏览记录
@router.post("/add")
async def add_history(
        news_id:AddHistory,
        db:AsyncSession = Depends(get_db),#数据库会话
        auth_token_user:User = Depends(authenticate_current_user)#验证用户
):
   db_history = await history.add_history(db, auth_token_user.id,news_id.news_id)
   data = AddHistoryResponse(id=db_history.id, userId=db_history.user_id, newsId=db_history.news_id, viewTime=db_history.view_time)
   return success_response(message="添加成功",data=data)

 #获取浏览历史列表
@router.get("/list")
async def get_history_list(
         page: int = Query(1, ge=1, title="页码"),
         page_size: int = Query(10, le=100, title="每页数量"),
         db:AsyncSession = Depends(get_db),#数据库会话
         auth_token_user:User = Depends(authenticate_current_user)#验证用户
 ):
    rows_list, total_count = await history.get_history_list_total(db, auth_token_user.id, page, page_size)
    has_more = total_count > page * page_size
    data = HistoryListResponse(list=rows_list,total=total_count,hasMore=has_more)
    return success_response(message="获取成功",data=data)

#删除单条浏览记录
@router.delete("/delete/{history_id}")
async def delete_history(
        history_id: int = Path(..., ge=1, title="浏览记录ID"),
        db:AsyncSession = Depends(get_db),#数据库会话
        auth_token_user:User = Depends(authenticate_current_user)#验证用户
):
    result = await history.delete_history(db, auth_token_user.id, history_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="浏览记录不存在")
    return success_response(message="删除成功")

#清空浏览历史
@router.delete("/clear")
async def clear_history(
        db:AsyncSession = Depends(get_db),#数据库会话
        auth_token_user:User = Depends(authenticate_current_user)#验证用户
):
    result = await history.delete_all_history(db, auth_token_user.id)
    if not result:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="浏览记录不存在"
    )
    return success_response(message="清空成功")



