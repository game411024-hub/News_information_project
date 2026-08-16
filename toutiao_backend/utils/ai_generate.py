import json

from config.ai_config import client

"""
前端浏览器
  │ ① POST /api/ai/chat，body: {"messages": [{role, content}, ...]}
  ▼
FastAPI 路由函数 chat()
  │ ② 把 request.messages 传给生成器
  ▼
生成器函数 generate(messages)
  │ ③ 调阿里云：client.chat.completions.create(stream=True)
  ▼
阿里云服务器开始流式返回
  │ ④ 一个 chunk 一个小片段（"你"、"好"、"世"、"界"）
  ▼
生成器 for chunk in response 遍历
  │ ⑤ 提取 delta.content，包装成 SSE 格式
  ▼
yield 一段一段吐出来
  │ ⑥
  ▼
StreamingResponse 边收边发给浏览器
  │ ⑦
  ▼
前端 fetch 流式读取，逐字显示
"""
# 定义生成器函数 generate，接收对话消息列表 messages
# 生成器：调用时不执行，迭代时才逐段执行并 yield 产出
async def generate(messages):
    """流式生成器:逐块产出 SSE 格式数据"""
    # 调用大模型接口（DashScope 的 OpenAI 兼容接口）
    response = client.chat.completions.create(
        # 指定要使用的模型名称
        model="deepseek-v4-pro",
        # 传入对话消息列表，结构为 [{role, content}, ...]
        messages=messages,
        stream=True,                    # 关键:开启流式
        # 开启流式后 create() 不等待完整回答，立即返回可迭代对象
        # 设置思考强度为 high（深度推理）
        reasoning_effort="high",
        # 通过 extra_body 开启思考模式：先输出推理过程，再输出正式回答
        extra_body={"thinking": {"type": "enabled"}}
    )
    #流式输出
    # 遍历响应对象，每个 chunk 是一小段增量（可能只有一个字）
    for chunk in response:              # 每个 chunk 是一小段增量
        # 取出当前片段的文本：嵌套结构 chunk → choices[0] → delta → content
        content = chunk.choices[0].delta.content# 获取增量内容
        # 部分 chunk（如思考过程）content 为 None，必须过滤掉
        if content is not None:         # 部分 chunk(如思考过程)content 为 None
            # 把增量内容包装成 OpenAI 兼容的 JSON 结构，方便前端解析
            sse_data = json.dumps(
                # choices[0].delta.content 与前端读取路径保持一致
                {"choices": [{"delta": {"content": content}}]},
                # ensure_ascii=False：中文原样输出，不转成 \uXXXX 转义序列
                ensure_ascii=False      # 中文不转义成 \uXXXX
            )
            # 按 SSE 协议格式产出：data: + JSON 内容 + 空行（空行表示一条消息结束）
            yield f"data: {sse_data}\n\n"# SSE 格式

    # 产出结束标记 [DONE]，前端读到它就知道流结束了
    yield "data: [DONE]\n\n"            # 结束标记,前端靠它收尾





