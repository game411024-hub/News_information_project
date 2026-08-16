from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator
from schemas.base import NewsItemBase


#检查是否收藏的请求体
class CheckIsFavorite(BaseModel):
    isFavorite: bool = Field(...,alias="isFavorite")
    """
    检查是否收藏的请求体
    """

#新增收藏的请求体
class AddNewsId(BaseModel):
    newsId: int = Field(...,alias="newsId")
    """
    新增收藏的请求体
    """
#定义响应数据模型类
class FavoriteResponse(BaseModel):
    """
    响应数据模型类
    """
    id: int
    user_id: int = Field(...,alias="userId")
    news_id: int = Field(...,alias="newsId")
    created_at:datetime = Field(...,alias="createTime")
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )




#定义获取收藏列表响应模型类
class ListResponse(NewsItemBase):
    """
    获取收藏列表响应模型类
    """
    favorite_time: datetime = Field(alias="favoriteTime")
    favorite_id: int = Field(alias="favoriteId")
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

class FavoriteListResponse(BaseModel):
    """
    获取收藏列表响应模型类
    """
    list: list[ListResponse]
    total: int = Field(alias="total")
    has_more: bool = Field(alias="hasMore")
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )
