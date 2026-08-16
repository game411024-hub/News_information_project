import json
from config.ai_config import OLLAMA_MODEL, local_client


# Ollama 提供 OpenAI 兼容 API（/v1 端点）
# 本地大模型生成器
async def local_generate(prompt):
    """流式生成器:逐块产出 SSE 格式数据"""
    response = local_client.chat.completions.create(
        # 指定要使用的模型名称
        model=OLLAMA_MODEL,
        # 传入对话消息列表，结构为 [{role, content}, ...]
        messages=prompt,
        stream=True,  # 关键:开启流式
    )
    # 流式输出
    # 遍历响应对象，每个 chunk 是一小段增量（可能只有一个字）
    for chunk in response:  # 每个 chunk 是一小段增量
        # 取出当前片段的文本：嵌套结构 chunk → choices[0] → delta → content
        content = chunk.choices[0].delta.content  # 获取增量内容
        # 部分 chunk（如思考过程）content 为 None，必须过滤掉
        if content :  # 部分 chunk(如思考过程)content 为 None
            # 把增量内容包装成 OpenAI 兼容的 JSON 结构，方便前端解析
            sse_data = json.dumps(
                # choices[0].delta.content 与前端读取路径保持一致
                {"choices": [{"delta": {"content": content}}]},
                # ensure_ascii=False：中文原样输出，不转成 \uXXXX 转义序列
                ensure_ascii=False  # 中文不转义成 \uXXXX
            )
            # 按 SSE 协议格式产出：data: + JSON 内容 + 空行（空行表示一条消息结束）
            yield f"data: {sse_data}\n\n"  # SSE 格式

    # 产出结束标记 [DONE]，前端读到它就知道流结束了
    yield "data: [DONE]\n\n"  # 结束标记,前端靠它收尾
