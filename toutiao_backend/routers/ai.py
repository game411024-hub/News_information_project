from fastapi import APIRouter
# 从 fastapi 模块中导入 StreamingResponse,这个模块用于流式响应
from fastapi.responses import StreamingResponse
from schemas.ai import AiRequest
from utils.ai_generate import generate
from utils.local_model import local_generate


"""
ai对话模块，提供对话功能
"""
router = APIRouter(prefix="/api/ai", tags=["ai"])

#获取ai响应的回答
@router.post("/chat")
async def chat(
        messages: AiRequest
):
    request_messages = messages.messages
    # 调用 generate 函数，传入 messages,返回一个生成器, media_type="text/event-stream" 表示返回类型为事件流
    # return StreamingResponse(generate(request_messages), media_type="text/event-stream")
    return StreamingResponse(local_generate(request_messages), media_type="text/event-stream")
