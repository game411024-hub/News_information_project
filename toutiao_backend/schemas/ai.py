from pydantic import BaseModel, Field


#定义接受前端发来的请求数据类
from typing import List, Literal
from pydantic import BaseModel, Field


# 定义单条消息的结构
class Message(BaseModel):
    # role: 消息角色，Literal 限定只能是这三个值之一
    role: Literal["user", "assistant", "system"] = Field(..., description="消息角色")
    # content: 消息内容，必须是字符串
    content: str = Field(..., description="消息内容")


# 定义请求体：messages 是 Message 对象的列表
class AiRequest(BaseModel):
    messages: List[Message] = Field(..., description="对话历史消息列表")