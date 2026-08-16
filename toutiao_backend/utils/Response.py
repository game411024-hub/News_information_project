from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


# ============================================================
# 封装通用成功响应格式 - 操作步骤
# ============================================================
# 【目标】
# 统一所有 API 接口的返回格式，避免每个路由手写重复结构
# 最终格式：{"code": 200, "message": "success", "data": {...}}
# ============================================================
# 【步骤 1】定义通用响应数据类型（新建 schemas/response.py）
# ------------------------------------------------------------
# 1. 继承 Pydantic 的 BaseModel
# 2. 定义三个字段：code、message、data
#    - code 设为 int 类型，默认值 200
#    - message 设为 str 类型，默认值 "success"
#    - data 设为 Optional[Any]，默认值 None
# 3. 内部配置 model_config 开启 from_attributes = True
#    （作用：支持传入 SQLAlchemy ORM 对象时自动序列化）
# 【步骤 2】抽取响应结果工具函数（新建 utils/response.py）
# ------------------------------------------------------------
# 1. 从 fastapi.responses 导入 JSONResponse
# 2. 从 fastapi.encoders 导入 jsonable_encoder
# 3. 定义函数 success_response，接收参数 message 和 data
# 4. 函数内部：
#    a. 组装字典：{"code": 200, "message": message, "data": data}
#    b. 把字典传给 jsonable_encoder 进行转换
#    c. 将转换后的结果放入 JSONResponse 并 return
#
# 注意：jsonable_encoder 作用：
#       - 自动处理 datetime、Decimal 等无法直接 JSON 序列化的类型
#       - 自动把 SQLAlchemy ORM 对象转换成字典
# 【步骤 3】在路由处理函数中调用（任意 router 或 main）
# ------------------------------------------------------------
# 1. 导入刚才定义的 success_response 函数
# 2. 在业务逻辑处理完成后，把要返回的数据传给 data 参数
# 3. 直接 return success_response(data=你的数据)
# 4. 如果有自定义提示信息，传 message 参数
# 【扩展建议（可选）】
# ------------------------------------------------------------
# - 如果需要返回错误响应，可以单独封装 error_response 函数
#   格式为：{"code": 400/401/403/404/500, "message": "错误信息", "data": None}
# - 将这两个函数统一放在 utils/response.py 中，全局复用
# ============================================================


def success_response(message:str="success",data=None):
    """
    成功响应
    """
    content={
        "code":200,
        "message":message,
        "data":data
    }
    # 响应JSON数据，把任何FastAPI、Pydantic、ORM 对象转换成可以被 JSON 安全序列化的数据结构
    return JSONResponse(content=jsonable_encoder(content))