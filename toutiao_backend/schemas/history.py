from pydantic import BaseModel
from pydantic import Field
from pydantic import ConfigDict
from datetime import datetime

from schemas.base import NewsItemBase


#定义添加浏览记录请求类
class AddHistory(BaseModel):
    news_id: int = Field(...,alias="newsId")
    # 配置类
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

#封装添加浏览记录响应类
class AddHistoryResponse(BaseModel):
    id: int
    user_id: int = Field(...,alias="userId")
    news_id: int = Field(...,alias="newsId")
    view_time: datetime = Field(...,alias="viewTime")
    # 配置类
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

#封装浏览历史列表响应类
class HistoryList(NewsItemBase):
    view_time: datetime = Field(...,alias="viewTime")

class HistoryListResponse(BaseModel):
    list: list[HistoryList]
    total: int
    has_more: bool = Field(...,alias="hasMore")
    # 配置类
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )
